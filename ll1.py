from gramatica import Gramatica

class AnalizadorLL1:
    def __init__(self, gramatica: Gramatica):
        self.g = gramatica
        self.columnas = self.g.terminales + [Gramatica.FIN]
        self.filas = self.g.no_terminales + self.g.terminales + [Gramatica.FIN]
        self.tabla = {fila: {col: "" for col in self.columnas} for fila in self.filas}
        self.conflictos = []
        self._construir_tabla()

    def _construir_tabla(self):
        # 1. Reglas para No Terminales (numeradas desde 1 como en los apuntes)
        for num_regla, (izq, der) in enumerate(self.g.reglas, start=1):
            first_der = self.g.first_secuencia(der)

            for term in (first_der - {Gramatica.EPSILON}):
                self._asignar_celda(izq, term, str(num_regla))

            if Gramatica.EPSILON in first_der:
                for term in self.g.follow[izq]:
                    self._asignar_celda(izq, term, str(num_regla))

        # 2. Acciones POP para Terminales y Aceptar para '$'
        for term in self.g.terminales:
            self.tabla[term][term] = "POP"
        self.tabla[Gramatica.FIN][Gramatica.FIN] = "Aceptar"

    def _asignar_celda(self, fila, col, valor):
        if self.tabla[fila][col] != "" and self.tabla[fila][col] != valor:
            self.conflictos.append(
                f"Conflicto en ({fila}, {col}): ya tenía '{self.tabla[fila][col]}', se intentó poner '{valor}'"
            )
            self.tabla[fila][col] += f"/{valor}"
        else:
            self.tabla[fila][col] = valor

    def analizar_cadena(self, cadena_tokens):
        """
        Analiza una cadena de tokens separados por espacio (ej: 'num + num * num').
        Retorna (exito_bool, historial_de_pasos).
        """
        entrada = cadena_tokens.strip().split() + [Gramatica.FIN]
        pila = [Gramatica.FIN, self.g.simbolo_inicial]
        idx = 0
        historial = []

        while True:
            tope = pila[-1]
            actual = entrada[idx]
            pila_str = " ".join(pila)
            entrada_str = " ".join(entrada[idx:])

            accion = self.tabla.get(tope, {}).get(actual, "")

            if accion == "Aceptar":
                historial.append((pila_str, entrada_str, "Aceptar"))
                return True, historial

            elif accion == "POP":
                historial.append((pila_str, entrada_str, f"POP ({actual})"))
                pila.pop()
                idx += 1

            elif accion.isdigit():
                num_regla = int(accion)
                izq, der = self.g.reglas[num_regla - 1]
                regla_str = f"{num_regla}: {izq} -> {' '.join(der)}"
                historial.append((pila_str, entrada_str, regla_str))
                pila.pop()
                if der != [Gramatica.EPSILON]:
                    for simb in reversed(der):
                        pila.append(simb)
            else:
                historial.append((pila_str, entrada_str, f"ERROR (sin transición para '{tope}' con '{actual}')"))
                return False, historial
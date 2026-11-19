from collections import deque
from gramatica import Gramatica

class AnalizadorLR0:
    def __init__(self, gramatica: Gramatica):
        self.g = gramatica
        # Regla 0: Gramática aumentada (S' -> S)
        self.simbolo_aumentado = f"{self.g.simbolo_inicial}'"
        self.reglas = [(self.simbolo_aumentado, [self.g.simbolo_inicial])] + self.g.reglas

        self.estados = []       # Lista de frozenset de ítems (i, j) -> S0, S1, ...
        self.transiciones = {}  # Dict: (id_estado, simbolo) -> id_estado_destino
        self.columnas_accion = self.g.terminales + [Gramatica.FIN]
        self.columnas_ira = self.g.no_terminales
        self.tabla = {}         # Dict: id_estado -> {simbolo: accion}
        self.conflictos = []

        self._construir_automata()
        self._construir_tabla()

    def _simbolo_despues_punto(self, item):
        i, j = item
        _, der = self.reglas[i]
        if der == [Gramatica.EPSILON]:
            return None
        if j < len(der):
            return der[j]
        return None

    def cerradura(self, items_iniciales):
        """Cerradura(I) usando una cola Q, igual que en el pseudocódigo."""
        resultado = set(items_iniciales)
        cola = deque(items_iniciales)

        while cola:
            item_actual = cola.popleft()
            simb = self._simbolo_despues_punto(item_actual)

            if simb in self.g.no_terminales:
                for idx_regla, (izq, _) in enumerate(self.reglas):
                    if izq == simb:
                        nuevo_item = (idx_regla, 0)
                        if nuevo_item not in resultado:
                            resultado.add(nuevo_item)
                            cola.append(nuevo_item)

        return frozenset(resultado)

    def mover(self, conjunto_items, simbolo):
        """Mover(I, X): avanza el punto en los ítems donde siga 'simbolo'."""
        resultado = set()
        for i, j in conjunto_items:
            if self._simbolo_despues_punto((i, j)) == simbolo:
                resultado.add((i, j + 1))
        return resultado

    def ir_a(self, conjunto_items, simbolo):
        """IrA(I, X) = Cerradura(Mover(I, X))."""
        movidos = self.mover(conjunto_items, simbolo)
        if not movidos:
            return frozenset()
        return self.cerradura(movidos)

    def _construir_automata(self):
        # S0 = Cerradura({(0, 0)})
        s0 = self.cerradura({(0, 0)})
        self.estados.append(s0)
        cola_estados = deque([0])
        todos_simbolos = self.g.terminales + self.g.no_terminales

        while cola_estados:
            id_actual = cola_estados.popleft()
            estado_actual = self.estados[id_actual]

            for simb in todos_simbolos:
                nuevo_estado = self.ir_a(estado_actual, simb)
                if not nuevo_estado:
                    continue

                if nuevo_estado not in self.estados:
                    self.estados.append(nuevo_estado)
                    id_dest = len(self.estados) - 1
                    cola_estados.append(id_dest)
                else:
                    id_dest = self.estados.index(nuevo_estado)

                self.transiciones[(id_actual, simb)] = id_dest

    def _asignar_celda(self, id_estado, col, valor):
        actual = self.tabla[id_estado][col]
        if actual != "" and actual != valor:
            self.conflictos.append(
                f"Conflicto en S{id_estado}, '{col}': ya tenía '{actual}', se intentó poner '{valor}'"
            )
            self.tabla[id_estado][col] = f"{actual}/{valor}"
        else:
            self.tabla[id_estado][col] = valor

    def _construir_tabla(self):
        todas_cols = self.columnas_accion + self.columnas_ira
        for id_edo in range(len(self.estados)):
            self.tabla[id_edo] = {col: "" for col in todas_cols}

        # 1. Desplazamientos (sX) y transiciones IrA (X)
        for (id_orig, simb), id_dest in self.transiciones.items():
            if simb in self.g.terminales:
                self._asignar_celda(id_orig, simb, f"s{id_dest}")
            elif simb in self.g.no_terminales:
                self._asignar_celda(id_orig, simb, str(id_dest))

        # 2. Reducciones (rK) y Aceptar
        for id_edo, conjunto_items in enumerate(self.estados):
            for item in conjunto_items:
                if self._simbolo_despues_punto(item) is None:
                    num_regla, _ = item
                    if num_regla == 0:
                        self._asignar_celda(id_edo, Gramatica.FIN, "Aceptar")
                    else:
                        izq, _ = self.reglas[num_regla]
                        for term in self.g.follow[izq]:
                            self._asignar_celda(id_edo, term, f"r{num_regla}")

    def analizar_cadena(self, cadena_tokens):
        """
        Analiza una cadena de tokens separados por espacio (ej: 'num + num * num').
        Retorna (exito_bool, historial_de_pasos).
        """
        entrada = cadena_tokens.strip().split() + [Gramatica.FIN]
        pila_estados = [0]
        pila_simbolos = [Gramatica.FIN]
        idx = 0
        historial = []

        while True:
            estado_actual = pila_estados[-1]
            token_actual = entrada[idx]

            pila_str = " ".join(f"{s}({e})" for s, e in zip(pila_simbolos, pila_estados))
            entrada_str = " ".join(entrada[idx:])
            accion = self.tabla.get(estado_actual, {}).get(token_actual, "")

            if accion == "Aceptar":
                historial.append((pila_str, entrada_str, "Aceptar"))
                return True, historial

            elif accion.startswith("s") and "/" not in accion:
                sig_estado = int(accion[1:])
                historial.append((pila_str, entrada_str, f"Desplazar {accion}"))
                pila_simbolos.append(token_actual)
                pila_estados.append(sig_estado)
                idx += 1

            elif accion.startswith("r") and "/" not in accion:
                num_regla = int(accion[1:])
                izq, der = self.reglas[num_regla]
                regla_str = f"Reducir {accion}: {izq} -> {' '.join(der)}"
                historial.append((pila_str, entrada_str, regla_str))

                # Sacar tantos elementos como símbolos tenga el lado derecho (si no es epsilon)
                if der != [Gramatica.EPSILON]:
                    for _ in range(len(der)):
                        pila_simbolos.pop()
                        pila_estados.pop()

                estado_previo = pila_estados[-1]
                ira = self.tabla[estado_previo].get(izq, "")
                if not ira.isdigit():
                    historial.append((pila_str, entrada_str, f"ERROR IrA({estado_previo}, {izq})"))
                    return False, historial

                pila_simbolos.append(izq)
                pila_estados.append(int(ira))

            else:
                motivo = "CONFLICTO" if "/" in accion else "ERROR"
                historial.append((pila_str, entrada_str, f"{motivo} en S{estado_actual} con '{token_actual}'"))
                return False, historial
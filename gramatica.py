class Gramatica:
    EPSILON = "ε"
    FIN = "$"

    def __init__(self, texto_gramatica):
        self.reglas = []
        self.no_terminales = []
        self.terminales = []
        self.simbolo_inicial = None
        self.first = {}
        self.follow = {}

        self._parsear(texto_gramatica)
        self.calcular_first()
        self.calcular_follow()

        self.tokens = {t: (i + 1) * 10 for i, t in enumerate(self.terminales)}
        self.tokens[self.FIN] = 0

    def _parsear(self, texto):
        lineas = [l.strip() for l in texto.strip().splitlines() if l.strip()]

        for linea in lineas:
            if "->" not in linea:
                continue
            izq, der_completo = linea.split("->", 1)
            izq = izq.strip()

            if self.simbolo_inicial is None:
                self.simbolo_inicial = izq
            if izq not in self.no_terminales:
                self.no_terminales.append(izq)

            alternativas = [alt.strip() for alt in der_completo.split("|")]
            for alt in alternativas:
                if alt in ("ε", "epsilon", "EPSILON", "e", ""):
                    simbolos = [self.EPSILON]
                else:
                    simbolos = alt.split()
                self.reglas.append((izq, simbolos))

        for _, der in self.reglas:
            for simb in der:
                if simb != self.EPSILON and simb not in self.no_terminales:
                    if simb not in self.terminales:
                        self.terminales.append(simb)


    def calcular_first(self):
        for t in self.terminales:
            self.first[t] = {t}
        self.first[self.EPSILON] = {self.EPSILON}
        for nt in self.no_terminales:
            self.first[nt] = set()

        cambio = True
        while cambio:
            cambio = False
            for izq, der in self.reglas:
                antes = len(self.first[izq])
                first_der = self.first_secuencia(der)
                self.first[izq].update(first_der)
                if len(self.first[izq]) > antes:
                    cambio = True

    def first_secuencia(self, secuencia):
        resultado = set()
        if not secuencia or secuencia == [self.EPSILON]:
            resultado.add(self.EPSILON)
            return resultado

        todos_tienen_epsilon = True
        for simb in secuencia:
            first_s = self.first.get(simb, {simb})
            resultado.update(first_s - {self.EPSILON})
            if self.EPSILON not in first_s:
                todos_tienen_epsilon = False
                break

        if todos_tienen_epsilon:
            resultado.add(self.EPSILON)
        return resultado

    def calcular_follow(self):
        for nt in self.no_terminales:
            self.follow[nt] = set()
        self.follow[self.simbolo_inicial].add(self.FIN)

        cambio = True
        while cambio:
            cambio = False
            for izq, der in self.reglas:
                for i, simb in enumerate(der):
                    if simb in self.no_terminales:
                        antes = len(self.follow[simb])
                        beta = der[i + 1:]

                        if beta:
                            first_beta = self.first_secuencia(beta)
                            self.follow[simb].update(first_beta - {self.EPSILON})
                            if self.EPSILON in first_beta:
                                self.follow[simb].update(self.follow[izq])
                        else:
                            self.follow[simb].update(self.follow[izq])

                        if len(self.follow[simb]) > antes:
                            cambio = True
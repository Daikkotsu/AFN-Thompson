class EstadoAnalizLexico:

    def __init__(self, ind_carac_actual = 0, ind_ini_lexema = 0, ind_fin_lexema = -1, paso_por_edo_acep = False, token = -1, lexema = ""):
        self.IndCaracActual = ind_carac_actual
        self.IndIniLexema = ind_ini_lexema
        self.IndFinLexema = ind_fin_lexema
        self.PasoPorEdoAcep = paso_por_edo_acep
        self.token = token
        self.lexema = lexema

    def clonar(self):
        return EstadoAnalizLexico(
            self.IndCaracActual,
            self.IndIniLexema,
            self.IndFinLexema,
            self.PasoPorEdoAcep,
            self.token,
            self.lexema
        )

class AnalizLexico:

    FIN = 0
    ERROR = 20000
    OMITIR = 20001

    def __init__(self, afd=None, sigma=""):
        self.afd = afd
        self.cadena = sigma
        self.pila_estados = []

        self.estado = EstadoAnalizLexico()
        self.set_sigma(sigma)

    def set_sigma(self, sigma):

        self.cadena = sigma
        self.estado = EstadoAnalizLexico()
        self.pila_estados.clear()

    def get_edo_analiz_lexico(self):
        return self.estado.clonar()

    def set_edo_analiz_lexico(self, nuevo_estado):
        self.estado = nuevo_estado.clonar()

    def undo_token(self):

        if not self.pila_estados:
            return False
        self.estado = self.pila_estados.pop()
        return True

    def yylex(self):
        self.pila_estados.append(self.get_edo_analiz_lexico())

        self.estado.IndIniLexema = self.estado.IndCaracActual
        self.estado.IndFinLexema = -1
        self.estado.PasoPorEdoAcep = False
        self.estado.token = -1
        self.estado.lexema = ""

        if self.estado.IndCaracActual >= len(self.cadena):
            return self.FIN

        estado_afd_actual = self.afd.edo_ini
        
        # Validar si el S0 ya es de aceptación desde el inicio
        if estado_afd_actual.token != -1:
            self.estado.PasoPorEdoAcep = True
            self.estado.token = estado_afd_actual.token
            self.estado.IndFinLexema = self.estado.IndCaracActual

        while self.estado.IndCaracActual < len(self.cadena):
            c = self.cadena[self.estado.IndCaracActual]
            
            transicion = estado_afd_actual.transiciones.get(c)
            if transicion is None:
                break

            estado_afd_actual = transicion
            self.estado.IndCaracActual += 1

            if estado_afd_actual.token != -1:
                self.estado.PasoPorEdoAcep = True
                self.estado.token = estado_afd_actual.token
                self.estado.IndFinLexema = self.estado.IndCaracActual

        if self.estado.PasoPorEdoAcep:
            self.estado.IndCaracActual = self.estado.IndFinLexema
            self.estado.lexema = self.cadena[self.estado.IndIniLexema : self.estado.IndFinLexema]
            
            # PARCHE ANTI-CICLOS: Si el lexema está vacío, fuerza a avanzar 1 char
            if len(self.estado.lexema) == 0:
                self.estado.IndCaracActual += 1
                self.estado.lexema = self.cadena[self.estado.IndIniLexema : self.estado.IndCaracActual]
                
            return self.estado.token
        else:
            self.estado.IndCaracActual = self.estado.IndIniLexema + 1
            self.estado.lexema = self.cadena[self.estado.IndIniLexema : self.estado.IndCaracActual]
            self.estado.token = self.ERROR
            return self.ERROR
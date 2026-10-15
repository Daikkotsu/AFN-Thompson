from analiz_lexico import AnalizLexico

class EvaluadorExpr:
    def __init__(self, analizador_lexico):
        self.lexic = analizador_lexico

    def analizar_y_evaluar(self):

        v = 0.0
        post = ""

        exito, v, post = self.E(v, post)

        if exito:
            token = self.lexic.yylex()
            if token == AnalizLexico.FIN:
                return True, v, post

        return False, None, None

    def E(self, v, post):
        exito, v, post = self.T(v, post)
        if exito:
            exito, v, post = self.Ep(v, post)
            if exito:
                return True, v, post
        return False, v, post

    def Ep(self, v, post):
        token = self.lexic.yylex()

        if token == 10 or token == 20:
            v2 = 0.0
            post2 = ""
            exito, v2, post2 = self.T(v2, post2)

            if exito:
                if token == 10:
                    v = v + v2
                    post = post + " " + post2 + " +"
                else:
                    v = v - v2
                    post = post + " " + post2 +" -"

                exito, v, post = self.Ep(v, post)
                if exito:
                    return True, v, post
            return False, v, post

        self.lexic.undo_token()
        return True, v, post

    def T(self, v, post):
        exito, v, post = self.F(v, post)
        if exito:
            exito, v, post = self.Tp(v, post)
            if exito:
                return True, v, post
        return False, v, post

    def Tp(self, v, post):
        token = self.lexic.yylex()
        
        if token == 30 or token == 40:  # * o /
            v2 = 0.0
            post2 = ""
            exito, v2, post2 = self.F(v2, post2)
            
            if exito:
                if token == 30:
                    v = v * v2
                    post = post + " " + post2 + " *"
                else:
                    v = v / v2
                    post = post + " " + post2 + " /"
                    
                # Llamada recursiva Tp()
                exito, v, post = self.Tp(v, post)
                if exito:
                    return True, v, post
            return False, v, post
            
        # Si no es * o /, deshacemos el token (epsilon)
        self.lexic.undo_token()
        return True, v, post

    def F(self, v, post):
        token = self.lexic.yylex()
        
        if token == 50:  # Parentesis Izquierdo '('
            exito, v, post = self.E(v, post)
            if exito:
                token = self.lexic.yylex()
                if token == 60:  # Parentesis Derecho ')'
                    return True, v, post
                    
        elif token == 70:  # Numero
            # Acciones semánticas para la hoja NUM
            v = float(self.lexic.estado.lexema)
            post = self.lexic.estado.lexema
            return True, v, post
            
        return False, v, post
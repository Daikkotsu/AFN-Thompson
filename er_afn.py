from afn import AFN
from analiz_lexico import AnalizLexico

class ER_AFN:
    contador_tmp = 0  # Contador estático para generar IDs únicos

    def __init__(self, analizador_lexico):
        self.lexic = analizador_lexico

    def generar_id(self):
        ER_AFN.contador_tmp += 1
        return f"TMP_ER_{ER_AFN.contador_tmp}"

    def convertir(self, id_afn_resultante="ER_RESULTADO"):
        exito, f = self.E(None)
        
        if exito:
            token = self.lexic.yylex()
            if token == AnalizLexico.FIN:
                if f.id_afn in AFN.afns_creados:
                    del AFN.afns_creados[f.id_afn]
                
                f.id_afn = id_afn_resultante
                AFN.afns_creados[id_afn_resultante] = f
                return True, f
                
        return False, None

    def E(self, f):
        exito, f = self.T(f)
        if exito:
            exito, f = self.Ep(f)
            if exito:
                return True, f
        return False, f

    def Ep(self, f):
        token = self.lexic.yylex()
        
        if token == 10:  # Unión '|'
            f2 = None
            exito, f2 = self.T(f2)
            if exito:
                f.unir(f2, self.generar_id())
                exito, f = self.Ep(f)
                if exito:
                    return True, f
            return False, f
            
        self.lexic.undo_token()
        return True, f

    def T(self, f):
        exito, f = self.C(f)
        if exito:
            exito, f = self.Tp(f)
            if exito:
                return True, f
        return False, f

    def Tp(self, f):
        token = self.lexic.yylex()
        
        # Concatenación implícita
        if token == 80 or token == 60:
            self.lexic.undo_token()
            f2 = None
            exito, f2 = self.C(f2)
            
            if exito:
                f.concatenar(f2, self.generar_id())
                exito, f = self.Tp(f)
                if exito:
                    return True, f
            return False, f
            
        self.lexic.undo_token()
        return True, f

    def C(self, f):
        exito, f = self.F(f)
        if exito:
            exito, f = self.Cp(f)
            if exito:
                return True, f
        return False, f

    def Cp(self, f):
        token = self.lexic.yylex()
        
        if token == 30:  # Kleene '*'
            f.cerradura_kleene(self.generar_id())
            exito, f = self.Cp(f)
            return exito, f
            
        elif token == 40:  # Positiva '+'
            f.cerradura_pos(self.generar_id())
            exito, f = self.Cp(f)
            return exito, f
            
        elif token == 50:  # Opcional '?'
            f.opcional(self.generar_id())
            exito, f = self.Cp(f)
            return exito, f
            
        self.lexic.undo_token()
        return True, f

    def F(self, f):
        token = self.lexic.yylex()
        
        if token == 60:  # '('
            exito, f = self.E(f)
            if exito:
                token = self.lexic.yylex()
                if token == 70:  # ')'
                    return True, f
            return False, f
            
        elif token == 80:  # SIMBOLO
            f = AFN().crear_basico(self.lexic.estado.lexema, id_afn=self.generar_id())
            return True, f
            
        return False, f
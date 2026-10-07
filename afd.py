from afn import AFN 

class EstadoAFD:
    def __init__(self, id_edo, edos_afn):
        self.id_edo = id_edo 
        self.edos_afn = edos_afn
        self.transiciones = {}
        self.token = -1

    def __repr__(self):
        return f"EstadoAFD({self.id_edo})"

class AFD:
    def __init__(self, id_afd=None):
        self.id_afd = id_afd
        self.estados = []
        self.edo_ini = None
        self.alfabeto = set()

    def convertir_afn(self, afn):

        self.alfabeto = afn.alfabeto.copy()
        if afn.EPSILON in self.alfabeto:
            self.alfabeto.remove(afn.EPSILON)

        num_conj_sj = 0
        conj_sj_sin_analizar = []

        edos_s0 = afn.cerradura_epsilon(afn.edo_ini)

        s0 = EstadoAFD(num_conj_sj, edos_s0)
        num_conj_sj += 1

        conj_sj_sin_analizar.append(s0)
        self.estados.append(s0)
        self.edo_ini = s0

        while conj_sj_sin_analizar:
            sj_aux = conj_sj_sin_analizar.pop(0)

            for simbolo in self.alfabeto:

                sj_temp_edos = afn.ir_a(sj_aux.edos_afn, simbolo)

                if not sj_temp_edos:
                    continue

                estado_existente = self.buscar_sj(sj_temp_edos)

                if estado_existente is None:

                    nuevo_estado = EstadoAFD(num_conj_sj, sj_temp_edos)
                    num_conj_sj += 1

                    self.estados.append(nuevo_estado)
                    conj_sj_sin_analizar.append(nuevo_estado)

                    sj_aux.transiciones[simbolo] = nuevo_estado
                else:

                    sj_aux.transiciones[simbolo] = estado_existente

        self.evaluar_estados_aceptacion(afn)
        return self

    def buscar_sj(self, edos_afn):

        ids_buscar = {e.id_edo for e in edos_afn}

        for estado_afd in self.estados:
            ids_actual = {e.id_edo for e in estado_afd.edos_afn}
            if ids_buscar == ids_actual:
                return estado_afd

        return None

    def evaluar_estados_aceptacion(self, afn):

        for estado_afd in self.estados:

            interseccion = estado_afd.edos_afn.intersection(afn.edos_acept)

            count = len(interseccion)

            if count == 0:
                estado_afd.token = -1
            elif count == 1:
                estado_aceptacion = list(interseccion)[0]
                estado_afd.token = estado_aceptacion.token
            else:
                print(f"--> AMBIGÜEDAD DETECTADA en el estado AFD {estado_afd.id_edo}")
                estado_afd.token = list(interseccion)[0].token

    def imprimir_tabla(self):
        print(f"\n--- Tabla AFD (ID: {self.id_afd}) ---")
        alfabeto_ordenado = sorted(list(self.alfabeto))

        encabezados = ["Edo"] + alfabeto_ordenado + ["Token"]
        print("\t".join(encabezados))

        for estado in self.estados:
            fila = [str(estado.id_edo)]
            for sim in alfabeto_ordenado:

                destino = estado.transiciones.get(sim)
                if destino:
                    fila.append(str(destino.id_edo))
                else:
                    fila.append("-1")

            fila.append(str(estado.token))
            print("\t".join(fila))
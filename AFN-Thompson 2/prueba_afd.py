from afn import AFN
from afd import AFD


afn_a = AFN().crear_basico("a", id_afn="A")

afn_kleene = afn_a.cerradura_kleene("A_KLEENE")
afn_a.edos_acept.copy().pop().token = 10


afn_kleene.ver_afn()


print("\nIniciando conversión a AFD...")
mi_afd = AFD(id_afd="AFD_A_KLEENE")
mi_afd.convertir_afn(afn_kleene)


mi_afd.imprimir_tabla()

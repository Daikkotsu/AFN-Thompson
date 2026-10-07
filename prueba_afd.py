from afn import AFN
from afd import AFD

# 1. Vamos a crear un AFN básico para la letra "a" y luego la cerradura de Kleene "a*"
afn_a = AFN().crear_basico("a", id_afn="A")

afn_kleene = afn_a.cerradura_kleene("A_KLEENE")
afn_a.edos_acept.copy().pop().token = 10  # Le damos un token de prueba

# Si gustas, imprimimos el AFN para recordar cómo quedó
afn_kleene.ver_afn()

# 2. Convertimos a AFD
print("\nIniciando conversión a AFD...")
mi_afd = AFD(id_afd="AFD_A_KLEENE")
mi_afd.convertir_afn(afn_kleene)

# 3. Imprimimos la tabla
mi_afd.imprimir_tabla()
from afn import AFN
from afd import AFD

print("--- CREANDO TOKENS INDIVIDUALES ---")

# 1. Creamos AFNs básicos y les asignamos el Token (Usaré la numeración de tu contexto)
afn_suma = AFN().crear_basico("+", id_afn="SUMA")
afn_suma.asignar_token(10)

afn_resta = AFN().crear_basico("-", id_afn="RESTA")
afn_resta.asignar_token(20)

afn_mult = AFN().crear_basico("*", id_afn="MULT")
afn_mult.asignar_token(30)

# Simulemos un número MUY simplificado: un solo dígito (0-9)
afn_num = AFN().crear_basico("0", "9", id_afn="NUM")
afn_num.asignar_token(70)

print("Tokens creados con éxito.")

# 2. Aplicamos la Unión Especial Léxica
print("\n--- GENERANDO AFN COMBINADO LÉXICO ---")
afn_lexico = AFN.union_especial_lexica("LEXICO", ["SUMA", "RESTA", "MULT", "NUM"])
print(f"Estados del AFN Léxico: {len(afn_lexico.edos_afn)}")
print(f"Estados de Aceptación: {[e.id_edo for e in afn_lexico.edos_acept]}")

# 3. Convertimos a AFD
print("\n--- CONVIRTIENDO A AFD ---")
mi_afd = AFD(id_afd="AFD_LEXICO")
mi_afd.convertir_afn(afn_lexico)

# 4. Imprimimos la tabla resultante
mi_afd.imprimir_tabla()
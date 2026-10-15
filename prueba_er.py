from afn import AFN
from afd import AFD
from analiz_lexico import AnalizLexico
from er_afn import ER_AFN

print("--- 1. CONSTRUYENDO TOKENS DE REGEX ---")
AFN().crear_basico("|", id_afn="OR").asignar_token(10)
AFN().crear_basico("*", id_afn="KLEENE").asignar_token(30)
AFN().crear_basico("+", id_afn="POS").asignar_token(40)
AFN().crear_basico("?", id_afn="OPC").asignar_token(50)
AFN().crear_basico("(", id_afn="PAR_I").asignar_token(60)
AFN().crear_basico(")", id_afn="PAR_D").asignar_token(70)

# Un Símbolo (Token 80) puede ser cualquier letra de la 'a' a la 'z'
AFN().crear_basico("a", "z", "LETRAS").asignar_token(80)

afn_lex = AFN.union_especial_lexica("LEX_REGEX", ["OR", "KLEENE", "POS", "OPC", "PAR_I", "PAR_D", "LETRAS"])
afd_regex = AFD("AFD_REGEX").convertir_afn(afn_lex)

cadena_regex = "(a|b)*c+"
print(f"--- 2. CONVIRTIENDO EXPRESIÓN REGULAR: {cadena_regex} ---")

analizador = AnalizLexico(afd_regex, cadena_regex)
traductor_regex = ER_AFN(analizador)

exito, afn_final = traductor_regex.convertir("MI_SUPER_AFN")

if exito:
    print("\n¡Expresión Regular convertida exitosamente a AFN!")
    print(f"ID del AFN generado: {afn_final.id_afn}")
    print(f"Total de Estados del AFN: {len(afn_final.edos_afn)}")
    afn_final.ver_afn()
else:
    print("Error de sintaxis en la expresión regular.")
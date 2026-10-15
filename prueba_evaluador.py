from afn import AFN
from afd import AFD
from analiz_lexico import AnalizLexico
from evaluador_expr import EvaluadorExpr

print("--- 1. CONSTRUYENDO TOKENS DEL EVALUADOR ---")
AFN().crear_basico("+", id_afn="SUMA").asignar_token(10)
AFN().crear_basico("-", id_afn="RESTA").asignar_token(20)
AFN().crear_basico("*", id_afn="MULT").asignar_token(30)
AFN().crear_basico("/", id_afn="DIV").asignar_token(40)
AFN().crear_basico("(", id_afn="PAR_I").asignar_token(50)
AFN().crear_basico(")", id_afn="PAR_D").asignar_token(60)

# Construimos los digitos para el token 70
afn_num = AFN().crear_basico("0", "9", "DIGITOS").cerradura_pos("NUM").asignar_token(70)

print("--- 2. CREANDO ANALIZADOR LÉXICO ---")
afn_lex = AFN.union_especial_lexica("LEX_MAT", ["SUMA", "RESTA", "MULT", "DIV", "PAR_I", "PAR_D", "NUM"])
afd_mat = AFD("AFD_MAT").convertir_afn(afn_lex)

# La cadena exacta de la imagen del profesor
cadena = "2+8*(3+2)"
analizador_lexico = AnalizLexico(afd_mat, cadena)

print(f"\n--- 3. EVALUANDO EXPRESIÓN: {cadena} ---")
evaluador = EvaluadorExpr(analizador_lexico)

exito, resultado, postfijo = evaluador.analizar_y_evaluar()

if exito:
    print("¡Análisis Sintáctico Exitoso!")
    print(f"Resultado Matemático: {resultado}")
    print(f"Notación Postfija: {postfijo.strip()}")
else:
    print("Error de Sintaxis.")
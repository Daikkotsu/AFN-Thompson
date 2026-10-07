from afn import AFN
from afd import AFD
from analiz_lexico import AnalizLexico

# 1. Creamos la expresión regular para Números: [0-9]+
# Primero rango básico, luego cerradura positiva
afn_digito = AFN().crear_basico("0", "9", "DIGITO")
afn_nums = afn_digito.cerradura_pos("NUMS")
afn_nums.asignar_token(70)

# 2. Operadores simples
afn_suma = AFN().crear_basico("+", id_afn="SUMA").asignar_token(10)
afn_resta = AFN().crear_basico("-", id_afn="RESTA").asignar_token(20)

# 3. AFN Combinado y AFD
afn_lexico = AFN.union_especial_lexica("LEX", ["NUMS", "SUMA", "RESTA"])
afd_lexico = AFD("AFD_LEX").convertir_afn(afn_lexico)

# 4. PRUEBA DEL ANALIZADOR LÉXICO
cadena_prueba = "123+45-6"
print(f"Analizando cadena: '{cadena_prueba}'\n")

analizador = AnalizLexico(afd=afd_lexico, sigma=cadena_prueba)

# Leemos un par de tokens
t1 = analizador.yylex()
print(f"Token: {t1}, Lexema: '{analizador.estado.lexema}'")

t2 = analizador.yylex()
print(f"Token: {t2}, Lexema: '{analizador.estado.lexema}'")

# Hacemos UNDO para demostrar que puede retroceder
print("\n--- EJECUTANDO UNDO TOKEN ---")
analizador.undo_token()
print("Se deshizo el último token leído.\n")

# Continuamos leyendo hasta el final
while True:
    token = analizador.yylex()
    if token == AnalizLexico.FIN:
        print("-> FIN DE CADENA ALCANZADO")
        break
    
    # En la vida real aquí manejaríamos el ERROR, pero para la prueba lo mostramos
    print(f"Token: {token}, Lexema: '{analizador.estado.lexema}'")
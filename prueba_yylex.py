from afn import AFN
from afd import AFD
from analiz_lexico import AnalizLexico

# 1. Asegúrate de que aquí diga "0" y "9"
afn_digito = AFN().crear_basico("0", "9", "DIGITO")
afn_nums = afn_digito.cerradura_pos("NUMS").asignar_token(70)

afn_suma = AFN().crear_basico("+", id_afn="SUMA").asignar_token(10)
afn_resta = AFN().crear_basico("-", id_afn="RESTA").asignar_token(20)

afn_lexico = AFN.union_especial_lexica("LEX", ["NUMS", "SUMA", "RESTA"])
afd_lexico = AFD("AFD_LEX").convertir_afn(afn_lexico)

cadena_prueba = "123+45-6"
analizador = AnalizLexico(afd=afd_lexico, sigma=cadena_prueba)

print(f"--- INICIANDO LECTURA DE: {cadena_prueba} ---")

t1 = analizador.yylex()
print(f"T1 -> Token: {t1}, Lexema: '{analizador.estado.lexema}'")

t2 = analizador.yylex()
print(f"T2 -> Token: {t2}, Lexema: '{analizador.estado.lexema}'")

print("\n--- HACIENDO UNDO ---")
analizador.undo_token()

print("\n--- LEYENDO HASTA EL FIN ---")
seguro = 0
while seguro < 20: # Límite de 20 vueltas para que no te trabe la PC
    token = analizador.yylex()
    if token == AnalizLexico.FIN:
        print("-> FIN DE CADENA ALCANZADO")
        break
    print(f"Token: {token}, Lexema: '{analizador.estado.lexema}'")
    seguro += 1
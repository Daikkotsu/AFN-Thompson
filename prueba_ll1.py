from gramatica import Gramatica
from ll1 import AnalizadorLL1

texto_g = """
E  -> T Ep
Ep -> + T Ep | - T Ep | ε
T  -> F Tp
Tp -> * F Tp | / F Tp | ε
F  -> ( E ) | num
"""

g = Gramatica(texto_g)
ll1 = AnalizadorLL1(g)

print("=== FIRST ===")
for nt in g.no_terminales:
    print(f"First({nt}) = {g.first[nt]}")

print("\n=== FOLLOW ===")
for nt in g.no_terminales:
    print(f"Follow({nt}) = {g.follow[nt]}")

print("\n=== TABLA LL(1) ===")
encabezado = f"{'':<6}" + "".join(f"{c:<8}" for c in ll1.columnas)
print(encabezado)
print("-" * len(encabezado))
for f in ll1.filas:
    fila_str = f"{f:<6}" + "".join(f"{ll1.tabla[f][c]:<8}" for c in ll1.columnas)
    print(fila_str)

print("\n=== ANÁLISIS DE CADENA ===")
exito, pasos = ll1.analizar_cadena("num + num * ( num + num )")
for pila, ent, acc in pasos:
    print(f"Pila: {pila:<25} | Entrada: {ent:<28} | Acción: {acc}")
print("\nResultado:", "ACEPTADA" if exito else "RECHAZADA")
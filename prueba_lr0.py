from gramatica import Gramatica
from lr0 import AnalizadorLR0

texto_g = """
E -> E + T | E - T | T
T -> T * F | T / F | F
F -> ( E ) | num
"""

g = Gramatica(texto_g)
lr0 = AnalizadorLR0(g)

print(f"Total de estados generados: {len(lr0.estados)}")
if lr0.conflictos:
    print("Conflictos:", lr0.conflictos)

print("\n=== TABLA LR(0) ===")
cols = lr0.columnas_accion + lr0.columnas_ira
encabezado = f"{'Edo':<6}" + "".join(f"{c:<8}" for c in cols)
print(encabezado)
print("-" * len(encabezado))
for edo in range(len(lr0.estados)):
    fila = f"S{edo:<5}" + "".join(f"{lr0.tabla[edo][c]:<8}" for c in cols)
    print(fila)

print("\n=== ANÁLISIS DE CADENA ===")
exito, pasos = lr0.analizar_cadena("num + num * ( num + num )")
for pila, ent, acc in pasos:
    print(f"Pila: {pila:<38} | Entrada: {ent:<26} | {acc}")
print("\nResultado:", "ACEPTADA" if exito else "RECHAZADA")
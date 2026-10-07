from afn import Estado, Transicion, AFN

# 1. Recreamos el escenario de prueba:
# q0 --ε--> q1
# q1 --ε--> q2
# q2 --a--> q3

q0 = Estado()
q1 = Estado()
q2 = Estado()
q3 = Estado()

# Forzamos los IDs para que la salida en consola sea fácil de leer (opcional, solo para la prueba)
q0.id_edo = 0
q1.id_edo = 1
q2.id_edo = 2
q3.id_edo = 3

q0.transiciones.append(Transicion(AFN.EPSILON, q1))
q1.transiciones.append(Transicion(AFN.EPSILON, q2))
q2.transiciones.append(Transicion("a", q3))

# Instanciamos un AFN dummy solo para usar sus métodos
afn_prueba = AFN("Prueba")

print("--- PRUEBA DE OPERACIONES BASE PARA AFD ---")

# Prueba de Cerradura Epsilon
# Esperamos: {0, 1, 2}
cerradura = afn_prueba.cerradura_epsilon(q0)
print(f"CerraduraEpsilon(q0): {[e.id_edo for e in cerradura]}")

# Prueba de Mover
# Esperamos: {3}
movimiento = afn_prueba.mover(cerradura, "a")
print(f"Mover(CerraduraEpsilon(q0), 'a'): {[e.id_edo for e in movimiento]}")

# Prueba de IrA
# Esperamos: {3} (La cerradura epsilon de q3 es solo q3, porque no tiene salidas epsilon)
conjunto_ira = afn_prueba.ir_a(cerradura, "a")
print(f"IrA(CerraduraEpsilon(q0), 'a'): {[e.id_edo for e in conjunto_ira]}")
from afn import Estado, Transicion, AFN






q0 = Estado()
q1 = Estado()
q2 = Estado()
q3 = Estado()


q0.id_edo = 0
q1.id_edo = 1
q2.id_edo = 2
q3.id_edo = 3

q0.transiciones.append(Transicion(AFN.EPSILON, q1))
q1.transiciones.append(Transicion(AFN.EPSILON, q2))
q2.transiciones.append(Transicion("a", q3))


afn_prueba = AFN()

print("--- PRUEBA DE OPERACIONES BASE PARA AFD ---")



cerradura = afn_prueba.cerradura_epsilon(q0)
print(f"CerraduraEpsilon(q0): {[e.id_edo for e in cerradura]}")



movimiento = afn_prueba.mover(cerradura, "a")
print(f"Mover(CerraduraEpsilon(q0), 'a'): {[e.id_edo for e in movimiento]}")



conjunto_ira = afn_prueba.ir_a(cerradura, "a")
print(f"IrA(CerraduraEpsilon(q0), 'a'): {[e.id_edo for e in conjunto_ira]}")

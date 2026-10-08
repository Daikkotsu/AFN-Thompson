import tkinter as tk
from tkinter import messagebox, ttk
import math

from afn import AFN

class InterfazThompson:

    def __init__(self):
        self.ventana = tk.Tk()

        self.ventana.title("Metodo de Thompson")
        self.ventana.geometry("500x500")

        self.crear_menu_principal()

    def crear_menu_principal(self):

        titulo = tk.Label(
            self.ventana,
            text="Metodo de Thompson",
            font=("Arial", 20, "bold")
        )

        titulo.pack(pady=25)

        boton_basico = tk.Button(
            self.ventana,
            text="Crear AFN basico",
            width=25,
            command=self.ventana_crear_basico
        )

        boton_basico.pack(pady=5)

        boton_union = tk.Button(
            self.ventana,
            text="Unir AFN",
            width=25,
            command=self.ventana_unir_afn
        )

        boton_union.pack(pady=5)

        boton_concatenar = tk.Button(
            self.ventana,
            text="Concatenar AFN",
            width=25,
            command=self.ventana_concatenar_afn
        )

        boton_concatenar.pack(pady=5)

        boton_pos = tk.Button(
            self.ventana,
            text="Cerradura positiva (+)",
            width=25,
            command=self.ventana_cerradura_pos
        )

        boton_pos.pack(pady=5)

        boton_kleene = tk.Button(
            self.ventana,
            text="Cerradura de Kleene (*)",
            width=25,
            command=self.ventana_cerradura_kleene
        )

        boton_kleene.pack(pady=5)

        boton_opcional = tk.Button(
            self.ventana,
            text="opcional (?)",
            width=25,
            command=self.ventana_opcional
        )

        boton_opcional.pack(pady=5)

        boton_ver = tk.Button(
            self.ventana,
            text="Ver AFN",
            width=25,
            command=self.ventana_ver_afn
        )

        boton_ver.pack(pady=5)

        boton_modulo_lexico = tk.Button(
            self.ventana,
            text="Analizador Léxico (AFN -> AFD)",
            width=30,
            command=self.ventana_modulo_lexico,
            bg="lightblue"
        )

        boton_modulo_lexico.pack(pady=15)

    def ventana_crear_basico(self):

        ventana = tk.Toplevel(self.ventana)

        ventana.title("Crear AFN basico")
        ventana.geometry("350x300")

        titulo = tk.Label(
            ventana,
            text="Crear AFN basico",
            font=("Arial", 16, "bold")
        )

        titulo.pack(pady=15)

        tk.Label(
            ventana,
            text="Simbolo inferior:"
        ).pack()

        entrada_simb1 = tk.Entry(ventana)
        entrada_simb1.pack(pady=5)

        tk.Label(
            ventana,
            text="Simbolo superior"
        ).pack()

        entrada_simb2 = tk.Entry(ventana)
        entrada_simb2.pack(pady=5)

        tk.Label(
            ventana,
            text="ID del AFN:"
        ).pack()

        entrada_id = tk.Entry(ventana)
        entrada_id.pack(pady=5)

        def crear():

            simb1 = entrada_simb1.get()
            simb2 = entrada_simb2.get()
            id_afn = entrada_id.get()

            try:

                if id_afn == "":
                    raise ValueError(
                        "Debes introducir un ID para el AFN."
                    )

                if simb2 == "":

                    AFN().crear_basico(
                        simb1,
                        id_afn=id_afn
                    )

                else:

                    AFN().crear_basico(
                        simb1,
                        simb2,
                        id_afn
                    )

                messagebox.showinfo(
                    "AFN creado",
                    f"El AFN `{id_afn}` fue creado correctamente."
                )

                ventana.destroy()

            except ValueError as error:

                messagebox.showerror(
                    "Error",
                    str(error)
                )

        boton_crear = tk.Button(
            ventana,
            text="Crear",
            width=15,
            command=crear
        )

        boton_crear.pack(pady=5)

    def ventana_unir_afn(self):

        ids = AFN.obtener_ids()

        if len(ids) < 2:
            messagebox.showwarning(
                "AFN insuficientes",
                "Debes crear al menos dos AFN para realizar una union."
            )
            return

        ventana = tk.Toplevel(self.ventana)

        ventana.title("Unir AFN")
        ventana.geometry("350x300")

        titulo = tk.Label(
            ventana,
            text="Unir AFN",
            font=("Arial", 16, "bold")
        )

        titulo.pack(pady=15)

        # Primer AFN

        tk.Label(
            ventana,
            text="Primer AFN:"
        ).pack()

        selector_afn1 = ttk.Combobox(
            ventana,
            values=ids,
            state="readonly",
            width=25
        )

        selector_afn1.pack(pady=5)
        selector_afn1.current(0)

        # Segundo AFN

        tk.Label(
            ventana,
            text="Segundo AFN:"
        ).pack()

        selector_afn2 = ttk.Combobox(
            ventana, 
            values=ids,
            state="readonly",
            width=25
        )

        selector_afn2.pack(pady=5)

        if len(ids) > 1:
            selector_afn2.current(1)

        # ID del resultado

        tk.Label(
            ventana, 
            text="ID del nuevo AFN:"
        ).pack()

        entrada_id = tk.Entry(
            ventana,
            width=28
        )

        entrada_id.pack(pady=5)

        #Accion

        def unir():

            id1 = selector_afn1.get()
            id2 = selector_afn2.get()
            nuevo_id = entrada_id.get().strip()

            try:

                if id1 == id2:
                    raise ValueError(
                        "Debes seleccionar dos AFN diferentes."
                    )

                if nuevo_id == "":
                    raise ValueError(
                        "Debes introducir un ID para el AFN resultante." 
                    )

                afn1 = AFN.obtener_afn(id1)
                afn2 = AFN.obtener_afn(id2)

                afn1.unir(
                    afn2,
                    nuevo_id
                )

                messagebox.showinfo(
                    "Union realizada",
                    f"El AFN `{nuevo_id}` fue creado correctamente."
                )

                ventana.destroy()

            except ValueError as error:

                messagebox.showerror(
                    "Error",
                    str(error)
                )

        boton_unir = tk.Button(
            ventana,
            text="Unir",
            width=15,
            command=unir
        )

        boton_unir.pack(pady=15)

    def ventana_concatenar_afn(self):

        ids = AFN.obtener_ids()

        if len(ids) < 2:

            messagebox.showwarning(
                "AFN insuficientes",
                "Necesitas al menos dos AFN para concatenar."
            )
            return

        ventana = tk.Toplevel(self.ventana)

        ventana.title("Concatenar AFN")
        ventana.geometry("350x300")

        titulo = tk.Label(
            ventana,
            text="Concatenar AFN",
            font=("Arial", 16, "bold")
        )

        titulo.pack(pady=15)

        tk.Label(
            ventana,
            text="Primer AFN:"
        ).pack()

        selector_afn1 = ttk.Combobox(
            ventana,
            values=ids,
            state="readonly",
            width=25
        )

        selector_afn1.pack(pady=5)
        selector_afn1.current(0)

        tk.Label(
            ventana,
            text="Segundo AFN:"
        ).pack()

        selector_afn2 = ttk.Combobox(
            ventana,
            values=ids,
            state="readonly",
            width=25
        )

        selector_afn2.pack(pady=5)
        selector_afn2.current(1)

        tk.Label(
            ventana,
            text="ID del nuevo AFN:"
        ).pack()

        entrada_id = tk.Entry(
            ventana,
            width=28
        )

        entrada_id.pack(pady=5)

        def concatenar():

            id1 = selector_afn1.get()
            id2 = selector_afn2.get()
            nuevo_id = entrada_id.get().strip()

            try:

                if id1 == id2:
                    raise ValueError(
                        "Debes seleccionar dos AFN diferentes."
                    )

                if nuevo_id == "":
                    raise ValueError(
                        "Debes seleccionar un ID para el AFN resultante."
                    )

                afn1 = AFN.obtener_afn(id1)
                afn2 = AFN.obtener_afn(id2)

                afn1.concatenar(
                    afn2,
                    nuevo_id
                )

                messagebox.showinfo(
                    "Concatenacion realizada",
                    f"El AFN `{nuevo_id}` fue creado correctamente."
                )

                ventana.destroy()

            except ValueError as error:

                messagebox.showerror(
                    "Error",
                    str(error)
                )

        boton_concatenar = tk.Button(
            ventana, 
            text="Concatenar",
            width=15,
            command=concatenar
        )

        boton_concatenar.pack(pady=15)

    def ventana_cerradura_pos(self):

        ids = AFN.obtener_ids()

        if not ids:
            messagebox.showwarning(
                "AFN faltante",
                "Debes crear al menos un AFN"
            )
            return

        ventana = tk.Toplevel(self.ventana)

        ventana.title("Cerradura positiva")
        ventana.geometry("350x250")

        titulo = tk.Label(
            ventana,
            text="Cerradura Positiva (+)",
            font=("Arial", 16, "bold")
        )

        titulo.pack(pady=15)

        tk.Label(
            ventana,
            text="AFN:"
        ).pack()

        selector_afn = ttk.Combobox(
            ventana,
            values=ids,
            state="readonly",
            width=25
        )

        selector_afn.pack(pady=5)
        selector_afn.current(0)

        # Donde mete el nuevo ID del AFN

        tk.Label(
            ventana,
            text="ID del nuevo AFN:"
        ).pack()

        entrada_id = tk.Entry(
            ventana,
            width=28
        )

        entrada_id.pack(pady=5)

        # Cerradura

        def aplicar():

            id_afn = selector_afn.get()
            nuevo_id = entrada_id.get().strip()

            try:

                if nuevo_id == "":
                    raise ValueError(
                        "Debes introducir un ID para el AFN resultante"
                    )

                afn = AFN.obtener_afn(id_afn)

                afn.cerradura_pos(
                    nuevo_id
                )

                messagebox.showinfo(
                    "Cerradura realizada",
                    f"El afn `{nuevo_id}` fue creado correctamente."
                )

                ventana.destroy()

            except ValueError as error:

                messagebox.showerror(
                    "Error",
                    str(error)
                )

        boton_aplicar = tk.Button(
            ventana,
            text="Aplicar",
            width=15,
            command=aplicar
        )

        boton_aplicar.pack(pady=15)

    def ventana_cerradura_kleene(self):

        ids = AFN.obtener_ids()

        if not ids:
            messagebox.showwarning(
                "AFN faltante",
                "Debes crear al menos un AFN."
            )
            return

        ventana = tk.Toplevel(self.ventana)

        ventana.title("Cerradura de Kleene")
        ventana.geometry("350x250")

        titulo = tk.Label(
            ventana,
            text="Cerradura de Kleene (*)",
            font=("Arial", 16, "bold")
        )

        titulo.pack(pady=15)

        # Aqui viene el selector del AFN

        tk.Label(
            ventana,
            text="AFN:"
        ).pack()

        selector_afn = ttk.Combobox(
            ventana, 
            values=ids,
            state="onlyread",
            width=25
        )

        selector_afn.pack(pady=5)
        selector_afn.current(0)

        #Lo de siempreeee, el ID del nuevo afn

        tk.Label(
            ventana,
            text="ID del nuevo AFN:"
        ).pack()

        entrada_id = tk.Entry(
            ventana,
            width=28
        )

        entrada_id.pack(pady=5)

        # Lo mismo x2, aplicar la cerradura

        def aplicar():

            id_afn = selector_afn.get()
            nuevo_id = entrada_id.get().strip()

            try:

                if nuevo_id == "":
                    raise ValueError(
                        "Debes introducir un ID para el AFN resultante."
                    )

                afn = AFN.obtener_afn(id_afn)

                afn.cerradura_kleene(
                    nuevo_id
                )

                messagebox.showinfo(
                    "Cerradura realizada",
                    f"El AFN `{nuevo_id}` fue creado correctamente."
                )

                ventana.destroy()

            except ValueError as error:

                messagebox.showerror(
                    "Error",
                    str(error)
                )

        boton_aplicar = tk.Button(
            ventana,
            text="Aplicar",
            width=15,   
            command=aplicar
        )

        boton_aplicar.pack(pady=15)

    def ventana_opcional(self):

        ids = AFN.obtener_ids()

        if not ids:
            messagebox.showwarning(
                "AFN faltante",
                "Debes crear un AFN."
            )
            return

        ventana = tk.Toplevel(self.ventana)

        ventana.title("Opcional")
        ventana.geometry("350x250")

        titulo = tk.Label(
            ventana,
            text="AFN opcional",
            font=("Arial", 16, "bold")
        )

        titulo.pack(pady=15)

        tk.Label(
            ventana,
            text="AFN:"
        ).pack()

        selector_afn = ttk.Combobox(
            ventana,
            values=ids,
            state="readonly",
            width=25
        )

        selector_afn.pack(pady=5)
        selector_afn.current(0)

        tk.Label(
            ventana,
            text="ID del nuevo AFN:"
        ).pack()

        entrada_id = tk.Entry(
            ventana,
            width=28
        )

        entrada_id.pack(pady=5)

        def aplicar():

            id_afn = selector_afn.get()
            nuevo_id = entrada_id.get().strip()

            try:

                if nuevo_id == "":
                    raise ValueError(
                        "Debe introducir un ID para el AFN resultante."
                    )

                afn = AFN.obtener_afn(id_afn)

                afn.opcional(
                    nuevo_id
                )

                messagebox.showinfo(
                    "Operacion realizada",
                    f"El AFN `{nuevo_id}` fue creado correctamente."
                )

                ventana.destroy()

            except ValueError as error:

                messagebox.showerror(
                    "Error",
                    str(error)
                )

        boton_aplicar = tk.Button(
            ventana,
            text="Aplicar",
            width=15,
            command=aplicar
        )

        boton_aplicar.pack(pady=15)

    def calcular_niveles(self, afn):

        niveles = {afn.edo_ini.id_edo: 0}
        cola = [afn.edo_ini]

        while cola:
            actual = cola.pop(0)
            nivel_actual = niveles[actual.id_edo]

            for transicion in actual.transiciones:
                destino = transicion.edo_dest

                if destino.id_edo not in niveles:
                    niveles[destino.id_edo] = nivel_actual + 1
                    cola.append(destino)

        # Si llegan a haber estados no alcanzados,
        # los pasamos al final
        max_nivel = max(niveles.values(), default=0)

        for estado in sorted(afn.edos_afn, key=lambda e: e.id_edo):
            if estado.id_edo not in niveles:
                max_nivel += 1
                niveles[estado.id_edo] = max_nivel

        # Forzamos los estados de aceptación
        # a aparecer en el último nivel
        niveles_no_finales = [
            nivel
            for id_edo, nivel in niveles.items()
            if all(
                estado.id_edo != id_edo
                for estado in afn.edos_acept
            )
        ]

        max_nivel_no_final = max(
            niveles_no_finales,
            default=0
        )

        for estado in afn.edos_acept:
            niveles[estado.id_edo] = max_nivel_no_final + 1

        return niveles

    def ventana_ver_afn(self):

        # Verificamos que existe al menos un AFN
        ids = AFN.obtener_ids()

        if not ids:
            messagebox.showwarning(
                "Sin AFN",
                "Primero debes crear al menos un AFN"
            )
            return

        ventana = tk.Toplevel(self.ventana)

        ventana.title("Ver AFN")
        ventana.geometry("900x800")

        titulo = tk.Label(
            ventana,
            text="Ver AFN",
            font=("Arial", 16, "bold")
        )

        titulo.pack(pady=15)

        #Aqui implementamos un selector de AFN

        frame_selector = tk.Frame(ventana)
        frame_selector.pack(pady=10)

        tk.Label(
            frame_selector,
            text="AFN:"
        ).pack(side="left", padx=5)

        selector_afn = ttk.Combobox(
            frame_selector,
            values=ids,
            state="readonly",
            width=25
        )

        selector_afn.pack(side="left", padx=5)

        selector_afn.current(0)

        # Diagrama del AFN

        frame_grafo = tk.LabelFrame(
            ventana,
            text="Diagrama del AFN"
        )

        frame_grafo.pack(
            padx=15,
            pady=10,
            fill="both"
        )

        canvas = tk.Canvas(
            frame_grafo,
            width=850,
            height=400
        )

        canvas.pack(
            padx=10,
            pady=10
        )

        # Mostramos la info general

        frame_info = tk.Frame(ventana)
        frame_info.pack(pady=10)

        label_inicial = tk.Label(frame_info, text="")
        label_inicial.pack()

        label_estados = tk.Label(frame_info, text="")
        label_estados.pack()

        label_aceptacion = tk.Label(frame_info, text="")
        label_aceptacion.pack()

        label_alfabeto = tk.Label(frame_info, text="")
        label_alfabeto.pack()


        frame_tabla = tk.Frame(ventana)
        frame_tabla.pack(pady=15)

        tabla = ttk.Treeview(
            frame_tabla,
            columns=("origen", "simbolo", "destino"),
            show="headings",
            height=8
        )

        scroll_y = ttk.Scrollbar(
            frame_tabla,
            orient="vertical",
            command=tabla.yview
        )

        tabla.configure(yscrollcommand=scroll_y.set)

        tabla.heading("origen", text="Estado origen")
        tabla.heading("simbolo", text="Simbolo")
        tabla.heading("destino", text="Estado destino")

        tabla.column(   
            "origen",
            width=150,
            anchor="center"
        )

        tabla.column(
            "simbolo",
            width=150,
            anchor="center"
        )

        tabla.column(
            "destino",
            width=150,
            anchor="center"
        )

        tabla.grid(row=0, column=0)
        scroll_y.grid(row=0, column=1, sticky="ns")

        # Con esta funcion mostraremos el AFN

        def mostrar_afn(event=None):

            id_afn = selector_afn.get()

            afn = AFN.obtener_afn(id_afn)

            if afn is None:
                return
            
            self.dibujar_afn(
                canvas,
                afn
            )

            estados = sorted(
                afn.edos_afn,
                key=lambda e: e.id_edo
            )

            aceptacion = sorted(
                afn.edos_acept,
                key=lambda e: e.id_edo
            )

            label_inicial.config(
                text=f"Estado inicial: {afn.edo_ini.id_edo} "
            )

            label_estados.config(
                text="Estados: " +
                str([e.id_edo for e in estados])
            )

            label_aceptacion.config(
                text="Estados de aceptacion: " +
                str([e.id_edo for e in aceptacion])
            )

            label_alfabeto.config(
                text="Alfabeto: " +
                str(sorted(afn.alfabeto))
            )

            # Este pa limpiar la tabla anterior
            for fila in tabla.get_children():
                tabla.delete(fila)

            for origen, simbolo, destino in afn.obtener_transiciones():

                tabla.insert(
                    "",
                    "end",
                    values=(
                        origen,
                        simbolo,
                        destino
                    )
                )

            # Con este selector se cambia 
            # automaticamente al cambiar de AFN

        selector_afn.bind(
            "<<ComboboxSelected>>",
            mostrar_afn
        )

        mostrar_afn()

    def ventana_modulo_lexico(self):
        ids = AFN.obtener_ids()
        if not ids:
            messagebox.showwarning("Sin AFN", "Primero debes crear AFNs básicos (Ej: + , - , 0-9).")
            return

        ventana = tk.Toplevel(self.ventana)
        ventana.title("Módulo Analizador Léxico")
        ventana.geometry("500x650")

        tk.Label(ventana, text="1. Selecciona los AFN para el Analizador:", font=("Arial", 11, "bold")).pack(pady=10)

        frame_lista = tk.Frame(ventana)
        frame_lista.pack()
        
        # Lista múltiple para seleccionar varios AFNs
        lista_afns = tk.Listbox(frame_lista, selectmode="multiple", width=30, height=6)
        lista_afns.pack(side="left")
        
        scroll = tk.Scrollbar(frame_lista, command=lista_afns.yview)
        scroll.pack(side="right", fill="y")
        lista_afns.config(yscrollcommand=scroll.set)

        for id_afn in ids:
            lista_afns.insert(tk.END, id_afn)

        tk.Label(ventana, text="ID para guardar este Analizador Léxico:").pack(pady=5)
        entrada_id_afd = tk.Entry(ventana, width=28)
        entrada_id_afd.pack(pady=5)

        # Variable para saber cuál analizamos actualmente
        self.afd_actual = None

        def generar_afd_lexico():
            indices = lista_afns.curselection()
            seleccionados = [lista_afns.get(i) for i in indices]
            id_nuevo_afd = entrada_id_afd.get().strip()
            
            if len(seleccionados) < 2:
                messagebox.showerror("Error", "Debes seleccionar al menos 2 AFNs para unirlos.")
                return
            if not id_nuevo_afd:
                messagebox.showerror("Error", "Debes ingresar un ID para guardar el analizador.")
                return
                
            try:
                # Les asignamos un token dinámico (10, 20, 30...) para la demo
                for i, id_sel in enumerate(seleccionados):
                    AFN.obtener_afn(id_sel).asignar_token((i + 1) * 10)
                    
                id_afn_combinado = f"AFN_{id_nuevo_afd}"
                if id_afn_combinado in AFN.afns_creados:
                    del AFN.afns_creados[id_afn_combinado]
                    
                afn_lex = AFN.union_especial_lexica(id_afn_combinado, seleccionados)
                
                from afd import AFD
                self.afd_actual = AFD(id_nuevo_afd).convertir_afn(afn_lex)
                messagebox.showinfo("Éxito", f"Analizador '{id_nuevo_afd}' guardado en memoria.")
            except Exception as e:
                messagebox.showerror("Error", f"Fallo generando AFD: {str(e)}")

        tk.Button(ventana, text="Generar AFD Léxico", command=generar_afd_lexico).pack(pady=10)

        tk.Label(ventana, text="2. Escribe la cadena a analizar:", font=("Arial", 11, "bold")).pack(pady=10)
        entrada_cadena = tk.Entry(ventana, width=40, font=("Arial", 12))
        entrada_cadena.pack(pady=5)

        # Tabla de resultados léxicos
        columnas = ("token", "lexema")
        tabla = ttk.Treeview(ventana, columns=columnas, show="headings", height=10)
        tabla.heading("token", text="Token")
        tabla.heading("lexema", text="Lexema")
        tabla.column("token", width=100, anchor="center")
        tabla.column("lexema", width=200, anchor="center")
        tabla.pack(pady=10)

        def analizar_cadena():
            if getattr(self, "afd_actual", None) is None:
                messagebox.showerror("Error", "Primero debes generar el AFD Léxico.")
                return
                
            cadena = entrada_cadena.get()
            if not cadena:
                return

            # Limpiar tabla
            for fila in tabla.get_children():
                tabla.delete(fila)

            from analiz_lexico import AnalizLexico
            analizador = AnalizLexico(self.afd_actual, cadena)

            while True:
                token = analizador.yylex()
                if token == AnalizLexico.FIN:
                    break
                
                tabla.insert("", tk.END, values=(token, analizador.estado.lexema))
                
                if token == AnalizLexico.ERROR:
                    messagebox.showwarning("Error Léxico", f"Símbolo no reconocido: '{analizador.estado.lexema}'")
                    break

        tk.Button(ventana, text="Analizar Cadena", command=analizar_cadena, bg="lightgreen", width=20).pack(pady=5)
        
    def dibujar_afn(self, canvas, afn):

        canvas.delete("all")

        estados = sorted(
            afn.edos_afn,
            key=lambda e: e.id_edo
        )

        if not estados:
            return

        ancho = 850
        alto = 400

        radio_estado = 25
        margen_x = 90
        margen_y = 70

        posiciones = {}

        # Obtenemos el nivel de cada estado
        niveles = self.calcular_niveles(afn)

        estados_por_nivel = {}

        # Agrupamos los estados según su nivel
        for estado in estados:

            nivel = niveles[estado.id_edo]

            if nivel not in estados_por_nivel:
                estados_por_nivel[nivel] = []

            estados_por_nivel[nivel].append(estado)

        lista_estados = estados_por_nivel[nivel]

        max_nivel = max(
            estados_por_nivel.keys(),
            default=0
        )

        cantidad_niveles = max_nivel + 1

        # Espacio horizontal entre niveles
        if cantidad_niveles == 1:
            espacio_x = 1
        else:
            espacio_x = (
                ancho - 2 * margen_x
            ) / (cantidad_niveles - 1)

        # Calculamos la posición de los estados
        for nivel in sorted(estados_por_nivel.keys()):

            lista_estados = sorted(
                estados_por_nivel[nivel],
                key=lambda e: e.id_edo
            )

            cantidad_estados = len(lista_estados)

            # Si solo hay uno, lo ponemos al centro
            if cantidad_estados == 1:

                y_positions = [
                    alto / 2
                ]

            else:

                espacio_y = (
                    alto - 2 * margen_y
                ) / (cantidad_estados - 1)

                y_positions = [
                    margen_y + i * espacio_y
                    for i in range(cantidad_estados)
                ]

            x = margen_x + nivel * espacio_x

            for estado, y in zip(
                lista_estados,
                y_positions
            ):
                posiciones[estado.id_edo] = (
                    x,
                    y
                )

        # Dibujamos las transiciones

        transiciones = afn.obtener_transiciones()

        # Pares de estados que tienen transición
        pares = {
            (origen, destino)
            for origen, simbolo, destino in transiciones
        }

        estados_aceptacion = {
            estado.id_edo
            for estado in afn.edos_acept
        }

        for origen, simbolo, destino in transiciones:

            x1, y1 = posiciones[origen]
            x2, y2 = posiciones[destino]

            nivel_origen = niveles[origen]
            nivel_destino = niveles[destino]

            # Transicion al mismo estado

            if origen == destino:

                canvas.create_line(
                    x1,
                    y1 - radio_estado,

                    x1 + 35,
                    y1 - 60,

                    x1 - 35,
                    y1 - 60,

                    x1,
                    y1 - radio_estado,

                    smooth=True,
                    arrow=tk.LAST,
                    width=2
                )

                canvas.create_text(
                    x1,
                    y1 - 75,
                    text=simbolo,
                    font=("Arial", 11, "bold")
                )

                continue

            # El salto del inicial al final va por debajo del AFN

            if (
                origen == afn.edo_ini.id_edo
                and destino in estados_aceptacion
            ):

                control_x = (x1 + x2) / 2
                control_y = alto - 20

                canvas.create_line(
                    x1,
                    y1 + radio_estado,

                    control_x,
                    control_y,

                    x2,
                    y2 + radio_estado,

                    smooth=True,
                    arrow=tk.LAST,
                    width=2
                )

                inicio_x = x1
                inicio_y = y1 + radio_estado

                fin_x = x2
                fin_y = y2 + radio_estado

                texto_x = (
                    inicio_x
                    + 2 * control_x
                    + fin_x
                ) / 4

                texto_y = (
                    inicio_y
                    + 2 * control_y
                    + fin_y
                ) / 4

                canvas.create_text(
                    texto_x,
                    texto_y - 8,
                    text=simbolo,
                    font=("Arial", 11, "bold")
                )

                continue

            # Las transiciones hacia atras van por arriba

            if nivel_destino < nivel_origen:

                diferencia_niveles = (
                    nivel_origen - nivel_destino
                )

                altura_arco = (
                    50 + diferencia_niveles * 15
                )

                control_x = (x1 + x2) / 2

                control_y = max(
                    20,
                    min(y1, y2) - altura_arco
                )

                canvas.create_line(
                    x1,
                    y1 - radio_estado,

                    control_x,
                    control_y,

                    x2,
                    y2 - radio_estado,

                    smooth=True,
                    arrow=tk.LAST,
                    width=2
                )

                inicio_x = x1
                inicio_y = y1 - radio_estado

                fin_x = x2
                fin_y = y2 - radio_estado

                texto_x = (
                    inicio_x
                    + 2 * control_x
                    + fin_x
                ) / 4

                texto_y = (
                    inicio_y
                    + 2 * control_y
                    + fin_y
                ) / 4

                canvas.create_text(
                    texto_x,
                    texto_y - 8,
                    text=simbolo,
                    font=("Arial", 11, "bold")
                )

                continue

            # Transiciones hacia adelante

            dx = x2 - x1
            dy = y2 - y1

            distancia = math.sqrt(
                dx ** 2 + dy ** 2
            )

            if distancia == 0:
                continue

            ux = dx / distancia
            uy = dy / distancia

            # Evitamos que la flecha entre
            # hasta el centro del círculo
            inicio_x = (
                x1 + ux * radio_estado
            )

            inicio_y = (
                y1 + uy * radio_estado
            )

            fin_x = (
                x2 - ux * radio_estado
            )

            fin_y = (
                y2 - uy * radio_estado
            )

            # Curvamos la flecha si hay transicion en ambos sentidos

            if (destino, origen) in pares:

                perpendicular_x = -uy
                perpendicular_y = ux

                desplazamiento = 30

                medio_x = (
                    (inicio_x + fin_x) / 2
                    + perpendicular_x * desplazamiento
                )

                medio_y = (
                    (inicio_y + fin_y) / 2
                    + perpendicular_y * desplazamiento
                )

                canvas.create_line(
                    inicio_x,
                    inicio_y,

                    medio_x,
                    medio_y,

                    fin_x,
                    fin_y,

                    smooth=True,
                    arrow=tk.LAST,
                    width=2
                )

                canvas.create_text(
                    medio_x
                    + perpendicular_x * 10,

                    medio_y
                    + perpendicular_y * 10,

                    text=simbolo,
                    font=("Arial", 11, "bold")
                )

            else:

                # Flecha normal
                canvas.create_line(
                    inicio_x,
                    inicio_y,
                    fin_x,
                    fin_y,
                    arrow=tk.LAST,
                    width=2
                )

                medio_x = (
                    inicio_x + fin_x
                ) / 2

                medio_y = (
                    inicio_y + fin_y
                ) / 2

                canvas.create_text(
                    medio_x,
                    medio_y - 12,
                    text=simbolo,
                    font=("Arial", 11, "bold")
                )

        # Dibujamos los estados despues de las transiciones

        for estado in estados:

            x, y = posiciones[
                estado.id_edo
            ]

            # Círculo principal
            canvas.create_oval(
                x - radio_estado,
                y - radio_estado,

                x + radio_estado,
                y + radio_estado,

                width=2
            )

            # Doble círculo si es
            # estado de aceptación
            if estado in afn.edos_acept:

                canvas.create_oval(
                    x - radio_estado + 5,
                    y - radio_estado + 5,

                    x + radio_estado - 5,
                    y + radio_estado - 5,

                    width=2
                )

            # ID del estado
            canvas.create_text(
                x,
                y,
                text=str(estado.id_edo),
                font=("Arial", 11, "bold")
            )

        # Flecha que indica el estado inicial

        inicial = afn.edo_ini

        x, y = posiciones[
            inicial.id_edo
        ]

        canvas.create_line(
            x - radio_estado - 50,
            y,

            x - radio_estado - 3,
            y,

            arrow=tk.LAST,
            width=2
        )

    def ordenar_estados_por_conexiones(
        self,
        estados_por_nivel,
        niveles,
        afn
    ):

        transiciones = afn.obtener_transiciones()

        # Empezamos ordenando por ID
        ordenados = {}

        for nivel, estados in estados_por_nivel.items():
            ordenados[nivel] = sorted(
                estados,
                key=lambda e: e.id_edo
            )

        # Recorremos las columnas de izquierda a derecha
        for nivel in sorted(ordenados.keys()):

            if nivel == 0:
                continue

            nivel_anterior = nivel - 1

            if nivel_anterior not in ordenados:
                continue

            # Posición vertical lógica de los estados anteriores
            posiciones_anteriores = {
                estado.id_edo: i
                for i, estado in enumerate(
                    ordenados[nivel_anterior]
                )
            }

            def prioridad(estado):

                padres = []

                for origen, simbolo, destino in transiciones:

                    if destino != estado.id_edo:
                        continue

                    # Solo nos interesan conexiones
                    # provenientes del nivel anterior
                    if (
                        origen in niveles
                        and niveles[origen] == nivel_anterior
                        and origen in posiciones_anteriores
                    ):
                        padres.append(
                            posiciones_anteriores[origen]
                        )

                # Si nadie del nivel anterior llega aquí,
                # lo dejamos al final
                if not padres:
                    return float("inf")

                # Promedio de las posiciones de sus padres
                return sum(padres) / len(padres)

            ordenados[nivel] = sorted(
                ordenados[nivel],
                key=prioridad
            )

        return ordenados

    def ejecutar(self):
        self.ventana.mainloop()

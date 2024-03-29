import re
import tkinter as tk
from tkinter import *
from tkinter import ttk
from datetime import datetime
from tkinter import messagebox
from tkcalendar import DateEntry
from rut_chile import rut_chile
from email_validator import validate_email, EmailNotValidError


class FormularioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Formulario de Información")

        # Variables para almacenar los datos del formulario
        self.nombre_var = tk.StringVar()
        self.apellido_materno_var = tk.StringVar()
        self.apellido_paterno_var = tk.StringVar()
        self.rut_var = tk.StringVar()
        self.direccion_var = tk.StringVar()
        self.correo_var = tk.StringVar()
        self.telefono_var = tk.StringVar()
        self.empresa_var = tk.StringVar()
        self.funciones_var = tk.StringVar()
        self.descripcion_textbox = tk.StringVar()

        # Variable validar rut
        self.rut_validado = False

        # Crear el marco para el formulario de información personal
        personal_frame = ttk.LabelFrame(root, text="Información Personal")
        personal_frame.grid(row=0, column=0, padx=20, pady=5, sticky="w")

        # Crear campos del formulario de información personal
        ttk.Label(personal_frame, text="Nombre:").grid(
            row=0, column=0, sticky="w")
        nombre_entry = ttk.Entry(personal_frame, textvariable=self.nombre_var)
        nombre_entry.grid(row=0, column=1, sticky="w")

        ttk.Label(personal_frame, text="Apellido Paterno:").grid(
            row=1, column=0, sticky="w")
        apellido_paterno_entry = ttk.Entry(
            personal_frame, textvariable=self.apellido_paterno_var)
        apellido_paterno_entry.grid(row=1, column=1, sticky="w")

        ttk.Label(personal_frame, text="Apellido Materno:").grid(
            row=2, column=0, sticky="w")
        apellido_materno_entry = ttk.Entry(
            personal_frame, textvariable=self.apellido_materno_var)
        apellido_materno_entry.grid(row=2, column=1, sticky="w")

        ttk.Label(personal_frame, text="Rut:").grid(
            row=3, column=0, sticky="w")
        rut_entry = ttk.Entry(personal_frame, textvariable=self.rut_var)
        rut_entry.grid(row=3, column=1, sticky="w")

        # Dar formato Entry - RUT
        def formato_rut(*args):
            # Eliminar guiones y puntos, y verificar si la entrada contiene solo dígitos
            nuevo_input = rut_entry.get().replace("-", "").replace(".", "")
            if len(nuevo_input) == 9:
                # Verificar si el último carácter es un dígito o "K"
                ultimo_caracter = nuevo_input[-1]
                if ultimo_caracter.isdigit() or ultimo_caracter.upper() == "K":
                    formato_rut = f"{nuevo_input[:2]}.{nuevo_input[2:5]}.{nuevo_input[5:8]}-{ultimo_caracter}"
                    self.rut_var.set(formato_rut)
                    self.rut_validado = True
                else:
                    messagebox.showerror(
                        "RUT INVALIDO", "Debe terminar en dígito o 'K'")
                    self.rut_validado = False
                    self.rut_var.set("")
            else:
                messagebox.showerror(
                    "RUT INVALIDO", "RUT debe tener 9 caracteres (sin contar guiones)")
                self.rut_validado = False
                self.rut_var.set("")

        # Vincular la función "formato_rut"al evento <FocusOut>
        rut_entry.bind("<FocusOut>", formato_rut)

        ttk.Label(personal_frame, text="Fecha de Nacimiento").grid(
            row=4, column=0, sticky="w")
        self.calendario_entry = DateEntry(personal_frame, width=12, day=1, month=1, year=2000,
                                          date_pattern="dd-mm-yyyy", background='darkblue', foreground='white', borderwidth=2)
        self.calendario_entry.grid(row=4, column=1, sticky="w")

        ttk.Label(personal_frame, text="Dirección:").grid(
            row=5, column=0, sticky="w")
        direccion_entry = ttk.Entry(
            personal_frame, textvariable=self.direccion_var)
        direccion_entry.grid(row=5, column=1, sticky="w")

        ttk.Label(personal_frame, text="Correo electrónico:").grid(
            row=6, column=0, sticky="w")
        correo_entry = ttk.Entry(personal_frame, textvariable=self.correo_var)
        correo_entry.grid(row=6, column=1, sticky="w")

        ttk.Label(personal_frame, text="Número de teléfono:").grid(
            row=7, column=0, sticky="w")
        telefono_entry = ttk.Entry(
            personal_frame, textvariable=self.telefono_var)
        telefono_entry.grid(row=7, column=1, sticky="w")

        # Formatear telefono al salir del foc
        def formato_telefono(*args):
            nuevo_input = telefono_entry.get()
            # Verifica si la entrada contiene solo dígitos
            if nuevo_input.isdigit():
                # Formatea el número de teléfono
                formato_telefono = f"+56{nuevo_input[0]}{nuevo_input[1:5]}{nuevo_input[5:9]}"
                self.telefono_var.set(formato_telefono)
            else:
                # La entrada no es válida; mantén la entrada original
                self.telefono_var.set(nuevo_input)
        # Vincular la función  al evento <FocusOut>
        telefono_entry.bind("<FocusOut>", formato_telefono)

        ttk.Label(personal_frame, text="Empresa:").grid(
            row=8, column=0, sticky="w")
        empresa_entry = ttk.Entry(
            personal_frame, textvariable=self.empresa_var)
        empresa_entry.grid(row=8, column=1, sticky="w")

        ttk.Label(personal_frame, text="Cargo:").grid(
            row=9, column=0, sticky="w")
        opciones_cargo = ["Ejecutivo de Ventas", "Cajero", "Analista",
                          "Jefe de Área", "Jefe de Proyectos", "Gerente", "DBA"]
        self.cargo_combobox = ttk.Combobox(
            personal_frame, values=opciones_cargo)
        self.cargo_combobox.grid(row=9, column=1, sticky="w")

        ttk.Label(personal_frame, text="Descripción del Cargo:").grid(
            row=10, column=0, sticky="w")

        # Crear un cuadro de texto (textbox) para la descripción
        self.descripcion_textbox = tk.Text(personal_frame, height=5, width=40)
        self.descripcion_textbox.grid(row=10, column=1, sticky="w")

        # Crear e l botón para guardar el formulario
        guardar_button = ttk.Button(
            root, text="Guardar", command=self.guardar_formulario)
        guardar_button.grid(row=1, column=0, padx=20, sticky="w")

        # Crear la grilla para mostrar la información
        self.tabla = ttk.Treeview(root, columns=(
            "Nombre Completo", "Rut", "Edad", "Correo Electrónico", "Teléfono", "Empresa", "Cargo", "Acciones"))
        self.tabla.grid(row=2, column=0,  padx=10, pady=5, sticky="w")
        self.tabla.column("#0", width=10, stretch=False)
        self.tabla.column("#1", width=180, stretch=True)
        self.tabla.column("#2", width=90, stretch=True)
        self.tabla.column("#3", width=40, stretch=True)
        self.tabla.column("#4", width=150, stretch=True)
        self.tabla.column("#5", width=100, stretch=True)
        self.tabla.column("#6", width=100, stretch=True)
        self.tabla.column("#7", width=100, stretch=True)
        self.tabla.column("#8", width=100, stretch=True)

        # Configurar encabezados de columnas
        self.tabla.heading("Nombre Completo", text="Nombre Completo")
        self.tabla.heading("Rut", text="Rut")
        self.tabla.heading("Edad", text="Edad")
        self.tabla.heading("Correo Electrónico", text="Correo Electrónico")
        self.tabla.heading("Teléfono", text="Teléfono")
        self.tabla.heading("Empresa", text="Empresa")
        self.tabla.heading("Cargo", text="Cargo")
        self.tabla.heading("Acciones", text="Acciones")

        # Configurar la acción "Eliminar" en la tabla
        self.tabla.bind("<Button-1>", self.on_select)

        # Agregar scrollbar vertical de la grilla
        scrollbar = ttk.Scrollbar(
            root, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=2, column=1, sticky="ns")

        # Agregar scrollbar horizontal de la grilla
        scrollbar_x = ttk.Scrollbar(
            root, orient="horizontal", command=self.tabla.xview)
        self.tabla.configure(xscrollcommand=scrollbar_x.set)
        scrollbar_x.grid(row=3, column=0, sticky="ew")

    def eliminar_registro(self):
        # Obtener el ítem seleccionado
        selected_item = self.tabla.selection()
        if not selected_item:
            messagebox.showinfo(
                "Error", "Selecciona un registro para eliminar.")
            return

        # Eliminar el ítem seleccionado de la grilla
        self.tabla.delete(selected_item)

    def on_select(self, event):
        selection = self.tabla.selection()
        if selection:
            item = selection[0]
            column = self.tabla.identify_column(event.x)
            if column == "#8":
                self.eliminar_registro()

    def guardar_formulario(self):
        # Obtener datos del formulario

        nombre = self.nombre_var.get()
        apellido_paterno = self.apellido_paterno_var.get()
        apellido_materno = self.apellido_materno_var.get()
        nombre_completo = nombre.upper() + " " + apellido_paterno.upper() + \
            " " + apellido_materno.upper()
        rut = self.rut_var.get()
        fecha_nacimiento = self.calendario_entry.get_date()
        direccion = self.direccion_var.get()
        correo = self.correo_var.get()
        telefono = self.telefono_var.get()
        empresa = self.empresa_var.get().upper()
        cargo = self.cargo_combobox.get()
        descripcion_cargo = self.descripcion_textbox.get("1.0", "end-1c")

        # Validar empresa
        def validar_empresa(nombre_empresa):
            # Patrón regex: letras, números, guión medio y guión bajo (hasta 150 caracteres)
            patron = r'^[\w-]{1,150}$'
            return bool(re.match(patron, nombre_empresa))

        # Validar cargo
        def validar_cargo(cargo):
            if cargo:
                return True
            return False

        # Validar correo
        def validar_correo(correo):
            try:
                # Validar y obtener información sobre el correo
                v = validate_email(correo)
                return True
            except EmailNotValidError as e:
                messagebox.showerror("Error", "Correo Incorrecto")
                return False

        # Validar direccion
        def validar_direccion(direccion):
            direccion = direccion.strip()

            if direccion.isalnum() or "-" in direccion or "#" in direccion or " " in direccion:
                if len(direccion) <= 100:
                    return True
                else:
                    messagebox.showerror(
                        "Error", "La dirección debe tener menos de 100 caracteres.")
                    return False
            else:
                messagebox.showerror(
                    "Error", "La dirección debe ser alfanumérica y puede contener guiones y almohadillas.")
                return False

        # Calcular la edad  a partir de la fecha de nacimiento
        def calcular_edad(fecha_nacimiento):
            if fecha_nacimiento:

                hoy = datetime.today()
                edad = hoy.year - fecha_nacimiento.year - \
                    ((hoy.month, hoy.day) <
                     (fecha_nacimiento.month, fecha_nacimiento.day))
                return edad
            else:
                return 0

            # Validacion del nombre y apellidos

        # Validacion de nombre y apellidos
        def validar_nombre(nombre):
            if len(nombre) > 50:
                messagebox.showerror(
                    "Error", "El nombre y apellidos no pueden exceder los 50 caracteres cada uno.")
                return False
            elif not nombre.strip():
                messagebox.showerror(
                    "Error", "Nombre, Apellidos son requerido.")
                return False
            elif not nombre.replace(" ", "").isalpha():
                messagebox.showerror(
                    "Error", "Nombre y Apellidos solo pueden contener letras.")
                return False
            else:
                return True

        # Insertar datos en la grilla
        if validar_nombre(nombre) and validar_nombre(apellido_materno) and validar_nombre(apellido_paterno) and calcular_edad(fecha_nacimiento) > 0 and self.rut_validado and validar_direccion(direccion) and validar_correo(correo) and validar_empresa(empresa) and validar_cargo(cargo):
            self.tabla.insert("", "end", values=(nombre_completo, rut, calcular_edad(
                fecha_nacimiento), correo, telefono, empresa, cargo, "Eliminar"))
            messagebox.showinfo(
                message="Ingresado Correctamente", title="Aviso")
        else:
            messagebox.showerror("Alerta", "Ingreso Incorrecto")


if __name__ == "__main__":
    root = tk.Tk()
    app = FormularioApp(root)
    root.mainloop()

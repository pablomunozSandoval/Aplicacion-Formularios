from datetime import datetime
from itertools import cycle
import re
from tkinter import messagebox
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview


class FormularioApp(tb.Frame):
    def __init__(self, master_window):
        super().__init__(master_window, padding=(10, 10))
        self.pack(fill=BOTH, expand=YES)

        # -------------------------
        # Variables de Clase
        # -------------------------

        self.nombre = tb.StringVar(value="")
        self.apellido_paterno = tb.StringVar(value="")
        self.apellido_materno = tb.StringVar(value="")
        self.rut = tb.StringVar(value="")
        self.rut_validado = False
        self.direccion = tb.StringVar(value="")
        self.email = tb.StringVar(value="")
        self.telefono = tb.StringVar(value="")
        self.empresa = tb.StringVar(value="")
        self.cargo = tb.StringVar(value="")
        self.descripcion = tb.StringVar(value="")
        self.fecha_nacimiento = tb.datetime(year=1990, month=12, day=1)
        self.definicion = tb.StringVar(value="")
        self.edad = 0
        self.data = []
        self.colors = master_window.style.colors

        informacion_contacto = "Ingrese su informacion de contacto: "
        label_info_contacto = tb.Label(
            self, text=informacion_contacto, width=80)
        label_info_contacto.pack(fill=X, pady=20)

        # -----------------
        #   Inputs
        # -----------------

        self.crear_input_nombre("Nombre: ",  self.nombre)

        self.crear_input_paterno("Apellido Paterno: ", self.apellido_paterno)
        self.crear_input_materno("Apellido Materno: ", self.apellido_materno)
        self.crear_input_rut("Rut: ", self.rut)
        self.crear_datepicker("Fecha Nacimiento:")
        self.crear_input_correo("Correo", self.email)
        self.crear_input_telefonico("Telefono:", self.telefono)
        self.crear_input_direccion("Dirección: ", self.direccion)

        informacion_empresa = "Ingrese la informacion de la empresa:"
        label_info_empresa = tb.Label(self, text=informacion_empresa, width=80)
        label_info_empresa.pack(fill=X, pady=20)
        self.crear_input_empresa("Empresa:", self.empresa)
        self.crear_combobox("Cargo laboral:", self.cargo)
        self.crear_input_descripcion(
            "Definicion del Cargo:", self.definicion)
        self.crear_botones()
        self.tabla = self.crear_tablas()

        cantidad = 5
        for i in range(cantidad):
            self.usuario("Pablo", "18.670.217-4", "pablo@gmail.com",
                         "932894650", "Nodos", "Cajero", "30")

    # ----------------------------------------------
        # Creacion de inputs
    # ----------------------------------------------
    def usuario(self, nombre_completo, rut, email, telefono, empresa, cargo, edad):
        self.data.append((nombre_completo, rut, edad, email,
                          telefono, empresa, cargo, "Eliminar"))
        self.tabla.destroy()
        self.tabla = self.crear_tablas()

    def crear_input_nombre(self, label, variable):

        frame_interno = tb.Frame(self)
        frame_interno.pack(fill=X, expand=YES, pady=5)

        label_nombre = tb.Label(
            master=frame_interno, text=label, width=20)
        label_nombre.pack(side=LEFT, padx=12)

        self.form_nombre = tb.Entry(
            master=frame_interno, textvariable=variable)
        validador = (self.register(
            self.validar_nombre), '%i', '%P')
        self.form_nombre.configure(
            validate='key', validatecommand=validador)
        self.form_nombre.pack(side=LEFT, padx=5, fill=X, expand=YES)

    def crear_input_paterno(self, label, variable):

        frame_interno = tb.Frame(self)
        frame_interno.pack(fill=X, expand=YES, pady=5)

        label_nombre = tb.Label(
            master=frame_interno, text=label, width=20)
        label_nombre.pack(side=LEFT, padx=12)

        self.form_paterno = tb.Entry(
            master=frame_interno, textvariable=variable)
        validador = (self.register(
            self.validar_paterno), '%i', '%P')
        self.form_paterno.configure(
            validate='key', validatecommand=validador)
        self.form_paterno.pack(side=LEFT, padx=5, fill=X, expand=YES)

    def crear_input_materno(self, label, variable):

        frame_interno = tb.Frame(self)
        frame_interno.pack(fill=X, expand=YES, pady=5)

        label_nombre = tb.Label(
            master=frame_interno, text=label, width=20)
        label_nombre.pack(side=LEFT, padx=12)

        self.form_materno = tb.Entry(
            master=frame_interno, textvariable=variable)

        validador = (self.register(
            self.validar_materno), '%i', '%P')

        self.form_materno.configure(
            validate='key', validatecommand=validador)
        self.form_materno.pack(side=LEFT, padx=5, fill=X, expand=YES)

    # --------------------------------------------------

    def crear_input_rut(self, label, variable):
        frame_interno = tb.Frame(self)
        frame_interno.pack(fill=X, expand=YES, pady=5)

        field_label = tb.Label(master=frame_interno, text=label, width=20)
        field_label.pack(side=LEFT, padx=12)

        # Creamos el widget de entrada (Entry) para el RUT
        self.form_rut = tb.Entry(
            master=frame_interno, textvariable=variable)
        self.form_rut.pack(side=LEFT, padx=5, fill=X, expand=YES)
        self.form_rut.bind(
            "<FocusOut>", self.formatear_rut)

    # --------------------------------------------------

    def crear_datepicker(self, label):

        frame_interno = tb.Frame(self)
        frame_interno.pack(fill=X, expand=YES, pady=5)

        field_label = tb.Label(master=frame_interno, text=label, width=20)
        field_label.pack(side=LEFT, padx=12)

        self.calendario_entry = tb.DateEntry(
            master=frame_interno, firstweekday=0, startdate=datetime(1990, 12, 31))
        self.calendario_entry.pack(side=LEFT, padx=5, fill=X, expand=YES)
    # --------------------------------------------------

    def crear_input_direccion(self, label, variable):
        frame_interno = tb.Frame(self)
        frame_interno.pack(fill=X, expand=YES, pady=5)

        field_label = tb.Label(master=frame_interno, text=label, width=20)
        field_label.pack(side=LEFT, padx=12)

        self.form_direccion = tb.Entry(
            master=frame_interno, textvariable=variable)
        validador = (self.register(
            self.validar_direccion), '%i', '%P')

        self.form_direccion.pack(side=LEFT, padx=5, fill=X, expand=YES)
        self.form_direccion.configure(
            validate="key", validatecommand=validador)

    # --------------------------------------------------

    def crear_input_correo(self, label, variable):
        frame_interno = tb.Frame(self)
        frame_interno.pack(fill=X, expand=YES, pady=5)

        field_label = tb.Label(master=frame_interno, text=label, width=20)
        field_label.pack(side=LEFT, padx=12)

        validador = (self.register(self.validar_correo))

        self.form_correo = tb.Entry(
            master=frame_interno, textvariable=variable, validatecommand=(validador, '%i', "%P"), validate='focusout')
        self.form_correo.pack(side=LEFT, padx=5, fill=X, expand=YES)

    # --------------------------------------------------

    def crear_input_telefonico(self, label, variable):
        frame_interno = tb.Frame(self)
        frame_interno.pack(fill=X, expand=YES, pady=5)

        field_label = tb.Label(master=frame_interno, text=label, width=20)
        field_label.pack(side=LEFT, padx=12)

        field_internacional = tb.Label(
            master=frame_interno, text="+56", width=5)
        field_internacional.pack(side=LEFT, padx=3)

        self.form_numero = tb.Entry(
            master=frame_interno, textvariable=variable)
        validado = self.register(
            self.validar_y_formatear_telefono)
        self.form_numero.config(validate='key',
                                validatecommand=(validado, '%i', '%P'))
        self.form_numero.pack(side=LEFT, padx=5, fill=X, expand=YES)

    # --------------------------------------------------

    def crear_combobox(self, label, variable):
        frame_interno = tb.Frame(self)
        frame_interno.pack(fill=X, expand=YES, pady=5)

        field_label = tb.Label(master=frame_interno, text=label, width=20)
        field_label.pack(side=LEFT, padx=12)

        opciones_cargo = ["Ejecutivo de Ventas", "Cajero", "Analista",
                          "Jefe de Área", "Jefe de Proyectos", "Gerente", "DBA"]

        cargo_combobox = tb.Combobox(
            master=frame_interno, values=opciones_cargo, textvariable=variable, state=READONLY)
        cargo_combobox.pack(side=LEFT, padx=5, fill=X, expand=YES)

# --------------------------------------------------------

    def crear_input_descripcion(self, label, variable):
        frame_interno = tb.Frame(self)
        frame_interno.pack(fill=X, expand=YES, pady=5)

        field_label = tb.Label(master=frame_interno, text=label, width=20)
        field_label.pack(side=LEFT, padx=12)

        form_direccion = tb.Entry(master=frame_interno, textvariable=variable)
        form_direccion.pack(side=LEFT, padx=5, fill=X, expand=YES)
# -------------------------------------------------------

    def crear_input_empresa(self, label, variable):
        frame_interno = tb.Frame(self)
        frame_interno.pack(fill=X, expand=YES, pady=5)

        field_label = tb.Label(master=frame_interno, text=label, width=20)
        field_label.pack(side=LEFT, padx=12)

        self.form_empresa = tb.Entry(
            master=frame_interno, textvariable=variable)
        validador = (self.register(
            self.validar_empresa), '%i', '%P')
        self.form_empresa.pack(side=LEFT, padx=5, fill=X, expand=YES)
        self.form_empresa.configure(
            validate="key", validatecommand=validador)

# -----------------------------------------------
        # Crear Tabla
# -----------------------------------------------

    def crear_tablas(self):
        coldata = [
            {"text": "Nombre Completo", "width": 150},
            {"text": "Rut", "width": 80},
            {"text": "Edad", "width": 30},
            {"text": "Correo", "width": 100},
            {"text": "Telefono", "width": 80},
            {"text": "Empresa", "width": 50},
            {"text": "Cargo", "width": 100},
            {"text": "Acciones", "width": 90}
        ]
        tabla = Tableview(
            master=self,
            coldata=coldata,
            rowdata=self.data,
            paginated=False,
            searchable=False,
            autofit=True,
            autoalign=CENTER
            # bootstyle=PRIMARY,
            # stripecolor=(self.colors.light, None)
        )

        tabla.pack(fill=BOTH, expand=NO, padx=10, pady=10)
        tabla.view.bind("<Double-Button-1>", self.eliminar_fila)
        tabla.view.bind("<Double-Button-2>", self.eliminar_fila)

        return tabla

    def eliminar_fila(self, event):
        # Obtén la columna en la que se hizo clic
        column = self.tabla.view.identify_column(event.x)

        # Verifica si se hizo clic en la columna 8 (índice 7)
        if column == "#8":
            # Obtiene la fila seleccionada
            selected_row = self.tabla.view.index(self.tabla.view.selection())
            if selected_row is not None:
                # Elimina la fila seleccionada
                self.tabla.delete_row(selected_row)
        else:
            print("No se hizo clic en la columna 8")

# --------------------------------------------
    # Crear Botones
# --------------------------------------------

    def crear_botones(self):
        frame_botones = tb.Frame(self)
        frame_botones.pack(fill=X, expand=YES, pady=(15, 20))

        guardar_boton = tb.Button(
            master=frame_botones,
            text="Guardar",
            command=self.guardar_datos,
            bootstyle='SUCCESS - OUTLINE',
            width=10)
        guardar_boton.pack(side=RIGHT, padx=32)

        self.error_label = tb.Label(master=frame_botones, bootstyle=DANGER)
        self.error_label.pack(side=RIGHT, padx=12)

    # --------------------------------------------------
        # Método que se encarga de obtener los valores de las variables asociadas a cada campo
        # y de realizar el ingreso a la tabla
    # --------------------------------------------------

    def guardar_datos(self):

        # Obtener datos del formulario
        nombre = self.nombre.get()
        apellido_paterno = self.apellido_paterno.get()
        apellido_materno = self.apellido_materno.get()
        nombre_completo = nombre.upper() + " " + apellido_paterno.upper() + \
            " " + apellido_materno.upper()
        fecha_nacimiento = self.calendario_entry.entry.get()
        direccion = self.direccion.get()
        correo = self.email.get()
        telefono = "+56 "+self.telefono.get()
        empresa = self.empresa.get().upper()
        cargo = self.cargo.get()
        rut = self.rut.get()

        descripcion_cargo = self.descripcion.get()

        if len(nombre) != 0 and len(apellido_paterno) != 0 and len(apellido_materno) != 0 and self.calcular_edad(fecha_nacimiento) > 0 and self.rut_validado and len(correo) != 0 and len(direccion) != 0 and len(telefono) != 0 and len(empresa) != 0 and len(cargo) != 0:

            self.data.append((nombre_completo, rut, self.edad, correo,
                             telefono, empresa, cargo, "Eliminar"))
            self.tabla.destroy()

            self.tabla = self.crear_tablas()

            messagebox.showinfo(
                message="Ingresado Correctamente", title="Aviso")
        else:
            messagebox.showerror("Alerta", "Ingreso Incorrecto")


# ------------------------------------------------------------
    # Validaciones
# ------------------------------------------------------------

    def validar_nombre(self, indice, nuevo):
        patron = r'^[a-zA-ZñÑ\s]{1,50}$'
        self.regex_validacion = re.compile(patron)
        resultado = self.regex_validacion.match(nuevo) is not None

        if resultado:
            self.form_nombre.config(bootstyle=PRIMARY)
            return TRUE
        else:
            if len(nuevo.strip()) == 0:
                self.form_nombre.config(bootstyle=DANGER)
                self.form_nombre.delete(0, END)
                return FALSE
            else:
                self.form_nombre.config(bootstyle=DANGER)
                return FALSE

    def validar_paterno(self, indice, nuevo):
        patron = r'^[a-zA-ZñÑ\s]{0,50}$'
        self.regex_validacion = re.compile(patron)
        resultado = self.regex_validacion.match(nuevo) is not None
        if resultado:
            self.form_paterno.config(bootstyle=PRIMARY)
            return True
        else:
            if len(nuevo.strip()) == 0:
                self.form_paterno.config(bootstyle=DANGER)
                self.form_paterno.delete(0, END)
                return FALSE
            else:
                self.form_paterno.config(bootstyle=DANGER)
                return FALSE

    def validar_materno(self, indice, nuevo):
        patron = r'^[a-zA-ZñÑ\s]{1,50}$'
        self.regex_validacion = re.compile(patron)
        resultado = self.regex_validacion.match(nuevo) is not None
        if resultado:
            self.form_materno.config(bootstyle=PRIMARY)
            return True
        else:
            if len(nuevo.strip()) == 0:
                self.form_materno.config(bootstyle=DANGER)
                self.form_materno.delete(0, END)
                return FALSE
            else:
                self.form_materno.config(bootstyle=DANGER)
                return FALSE

    def formatear_rut(self, evento=None):
        self.rut_validado = False
        self.form_rut.configure(bootstyle=PRIMARY)
        # Eliminar guiones y puntos, y verificar si la entrada contiene solo dígitos
        nuevo_input = self.form_rut.get().strip().replace("-", "").replace(".", "")
        if len(nuevo_input) != 0:
            ultimo_caracter = nuevo_input[-1]
            if len(nuevo_input) >= 9 and ultimo_caracter.isdigit() or ultimo_caracter.upper() == "K":
                # Verificar si el último carácter es un dígito o "K"
                formato_rut = f"{nuevo_input[:2]}.{nuevo_input[2:5]}.{nuevo_input[5:8]}-{ultimo_caracter}"
                # Limpiar el contenido actual del Entry
                self.form_rut.delete(0, 'end')
                # Insertar el nuevo formato
                self.form_rut.insert(0, formato_rut)
                self.rut_validado = True

            else:
                self.form_rut.configure(bootstyle=DANGER)
                formato_rut = f"{nuevo_input[:2]}.{nuevo_input[2:5]}.{nuevo_input[5:8]}"
                # Limpiar el contenido actual del Entry
                self.form_rut.delete(0, 'end')
                self.form_rut.insert(0, formato_rut)
                self.rut_validado = FALSE
        else:
            self.form_rut.configure(bootstyle=DANGER)
            self.rut_validado = FALSE

    def validar_direccion(self, indice, direccion):

        # Patrón que permite alfanuméricos, guiones y #
        patron = r'^[\w#\-\s]{1,100}$'
        if not direccion:  # Verifica si la dirección está vacía
            self.form_direccion.configure(bootstyle=DANGER)
            self.form_direccion.delete(0, END)
            return FALSE
        # Verifica si la dirección no cumple con el patrón
        elif not re.match(patron, direccion):
            self.form_direccion.configure(bootstyle=DANGER)
            return FALSE
        else:
            if len(direccion.strip()) != 0:  # Si la dirección es válida
                self.form_direccion.configure(bootstyle=PRIMARY)
                return TRUE
            self.form_direccion.configure(bootstyle=DANGER)
            self.form_direccion.delete(0, END)
            return FALSE

    def validar_correo(self, indice, correo):
        # Patrón de expresión regular para validar un correo electrónico
        patron_correo = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        # Utilizamos re.match para verificar si el correo coincide con el patrón
        if re.fullmatch(patron_correo, correo) is None:
            self.form_correo.configure(bootstyle=DANGER)
            return False
        self.form_correo.configure(bootstyle=PRIMARY)
        return True

    def validar_y_formatear_telefono(self, indice, numero):
        patron = r'^\d{0,9}$'
        self.regex_validacion = re.compile(patron)
        resultado = self.regex_validacion.match(numero) is not None
        if len(numero) > 9:
            self.form_numero.configure(bootstyle=PRIMARY)
            return FALSE
        elif len(numero.strip()) == 0:
            self.form_numero.configure(bootstyle=DANGER)
            self.form_numero.delete(0, END)
            return False
        else:
            if resultado:
                self.form_numero.configure(bootstyle=PRIMARY)
                return True
            self.form_numero.configure(bootstyle=DANGER)
            return False

    def validar_empresa(self, indice, empresa):
        # Cambio en el patrón para permitir alfanuméricos y limitar longitud a 150

        patron = r'^\w{1,150}$'
        self.regex_validacion = re.compile(patron)
        resultado = self.regex_validacion.match(empresa)
        if not resultado:  # Si no hay coincidencia con el patrón
            self.form_empresa.configure(bootstyle=DANGER)
            self.form_empresa.delete(0, END)
            return False

        else:  # Si hay coincidencia con el patrón
            self.form_empresa.configure(bootstyle=PRIMARY)
            return True

    def validar_descripcion(descripcion):
        if len(descripcion) > 1000:  # Verifica si la longitud de la descripción supera los 1000 caracteres
            return False  # La descripción es demasiado larga
        else:  # Si la descripción está dentro del límite de longitud
            return True

    def calcular_edad(self, fecha_nacimiento):
        if fecha_nacimiento:
            fecha_nacimiento = fecha_nacimiento.replace("-", "/")
            formato = "%d/%m/%Y"
            fecha_nacimiento = datetime.strptime(fecha_nacimiento, formato)
            hoy = datetime.today()
            edad_resultado = hoy.year - fecha_nacimiento.year - \
                ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
            self.edad = edad_resultado
            return self.edad
        else:
            return 0


if __name__ == "__main__":
    root = tb.Window("FormularioApp", "superhero", resizable=(False, True))
    app = FormularioApp(root)
    root.mainloop()

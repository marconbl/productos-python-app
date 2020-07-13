from tkinter import ttk
from tkinter import *

import sqlite3

class producto:
    db_name = "database.db"


    def __init__(self, window):
        self.wind = window
        self.wind.title('Aplicacion de Productos')

        #Creacion de un contenedor con label#
        frame = LabelFrame(self.wind, text = "Registra un nuevo producto")
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        #Nombre de entrada
        Label(frame, text = 'Nombre: ').grid(row = 1, column = 0)
        self.nombre = Entry(frame)
        self.nombre.focus()
        self.nombre.grid(row = 1, column = 1)

        #Precio de entrada
        Label(frame, text = 'Precio ').grid(row = 2, column = 0)
        self.precio = Entry(frame)
        self.precio.grid(row = 2, column = 1)

        #Creacion de boton de agregar producto
        ttk.Button(frame, text = "Guardar Producto", command = self.add_productos).grid(row = 3, columnspan = 2, sticky = W + E)

        #Mensaje de Salida
        self.mensaje = Label(text = "", fg = "red")
        self.mensaje.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)


        #Tabla
        self.tree = ttk.Treeview(height = 10, columns = 2)
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading("#0", text = "Nombre", anchor = CENTER)
        self.tree.heading("#1", text = "Precio", anchor = CENTER)

        #Botones Eliminar y actualizar
        ttk.Button(text = "Eliminar", command =self.eliminar_productos).grid(row = 5, column = 0, sticky = W + E)
        ttk.Button(text = "Editar", command =self.editar_productos).grid(row = 5, column = 1, sticky = W + E)


        #Llenando las filas de la tabla
        self.get_productos()


    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            resultado = cursor.execute(query, parameters)
            conn.commit()
        return resultado


    def get_productos(self):
        #limpieza de tabla
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        #consulta
        query = "SELECT * FROM productos ORDER BY nombre DESC"
        db_rows = self.run_query(query)
        #imprimiendo los datos
        for row in db_rows:
            self.tree.insert('', 0 , text = row [1], value = row [2])
    
    def validacion(self):
        return len(self.nombre.get()) != 0 and (self.precio.get()) != 0


    def add_productos(self):
        if self.validacion():
            query = "INSERT INTO productos VALUES(NULL, ?, ?)"
            parametros = (self.nombre.get(), self.precio.get())
            self.run_query(query, parametros)
            self.mensaje["text"] = "El producto '{}' ha sido guardado".format(self.nombre.get())
            self.nombre.delete(0, END)
            self.precio.delete(0, END)
        else:
            self.mensaje["text"] = "El nombre y el precio son requeridos"
        self.get_productos()
    def eliminar_productos(self):
        self.mensaje["text"] = ""
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.mensaje["text"] = "Por favor selecciona un registro"
            return
        self.mensaje["text"] = ""    
        name = self.tree.item(self.tree.selection())['text']
        query = "DELETE FROM productos WHERE nombre = ?"
        self.run_query(query, (name, ))
        self.mensaje["text"] = "El registro '{}' ha sido eliminado correctamente.".format(name)
        self.get_productos()
    def editar_productos(self):
        self.mensaje["text"] = ""
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.mensaje["text"] = "Por favor selecciona un registro"
            return
        name = self.tree.item(self.tree.selection())['text']
        precio_anterior =  self.tree.item(self.tree.selection())['values'][0]
        self.ventanadeEdicion = Toplevel()
        self.ventanadeEdicion.title = "Editar producto"

        #Nombre anterior
        Label(self.ventanadeEdicion, text="Nombre anterior: ").grid(row = 0, column = 1)
        Entry(self.ventanadeEdicion, textvariable = StringVar(self.ventanadeEdicion, value = name), state = "readonly").grid(row = 0, column = 2)
        #Nombre nuevo
        Label(self.ventanadeEdicion, text="Nombre nuevo: ").grid(row = 1, column = 1)
        nuevo_nombre = Entry(self.ventanadeEdicion)
        nuevo_nombre.grid(row = 1, column = 2)
        #Precio anterior
        Label(self.ventanadeEdicion, text="Precio anterior: ").grid(row = 2, column = 1)
        Entry(self.ventanadeEdicion, textvariable = StringVar(self.ventanadeEdicion, value = precio_anterior), state = "readonly").grid(row = 2, column = 2)
        #Precio nuevo
        Label(self.ventanadeEdicion, text="Precio nuevo: ").grid(row = 3, column = 1)
        nuevo_precio = Entry(self.ventanadeEdicion)
        nuevo_precio.grid(row = 3, column = 2)

        Button(self.ventanadeEdicion, text = "Actualizar", command = lambda: self.edit_records(nuevo_nombre.get(),name, nuevo_precio.get(), precio_anterior)).grid(row = 4, column = 2, sticky = W)

    def edit_records(self, nuevo_nombre, name, nuevo_precio, precio_anterior):
        query = "UPDATE productos SET nombre = ?, precio = ? WHERE nombre = ? AND precio = ?"
        parameters = (nuevo_nombre, name, nuevo_precio, precio_anterior)
        self.run_query(query, parameters)
        self.ventanadeEdicion.destroy()
        self.mensaje["text"] = "El registro '{}' ha sido actualizado correctamente".format(name)
        self.get_productos()
      




if __name__ == '__main__':
    window = Tk ()
    aplicacion = producto(window)
    window.mainloop()

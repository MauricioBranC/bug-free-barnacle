import tkinter as tk
from tkinter import ttk
import sympy as sp
import numpy as np

class MatrizGUI:
    def __init__(self, root):
        def rgb_to_hex(r, g, b):
            """Convierte valores RGB a una cadena hexadecimal."""
            return f'#{r:02x}{g:02x}{b:02x}'

        font_color = rgb_to_hex(240, 240, 240)
        text_color = rgb_to_hex(32,32,30)
        relleno_celda = rgb_to_hex(226, 226, 226)
        relleno_botones = rgb_to_hex(251, 251, 251)
        Title_style = ("Times New Roman", 15, "bold")
        Letras_style = ("Times New Roman", 10)

        self.root = root
        self.root.title("Escalonar")
        self.root.geometry("500x300")
        self.root.configure(bg=font_color)
        self.matriz = sp.Matrix([[0]])  # Matriz inicial de 1x1

        self.frame = ttk.Frame(root)
        self.frame.pack(padx=10, pady=10)

        self.table_frame = ttk.Frame(self.frame)
        self.table_frame.grid(row=0, column=0, columnspan=4)

        self.create_table()

        # Botones para añadir y quitar filas y columnas
        ttk.Button(self.frame, text="Añadir fila", command=self.add_row).grid(row=1, column=0, pady=5)
        ttk.Button(self.frame, text="Quitar fila", command=self.remove_row).grid(row=1, column=1, pady=5)
        ttk.Button(self.frame, text="Añadir columna", command=self.add_column).grid(row=1, column=2, pady=5)
        ttk.Button(self.frame, text="Quitar columna", command=self.remove_column).grid(row=1, column=3, pady=5)

        # Botón para escalonar la matriz
        ttk.Button(self.frame, text="Escalonar Matriz", command=self.escalonar_matriz).grid(row=2, column=0, columnspan=4, pady=10)

        # Frame para mostrar la matriz escalonada
        self.escalonada_frame = ttk.Frame(self.frame)
        self.escalonada_frame.grid(row=3, column=0, columnspan=4)

    def create_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        rows, cols = self.matriz.shape
        self.entries = []
        for i in range(rows):
            row_entries = []
            for j in range(cols):
                entry = ttk.Entry(self.table_frame, width=10)
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(0, str(self.matriz[i, j]))
                row_entries.append(entry)
            self.entries.append(row_entries)

    def update_matrix(self):
        rows = len(self.entries)
        cols = len(self.entries[0]) if rows > 0 else 0
        new_matrix = sp.zeros(rows, cols)
        for i in range(rows):
            for j in range(cols):
                try:
                    new_matrix[i, j] = float(self.entries[i][j].get())
                except ValueError:
                    new_matrix[i, j] = 0
        self.matriz = new_matrix

    def add_row(self):
        self.update_matrix()
        rows, cols = self.matriz.shape
        self.matriz = self.matriz.row_insert(rows, sp.zeros(1, cols))
        self.create_table()

    def remove_row(self):
        self.update_matrix()
        rows, cols = self.matriz.shape
        if rows > 1:
            self.matriz = self.matriz.row_del(rows - 1)
            self.create_table()

    def add_column(self):
        self.update_matrix()
        rows, cols = self.matriz.shape
        self.matriz = self.matriz.col_insert(cols, sp.zeros(rows, 1))
        self.create_table()

    def remove_column(self):
        self.update_matrix()
        rows, cols = self.matriz.shape
        if cols > 1:
            self.matriz = self.matriz.col_del(cols - 1)
            self.create_table()

    def escalonar_matriz(self):
        self.update_matrix()
        matriz_escalonada = self.eliminacion_gauss_no_reducida(self.matriz)  # Obtener la forma escalonada no reducida
        self.display_escalonada(matriz_escalonada)

    def eliminacion_gauss_no_reducida(self, A):
        A = np.array(A.evalf(), dtype=float)  # Convertir A a numpy array de tipo float
        filas, columnas = A.shape

        for i in range(min(filas, columnas)):
            # Encontrar el máximo en la columna actual para usarlo como pivote
            max_row_index = np.argmax(np.abs(A[i:, i])) + i
            if A[max_row_index, i] != 0:
                # Intercambiar filas
                A[[i, max_row_index]] = A[[max_row_index, i]]
                # Hacer el pivote igual a 1
                A[i] = A[i] / A[i, i]

                # Hacer ceros debajo del pivote
                for j in range(i + 1, filas):
                    A[j] = A[j] - A[j, i] * A[i]

        return sp.Matrix(A)

    def display_escalonada(self, matriz_escalonada):
        for widget in self.escalonada_frame.winfo_children():
            widget.destroy()

        rows, cols = matriz_escalonada.shape
        for i in range(rows):
            for j in range(cols):
                label = ttk.Label(self.escalonada_frame, text=str(matriz_escalonada[i, j]), relief=tk.RIDGE, width=10)
                label.grid(row=i, column=j, padx=5, pady=5)

def Escalonar(): 
    root = tk.Tk()
    app = MatrizGUI(root)
    root.mainloop()

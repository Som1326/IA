import tkinter as tk
from algorithms import SmartCar
import os
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
import time


class Application2:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SmartCar Navigation")
        self.smart_car = SmartCar()
        self.ciudad = None
        self.carro = None
        self.recogio_pasajero = False
        self.frames = []
        self.current_frame = 0
        self.label = None  # Inicializar el label para el GIF aquí
        self.cell_size = 60
        self.margin = 10

    def run(self):
        self.create_main_window()
        self.root.mainloop()
    
    def show_gif(self, parent, gif_path,width, height):
        try:
            # Cargar el GIF usando Pillow
            self.gif_image = Image.open(gif_path)
            self.frames = []
            for frame in range(self.gif_image.n_frames):
                self.gif_image.seek(frame)
                frame_image = self.gif_image.copy()
                frame_image = frame_image.resize((width, height), Image.LANCZOS)  # Redimensionar el fotograma
                frame_image_tk = ImageTk.PhotoImage(frame_image)
                self.frames.append(frame_image_tk)

            # Crear un Label para mostrar el GIF
            self.label = tk.Label(parent)
            self.label.pack(pady=10)

            # Iniciar la animación
            self.animate_gif()
        except Exception as e:
            print(f"Error al cargar el GIF: {e}")
        
    def animate_gif(self):
        # Mostrar el fotograma actual
        if self.frames:  # Asegurarse de que haya fotogramas
            self.label.config(image=self.frames[self.current_frame])
            self.current_frame = (self.current_frame + 1) % len(self.frames)

        # Programar el siguiente fotograma
        self.label.after(100, self.animate_gif)  # Cambia el tiempo según la velocidad deseada
    
    def cargar_imagen(self, ruta):
        """Carga una imagen y la redimensiona al tamaño especificado."""
        imagen = Image.open(ruta)
        return ImageTk.PhotoImage(imagen)

    def create_main_window(self, width=1067, height=600):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.resizable(False, False)
        
        gif_path = os.path.abspath("ProyectoIA_SmartCar/Proyecto I/img/mainScr.gif")
        self.show_gif(self.root, gif_path, width=1067, height=600)
        
        button_frame = tk.Frame(self.root, bg='#121212', bd=0)
        button_frame.place(relx=0.5, rely=0.8, anchor='center') 
        tk.Button(button_frame, text="Upload the City", 
                  command=self.abrir_archivo, 
                  font=("Arial", 12), 
                  bg='#121212', 
                  fg="white",
                  padx=40,
                  pady=10,
                  borderwidth=2,
                  relief="flat",
                  activebackground="#45a049",
                  activeforeground="white",
                  ).pack(pady=0)
         
    def abrir_archivo(self):
        # Abrir el archivo y cargar la matriz de la ciudad
        archivo = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if archivo:
            self.ciudad = self.smart_car.iniciar_variables(archivo)
            self.create_second_window()
        else:
            messagebox.showerror("Error", "No se ha seleccionado ningún archivo")
            
    def create_second_window(self):
        new_window = tk.Toplevel(self.root, bg="#000000")
        new_window.title("SmartCar Navigation")
        new_window.state('zoomed')
        new_window.rowconfigure(0, weight=1)
        
        self.botones_canvas = tk.Canvas(new_window, bg="#121212", highlightbackground="#121212")
        self.botones_canvas.grid(column=0, padx=10, pady=5, sticky="ns")
        
        button_style = {
            "font": ("Arial", 10),
            "bg": "#2C2E30",
            "fg": "white",
            "padx": 1,
            "pady": 1,
            "borderwidth": 0,
            "width": 11,
            "height": 5,
            "relief": "flat",
            "activebackground": "#45a049",
            "activeforeground": "white"
        }
        tk.Label(self.botones_canvas, text="No informada", 
                 bg="#121212",
                 font=("Arial", 16),
                 fg="white"
                 ).grid(row=0, column=0, padx=10, pady=5)
        
        tk.Button(self.botones_canvas, text="Amplitud",**button_style, command=self.run_amplitud).grid(row=1, column=0, padx=10, pady=5)
        tk.Button(self.botones_canvas, text="Costo uniforme", **button_style, command=self.run_costo).grid(row=2, column=0, padx=10, pady=5)
        tk.Button(self.botones_canvas, text="Profundidad",**button_style, command=self.run_rofundidad).grid(row=3, column=0, padx=10, pady=5)
        
        tk.Label(self.botones_canvas, text="Informada", 
                 bg="#121212",
                 font=("Arial", 16),
                 fg="white"
                 ).grid(row=4, column=0, padx=10, pady=5)
        
        tk.Button(self.botones_canvas, text="Avara",**button_style, command=self.run_avara).grid(row=5, column=0, padx=10, pady=5)
        tk.Button(self.botones_canvas, text="A*",**button_style, command=self.run_AStar).grid(row=6, column=0, padx=10, pady=5)
        
        tk.Label(self.botones_canvas, text="Reiniciar", 
                 bg="#121212",
                 font=("Arial", 16),
                 fg="white"
                 ).grid(row=7, column=0, padx=10, pady=5)
        
        self.city = tk.Canvas(new_window, width=620, height=620, bg="#121212", highlightbackground="#121212")
        self.city.grid(row= 0 ,column=3, padx=10, pady=5)
        self.dibujar_mapa(self.city)
        
        tk.Button(self.botones_canvas, text="ResetMap",
                  bg="#2C2E30",
                  fg= "white",
                  borderwidth = 0,
                  width = 8,
                  height = 4,
                  relief="flat",
                  activebackground= "#45a049",
                  activeforeground= "white",
                  command=self.reset_map
                  ).grid(row=8, column=0, padx=10, pady=2)
    
        
        resultados_canva = tk.Canvas(new_window, width=525, height=620, bg="#000000", highlightbackground="#000000")
        resultados_canva.grid(row= 0 ,column=4, padx=6, pady=5)
        
        label_style = {
            "font": ("roboto", 15),
            "bg": "#000000",
            "fg": "white",
        }
        
        img_path = os.path.abspath("ProyectoIA_SmartCar/Proyecto I/img/secondSrc.png")
        red_img = Image.open(img_path)
        resized_image = red_img.resize((521, 289), Image.LANCZOS)
        self.img = ImageTk.PhotoImage(resized_image)
        image_label = tk.Label(resultados_canva, image=self.img)
        image_label.grid(row=0,column=0,columnspan=2,padx=10,pady=5)
    
        tk.Label(resultados_canva, text="SMART CAR",
                font= ("roboto", 25),
                bg= "#000000",
                fg= "white",
                 ).grid(row=1,column=0,columnspan=2,padx=10,pady=5)
        
        tk.Label(resultados_canva, text="nodos expandidos: ", **label_style).grid(row=2,column=0,padx=10,pady=5)
        self.nodos_label = tk.Label(resultados_canva, text="", **label_style)
        self.nodos_label.grid(row=2,column=1,padx=10,pady=5)
        
        tk.Label(resultados_canva, text=" profundidad: ", **label_style).grid(row=3,column=0,padx=10,pady=5)
        self.profundidad_label = tk.Label(resultados_canva, text="", **label_style)
        self.profundidad_label.grid(row=3,column=1,padx=10,pady=5)
        
        tk.Label(resultados_canva, text="tiempo de computo: ", **label_style).grid(row=4,column=0,padx=10,pady=5)
        self.tiempo_label = tk.Label(resultados_canva, text="", **label_style)
        self.tiempo_label.grid(row=4,column=1,padx=10,pady=5)
        
        tk.Label(resultados_canva, text="costo: ", **label_style).grid(row=5,column=0,padx=10,pady=5)
        self.costo_label = tk.Label(resultados_canva, text="", **label_style)
        self.costo_label.grid(row=5,column=1,padx=10,pady=5)
        
        
    def dibujar_mapa(self, canvas):
        # Limpiar el canvas
        canvas.delete("all")
        
        ruta_vehiculo = os.path.abspath("ProyectoIA_SmartCar/Proyecto I/img/car2.png")
        ruta_pasajero = os.path.abspath("ProyectoIA_SmartCar/Proyecto I/img/passenger2.png")
        ruta_meta = os.path.abspath("ProyectoIA_SmartCar/Proyecto I/img/goal.png")
        self.imagen_vehiculo = self.cargar_imagen(ruta_vehiculo)
        self.imagen_pasajero = self.cargar_imagen(ruta_pasajero)
        self.imagen_meta = self.cargar_imagen(ruta_meta)
        
        # Dibujar cada casilla de la matriz
        for i in range(len(self.ciudad)):
            for j in range(len(self.ciudad[0])):
                x0 = self.margin + j * self.cell_size
                y0 = self.margin + i * self.cell_size
                x1 = x0 + self.cell_size
                y1 = y0 + self.cell_size

                # Definir el color de la casilla según su tipo
                color = "white"
                if self.ciudad[i][j] == 0:
                    color = "white"  # tráfico liviano
                elif self.ciudad[i][j] == 1:
                    color = "#2a2c30"  # muro
                elif self.ciudad[i][j] == 2:
                    color = "yellow"  # punto de partida
                elif self.ciudad[i][j] == 3:
                    color = "#00af38"  # tráfico medio
                elif self.ciudad[i][j] == 4:
                    color = "#af001b"  # tráfico pesado
                elif self.ciudad[i][j] == 5:
                    color = "blue"  # pasajero
                elif self.ciudad[i][j] == 6:
                    color = "white"  # destino

                # Dibujar la casilla
                canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black")

                # Dibujar el icono de inicio, pasajero o destino
                if self.ciudad[i][j] == 2:
                    self.carro = canvas.create_image(x0 + self.cell_size / 2, y0 + self.cell_size / 2, image=self.imagen_vehiculo)
                elif self.ciudad[i][j] == 5:
                    canvas.create_image(x0 + self.cell_size / 2, y0 + self.cell_size / 2, image=self.imagen_pasajero)
                elif self.ciudad[i][j] == 6:
                    canvas.create_image(x0 + self.cell_size / 2, y0 + self.cell_size / 2, image=self.imagen_meta) 
    
    def reset_map(self):
    # Reiniciar el mapa al estado original
        if self.ciudad is not None and self.ciudad.size > 0:
            self.dibujar_mapa(self.city)
        self.nodos_label.config(text="")
        self.profundidad_label.config(text="")
        # self.tiempo_label.config(text="")
        self.costo_label.config(text="")
    
    def desactivar_botones(self):
        """Desactiva todos los botones de los algoritmos."""
        for widget in self.botones_canvas.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(state=tk.DISABLED)

    def activar_botones(self):
        """Activa todos los botones de los algoritmos."""
        for widget in self.botones_canvas.winfo_children(): 
            if isinstance(widget, tk.Button):
                widget.config(state=tk.NORMAL)
                
    def mover_vehiculo(self, ruta, canvas):
        if not hasattr(self, 'carro') or not self.carro or not canvas:
            print("El canvas o el vehículo no existen.")
            return
        
        self.desactivar_botones()  # Desactivar botones al iniciar la animación
        self.recogio_pasajero = False
        
        # Animar los movimientos del vehículo
        for (i, j) in ruta:
            x0 = self.margin + j * self.cell_size
            y0 = self.margin + i * self.cell_size
            
            try:
                # Mover la imagen del vehículo
                canvas.coords(self.carro, x0 + self.cell_size / 2, y0 + self.cell_size / 2)
                canvas.tag_raise(self.carro)
            except _tkinter.TclError:
                print("El canvas ya no es válido.")
                break
            
            if not (i, j) == ruta[0]:  # No dibujar rastro en la primera casilla
                rastro_color = "darkgray" if self.recogio_pasajero else "lightgray"
                x1 = x0 + self.cell_size
                y1 = y0 + self.cell_size
                canvas.create_rectangle(x0, y0, x1, y1, fill=rastro_color, outline="black")

            # Verificar si recogió al pasajero
            if self.ciudad[i][j] == 5:
                self.recogio_pasajero = True

            self.root.update()
            time.sleep(0.6)  # Esperar un poco para ver el movimiento
        self.activar_botones()
        # messagebox.showinfo("Destino alcanzado", "¡Ha llegado a su destino!")

    def mostrar_resultados(self, resultado):
        # Actualizar los valores de las etiquetas con los resultados
        self.nodos_label.config(text=str(resultado["nodos_expandidos"]))
        self.profundidad_label.config(text=str(resultado["profundidad_arbol"]))
        tiempo_ms = resultado['tiempo_computo'] * 1000
        self.tiempo_label.config(text=f"{tiempo_ms:.4f} ms")
        self.costo_label.config(text=str(resultado["costo"]))
        
    def run_amplitud(self):
        if self.ciudad is not None:
            resultado = self.smart_car.busqueda_amplitud(self.ciudad)
            if isinstance(resultado, dict):
                self.mostrar_resultados(resultado)  # Mostrar los resultados adicionales
                self.mover_vehiculo(resultado["ruta"], self.city)  # Mover el vehículo

    def run_costo(self):
        if self.ciudad is not None:
            resultado = self.smart_car.busqueda_costo_uniforme(self.ciudad)
            if isinstance(resultado, dict):
                self.mostrar_resultados(resultado)  # Mostrar los resultados adicionales
                self.mover_vehiculo(resultado["ruta"], self.city)  # Mover el vehículo

    def run_rofundidad(self):
        if self.ciudad is not None:
            resultado = self.smart_car.busqueda_preferente_por_profundidad(self.ciudad)
            if isinstance(resultado, dict):
                self.mostrar_resultados(resultado)  # Mostrar los resultados adicionales
                self.mover_vehiculo(resultado["ruta"], self.city)  # Mover el vehículo

    def run_avara(self):
        if self.ciudad is not None:
            resultado = self.smart_car.busqueda_avara(self.ciudad)
            if isinstance(resultado, dict):
                self.mostrar_resultados(resultado)  # Mostrar los resultados adicionales
                self.mover_vehiculo(resultado["ruta"], self.city)  # Mover el vehículo

    def run_AStar(self):
        if self.ciudad is not None:
            resultado = self.smart_car.busqueda_A_estrella(self.ciudad)
            if isinstance(resultado, dict):
                self.mostrar_resultados(resultado)  # Mostrar los resultados adicionales
                self.mover_vehiculo(resultado["ruta"], self.city)  # Mover el vehículo
    
    
            
        
        


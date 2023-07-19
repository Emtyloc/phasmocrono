import tkinter as tk
from tkinter import font
import keyboard

# Crear la ventana
window = tk.Tk()
window.title("Cronómetro")
window.config(bg="gray")
window.overrideredirect(True)


# Obtener las dimensiones de la pantalla
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Definir el tamaño de la ventana
window_width = 200
window_height = 50

# Calcular la posición de la ventana
window_x = (screen_width - window_width) // 2
window_y = 0

# Establecer la geometría de la ventana
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

# Hacer que la ventana sea transparente
window.wm_attributes("-topmost", True)
window.wm_attributes("-transparentcolor", "black")

fonts = list(font.families())
current_font = 0

# Crear una variable global para el tiempo transcurrido
time_elapsed = 0  # segundos

# Crear una variable global para el estado del cronómetro
timer_active = False

# Global
timer_reset = False

# Crear una variable global para el evento after
after_event = None


# Crear una función que actualice el tiempo cada segundo
def update_time():
    global time_elapsed, timer_active, after_event
    # Si el cronómetro está activo, sumar un segundo y mostrarlo en el label
    if timer_active:
        time_elapsed += 100
        # Formatear el tiempo en minutos, segundos y milisegundos
        minutes = time_elapsed // 60000
        seconds = (time_elapsed % 60000) // 1000
        milliseconds = time_elapsed % 1000
        milliseconds = str(milliseconds)[:1]
        time_str = f"{minutes:01d}:{seconds:02d}:{milliseconds}"
        time_label.config(text=time_str)
        # Llamar a la misma función después de x milisegundo
        after_event = window.after(
            94, update_time
        )  # cada 94 ms se aumentan 100 para compenzar lentitud de ejecucion
        # numero elegido al ojo y con un hardware especifico.


# Crear una función que inicie o pare el cronómetro
def start_stop_timer(event):
    # print(event.scan_code)
    global timer_active, fonts, current_font, timer_reset, time_elapsed
    # print(fonts[current_font])
    # time_label.config(font=(str(fonts[current_font]), 32))
    # current_font += 1
    # Cambiar el estado del cronómetro al opuesto
    if not timer_active:
        reset_time(event)
        time_elapsed = -1
    timer_active = not timer_active
    # Si el cronómetro se activa, llamar a la función update_time
    if timer_active:
        update_time()


# Crear una función que reinicie el tiempo
def reset_time(event):
    global time_elapsed, timer_active, after_event, timer_reset
    # Restablecer el tiempo a 0 segundos y mostrarlo en el label
    time_elapsed = 0
    time_label.config(text="0:00:0")
    # Desactivar el cronómetro y cancelar el evento after si existe
    timer_active = False
    if after_event is not None:
        window.after_cancel(after_event)


# Crear un label para mostrar el tiempo
time_label = tk.Label(
    window,
    text="0:00:0",
    font=("Chiller", 38),
    bg="black",
    fg="white",
    width=165,
    height=50,
    padx=15,
)
time_label.pack()


# Crear una función que se ejecute cuando se cierre la ventana
def on_close(event):
    # Detener after
    if after_event is not None:
        window.after_cancel(after_event)
    # Cerrar la ventana
    window.destroy()


# Asignar la función on_close al evento WM_DELETE_WINDOW de la ventana
window.protocol("WM_DELETE_WINDOW", on_close)

# asociamos shortcuts para el cronometro
keyboard.on_press_key(79, start_stop_timer)
keyboard.on_press_key(81, reset_time)
keyboard.on_press_key(73, on_close)
# keyboard.on_press(start_stop_timer)


# Iniciar el bucle principal de tkinter
window.mainloop()

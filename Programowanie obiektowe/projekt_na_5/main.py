import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def plot_function():
    function_name = function_var.get()
    start = float(entry_start.get())
    end = float(entry_end.get())
    step = float(entry_step.get())

    x = np.arange(start, end, step)
    y = []

    if function_name == "Sin":
        y = np.sin(x)
    elif function_name == "Cos":
        y = np.cos(x)
    elif function_name == "Tan":
        y = np.tan(x)

    ax.clear()
    ax.plot(x, y)
    ax.set_title(f'Plot of {function_name} Function')
    ax.set_xlabel('x')
    ax.set_ylabel(f'{function_name}(x)')
    canvas.draw()

def save_plot():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if file_path:
        fig.savefig(file_path)
        print(f"Plot saved to {file_path}")

def print_plot():
    plt.savefig("temp.png", bbox_inches="tight")
    print("Plot sent to printer")

# Tworzenie interfejsu użytkownika
root = tk.Tk()
root.title("Trigonometric Functions Plotter")

frame = ttk.Frame(root, padding="10")
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

function_label = ttk.Label(frame, text="Select Function:")
function_label.grid(column=0, row=0, sticky=tk.W)

function_var = tk.StringVar()
function_combobox = ttk.Combobox(frame, textvariable=function_var, values=["Sin", "Cos", "Tan"])
function_combobox.grid(column=1, row=0, sticky=tk.W)
function_combobox.set("Sin")

start_label = ttk.Label(frame, text="Start:")
start_label.grid(column=0, row=1, sticky=tk.W)
entry_start = ttk.Entry(frame)
entry_start.grid(column=1, row=1, sticky=tk.W)
entry_start.insert(0, "-10")

end_label = ttk.Label(frame, text="End:")
end_label.grid(column=0, row=2, sticky=tk.W)
entry_end = ttk.Entry(frame)
entry_end.grid(column=1, row=2, sticky=tk.W)
entry_end.insert(0, "10")

step_label = ttk.Label(frame, text="Step:")
step_label.grid(column=0, row=3, sticky=tk.W)
entry_step = ttk.Entry(frame)
entry_step.grid(column=1, row=3, sticky=tk.W)
entry_step.insert(0, "0.1")

plot_button = ttk.Button(frame, text="Plot", command=plot_function)
plot_button.grid(column=0, row=4, columnspan=2)

save_button = ttk.Button(frame, text="Save Plot", command=save_plot)
save_button.grid(column=0, row=5, columnspan=2)

print_button = ttk.Button(frame, text="Print Plot", command=print_plot)
print_button.grid(column=0, row=6, columnspan=2)

# Inicjalizacja wykresu
fig, ax = plt.subplots(figsize=(6, 4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(column=1, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Uruchomienie interfejsu użytkownika
root.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datatest  # из задания №1
from datetime import datetime
import os

# Определяем числовые колонки исключаем категориальные
CATEGORICAL_COLS = ['anaemia', 'diabetes', 'high bp']
NUMERIC_COLS = [col for col in datatest.df.columns if col not in CATEGORICAL_COLS]

# Маркер для отображения точек
MARKER = 'o'

class ScatterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Визуализация данных - Scatter Plot")
        self.root.geometry("800x650")

        self.x_col = NUMERIC_COLS[0]
        self.y_col = NUMERIC_COLS[1] if len(NUMERIC_COLS) > 1 else NUMERIC_COLS[0]

        self.x_buttons = []
        self.y_buttons = []

        self.create_widgets()
        self.update_plot()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        # Левая панель
        left_frame = ttk.Frame(main_frame, width=100)
        left_frame.grid(row=0, column=0, sticky='ns', padx=5, pady=5)
        left_frame.grid_propagate(False)

        ttk.Label(left_frame, text="Ось Y", font=('Arial', 10, 'bold')).pack(pady=5)

        for col in NUMERIC_COLS:
            btn = tk.Button(left_frame, text=col, width=15,
                            command=lambda c=col: self.select_y(c))
            btn.pack(pady=2)
            self.y_buttons.append(btn)

        canvas_frame = ttk.Frame(main_frame)
        canvas_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=canvas_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Нижняя панель
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.grid(row=1, column=0, columnspan=2, sticky='ew', padx=5, pady=5)

        ttk.Label(bottom_frame, text="Ось X", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)

        for col in NUMERIC_COLS:
            btn = tk.Button(bottom_frame, text=col, width=12,
                            command=lambda c=col: self.select_x(c))
            btn.pack(side=tk.LEFT, padx=2)
            self.x_buttons.append(btn)

        # Кнопка сохранения
        save_btn = tk.Button(bottom_frame, text="Сохранить график", command=self.save_plot,
                             bg='lightgreen', width=15)
        save_btn.pack(side=tk.RIGHT, padx=10)

        self.highlight_buttons()

    def select_x(self, col):
        """Выбор колонки для оси X."""
        self.x_col = col
        self.highlight_buttons()
        self.update_plot()

    def select_y(self, col):
        """Выбор колонки для оси Y."""
        self.y_col = col
        self.highlight_buttons()
        self.update_plot()

    def highlight_buttons(self):
        for btn in self.x_buttons:
            if btn['text'] == self.x_col:
                btn.config(bg='lightblue', relief=tk.SUNKEN)
            else:
                btn.config(bg='SystemButtonFace', relief=tk.RAISED)

        for btn in self.y_buttons:
            if btn['text'] == self.y_col:
                btn.config(bg='lightblue', relief=tk.SUNKEN)
            else:
                btn.config(bg='SystemButtonFace', relief=tk.RAISED)

    def update_plot(self):
        x_data = datatest.df[self.x_col]
        y_data = datatest.df[self.y_col]

        self.ax.clear()
        self.ax.scatter(x_data, y_data, marker=MARKER, color='blue', alpha=0.6, edgecolors='k')
        self.ax.set_xlabel(self.x_col)
        self.ax.set_ylabel(self.y_col)
        self.ax.set_title(f'Зависимость {self.y_col} от {self.x_col}')

        self.canvas.draw()

    def save_plot(self):
        """Сохранение графика."""
        now = datetime.now()
        filename = f"graph{now.hour:02d}_{now.minute:02d}_{now.second:02d}.png"
        filepath = os.path.join(os.getcwd(), filename)
        self.figure.savefig(filepath, dpi=100, bbox_inches='tight')
        messagebox.showinfo("Сохранение", f"График сохранён как:\n{filepath}")

if __name__ == '__main__':
    root = tk.Tk()
    app = ScatterApp(root)
    root.mainloop()
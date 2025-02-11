import tkinter as tk
from itertools import permutations, combinations

class ShiftScheduler:
    def __init__(self):
        self.shifts_with_2_men = set(permutations("MMWWWWWW", 8))
        self.shifts_with_3_men = set(permutations("MMMWWWWW", 8))
        self.shifts_with_4_men = set(permutations("MMMMWWWW", 8))
        
        self.possible_shifts = list(self.shifts_with_2_men | self.shifts_with_3_men | self.shifts_with_4_men)
        
        self.valid_schedules = []
        self.optimized_schedules = []

    def generate_valid_schedules(self):
        self.valid_schedules = [
            schedule for schedule in combinations(self.possible_shifts, 3)
            if sum(shift.count("M") for shift in schedule) == 8
        ]
    
    def filter_optimized_schedules(self):
        self.optimized_schedules = [
            schedule for schedule in self.valid_schedules
            if all("MM" not in "".join(shift) for shift in schedule)
        ]

    def display_schedules(self, schedules, label="Обычная комбинация", max_schedules=10):
        output = ""
        for i, schedule in enumerate(schedules[:max_schedules], 1):
            output += f'{label} {i}:\n'
            for j, shift in enumerate(schedule, 1):
                output += f'  Смена {j}: {"".join(shift)}\n'
            output += '\n'
        return output


def start_process():
    global is_running
    if is_running:
        return  
    
    try:
        max_combinations = int(entry_max_combinations.get())
        if max_combinations <= 0:
            raise ValueError("Число должно быть больше 0.")
    except ValueError:
        max_combinations = 10  

    is_running = True
    scheduler.generate_valid_schedules()

    output = f"Всего {len(scheduler.valid_schedules)} допустимых расписаний.\n"
    output += scheduler.display_schedules(scheduler.valid_schedules, "Обычная комбинация", max_combinations)

    output_text.delete(1.0, tk.END)  
    output_text.insert(tk.END, output)  

    scheduler.filter_optimized_schedules()

    output_optimized = f"\nВсего {len(scheduler.optimized_schedules)} оптимизированных расписаний (без подряд идущих мужчин).\n"
    output_optimized += scheduler.display_schedules(scheduler.optimized_schedules, "Оптимизированная комбинация", max_combinations)

    output_text.insert(tk.END, output_optimized)  
    is_running = False


def stop_process():
    global is_running
    is_running = False
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "Генерация остановлена.")


root = tk.Tk()
root.title("Конвейер сборки")

label_max_combinations = tk.Label(root, text="Максимальное количество комбинаций для вывода:")
label_max_combinations.pack()

entry_max_combinations = tk.Entry(root)
entry_max_combinations.pack()

button_start = tk.Button(root, text="Начать", command=start_process)
button_start.pack()

button_stop = tk.Button(root, text="Стоп", command=stop_process)
button_stop.pack()

output_text = tk.Text(root, height=20, width=80, wrap="word", bd=3, relief="sunken")
output_text.pack()

scheduler = ShiftScheduler()

is_running = False

root.mainloop()

import threading
import multiprocessing
import time
import random
import os
import tkinter as tk
from tkinter import ttk


class Philosopher(threading.Thread):
    def __init__(self, name, left_fork, right_fork, status_var):
        threading.Thread.__init__(self)
        self.name = name
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.status_var = status_var

    def run(self):
        while True:
            self.status_var.set(f"{self.name} myśli.")
            time.sleep(random.uniform(1, 3))
            self.status_var.set(f"{self.name} jest głodny.")
            self.dine()

    def dine(self):
        fork1, fork2 = self.left_fork, self.right_fork

        while True:
            fork1.acquire(True)
            locked = fork2.acquire(False)
            if locked: break
            fork1.release()
            self.status_var.set(f"{self.name} zmienia widelec.")
            fork1, fork2 = fork2, fork1
            time.sleep(random.uniform(1, 3))

        self.status_var.set(f"{self.name} je.")
        time.sleep(random.uniform(1, 3))
        fork2.release()
        fork1.release()


def process_file(file_path):
    print(f"Przetwarzanie pliku: {file_path}")
    with open(file_path, 'r') as file:
        data = file.read()
        # Symulacja przetwarzania
        time.sleep(random.uniform(0.1, 0.5))
    print(f"Zakończono przetwarzanie pliku: {file_path}")
    return len(data)


def concurrent_processing(file_paths, num_processes, status_var):
    status_var.set(f"Przetwarzanie plików z {num_processes} procesami...")
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.map(process_file, file_paths)
    status_var.set(f"Zakończono przetwarzanie plików.")
    return results


def start_processing(num_processes, status_var):
    num_files = 10
    file_paths = [f"file_{i}.txt" for i in range(num_files)]

    # Tworzenie przykładowych plików
    for file_path in file_paths:
        with open(file_path, 'w') as file:
            file.write("A" * random.randint(1000, 10000))

    # Przetwarzanie plików
    start_time = time.time()
    results = concurrent_processing(file_paths, num_processes, status_var)
    end_time = time.time()

    status_var.set(f"Czas przetwarzania: {end_time - start_time:.2f} sekundy. Wyniki: {results}")

    # Usuwanie przykładowych plików
    for file_path in file_paths:
        os.remove(file_path)


def main():
    # Tworzenie GUI
    root = tk.Tk()
    root.title("Filozofowie i Przetwarzanie Plików")

    main_frame = ttk.Frame(root, padding="10")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    status_vars = []
    for i in range(5):
        status_var = tk.StringVar()
        status_vars.append(status_var)
        ttk.Label(main_frame, textvariable=status_var).grid(row=i, column=0, sticky=(tk.W, tk.E))

    # Tworzenie widelców
    forks = [threading.Lock() for _ in range(5)]
    philosophers = [Philosopher(f"Filozof {i + 1}", forks[i], forks[(i + 1) % 5], status_vars[i]) for i in range(5)]

    # Startowanie filozofów
    for philosopher in philosophers:
        philosopher.start()

    process_status_var = tk.StringVar()
    ttk.Label(main_frame, textvariable=process_status_var).grid(row=5, column=0, sticky=(tk.W, tk.E))

    def on_start_processing():
        num_processes = int(processes_entry.get())
        threading.Thread(target=start_processing, args=(num_processes, process_status_var)).start()

    ttk.Label(main_frame, text="Liczba procesów:").grid(row=6, column=0, sticky=tk.W)
    processes_entry = ttk.Entry(main_frame)
    processes_entry.grid(row=6, column=1, sticky=(tk.W, tk.E))
    processes_entry.insert(0, "4")

    ttk.Button(main_frame, text="Rozpocznij przetwarzanie", command=on_start_processing).grid(row=7, column=0,
                                                                                              columnspan=2)

    root.mainloop()


if __name__ == "__main__":
    main()

import multiprocessing
import time
import matplotlib.pyplot as plt

def parallel_processing(file_paths, num_processes):
    start_time = time.time()
    with multiprocessing.Pool(num_processes) as pool:
        results = pool.map(process_file, file_paths)
    end_time = time.time()
    return end_time - start_time, results

# Lista plików do przetwarzania
file_paths = [f"data_file_{i}.txt" for i in range(10)]

# Pomiar czasu przetwarzania dla różnych liczby procesów
num_processes_list = [1, 2, 4, 8]
times = []

for num_processes in num_processes_list:
    duration, _ = parallel_processing(file_paths, num_processes)
    times.append(duration)
    print(f"Number of processes: {num_processes}, Time taken: {duration:.2f} seconds")

# Wykres
plt.plot(num_processes_list, times, marker='o')
plt.xlabel("Number of Processes")
plt.ylabel("Time Taken (seconds)")
plt.title("Time Taken for Parallel Processing of Files")
plt.show()

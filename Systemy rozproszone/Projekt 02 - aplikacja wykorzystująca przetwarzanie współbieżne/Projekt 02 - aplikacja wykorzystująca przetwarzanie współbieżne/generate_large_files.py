import os

def generate_large_files(num_files, lines_per_file):
    for i in range(num_files):
        with open(f"data_file_{i}.txt", "w") as f:
            for _ in range(lines_per_file):
                f.write("This is a line of sample text data.\n")

# Generujemy 10 plików po 100000 linii każdy
generate_large_files(10, 100000)

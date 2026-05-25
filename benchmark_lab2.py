import subprocess
import time
import numpy as np
import matplotlib.pyplot as plt
import os

# Параметры
executable = "./matrix_mult.exe"
sizes = [200, 400, 800, 1200, 1600, 2000]   # размеры матриц
threads_list = [1, 2, 4, 8]                 # число потоков (если CPU 8 ядер)
repeats = 3

results = {t: [] for t in threads_list}

print("=== Вторая лабораторная: исследование масштабируемости ===")
for n in sizes:
    print(f"\nРазмер {n}×{n}")
    # Генерируем матрицы, если их нет
    if not os.path.exists(f"A_{n}.txt"):
        subprocess.run(["python", "generate.py", str(n), f"A_{n}.txt", f"B_{n}.txt"], check=True)
    
    for t in threads_list:
        times = []
        for _ in range(repeats):
            start = time.perf_counter()
            subprocess.run([executable, f"A_{n}.txt", f"B_{n}.txt", f"C_{n}_t{t}.txt", str(t)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            end = time.perf_counter()
            times.append(end - start)
        avg_time = np.mean(times)
        results[t].append(avg_time)
        print(f"  Потоков {t}: {avg_time:.4f} с")

# --- Таблица ---
print("\n" + "="*80)
print("Время выполнения (секунды):")
print("n\t" + "\t".join([f"{t} потоков" for t in threads_list]))
for i, n in enumerate(sizes):
    row = f"{n}\t" + "\t".join([f"{results[t][i]:.4f}" for t in threads_list])
    print(row)

# --- Ускорение (Speedup) ---
speedup = {t: [] for t in threads_list if t != 1}
for t in threads_list:
    if t == 1: continue
    speedup[t] = [results[1][i] / results[t][i] for i in range(len(sizes))]

# --- Эффективность (Efficiency = Speedup / p) ---
efficiency = {t: [speedup[t][i] / t for i in range(len(sizes))] for t in speedup}

# --- График времени ---
plt.figure(figsize=(10,6))
for t in threads_list:
    plt.plot(sizes, results[t], marker='o', label=f"{t} потоков")
plt.xlabel("Размер матрицы n")
plt.ylabel("Время (сек)")
plt.title("Время умножения матриц от размера и числа потоков")
plt.legend()
plt.grid(True)
plt.savefig("lab2_time.png")
plt.show()

# --- График ускорения ---
plt.figure(figsize=(10,6))
for t in speedup:
    plt.plot(sizes, speedup[t], marker='s', label=f"{t} потоков")
plt.plot(sizes, sizes, 'k--', label="Идеальное ускорение (линейное)")
plt.xlabel("Размер матрицы n")
plt.ylabel("Ускорение (T1 / Tp)")
plt.title("Ускорение параллельной версии")
plt.legend()
plt.grid(True)
plt.savefig("lab2_speedup.png")
plt.show()

# --- График эффективности ---
plt.figure(figsize=(10,6))
for t in efficiency:
    plt.plot(sizes, efficiency[t], marker='d', label=f"{t} потоков")
plt.xlabel("Размер матрицы n")
plt.ylabel("Эффективность (Speedup / p)")
plt.title("Эффективность параллелизации")
plt.legend()
plt.grid(True)
plt.savefig("lab2_efficiency.png")
plt.show()

# Вывод таблицы ускорения
print("\nУскорение (Speedup):")
print("n\t" + "\t".join([f"{t} потоков" for t in speedup.keys()]))
for i, n in enumerate(sizes):
    row = f"{n}\t" + "\t".join([f"{speedup[t][i]:.2f}" for t in speedup.keys()])
    print(row)
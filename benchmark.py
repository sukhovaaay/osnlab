import subprocess
import time
import numpy as np
import matplotlib.pyplot as plt
import os

# Настройки
executable = "./matrix_mult.exe"   # имя вашей программы
sizes = [100, 200, 400, 600, 800, 1000]   # размеры матриц
threads_list = [1, 2, 4, 8]               # число потоков
repeats = 3                                 # сколько раз повторять для усреднения

results = {t: [] for t in threads_list}

print("Запуск бенчмарка...")
for n in sizes:
    print(f"\nРазмер {n}×{n}")
    # Генерируем матрицы, если их ещё нет
    if not os.path.exists(f"A_{n}.txt") or not os.path.exists(f"B_{n}.txt"):
        print(f"  Генерация A_{n}.txt и B_{n}.txt...")
        subprocess.run(["python", "generate.py", str(n), f"A_{n}.txt", f"B_{n}.txt"], check=True)
    
    for t in threads_list:
        times = []
        for rep in range(repeats):
            start = time.perf_counter()
            subprocess.run([executable, f"A_{n}.txt", f"B_{n}.txt", f"C_{n}_t{t}.txt", str(t)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            end = time.perf_counter()
            times.append(end - start)
        avg_time = np.mean(times)
        results[t].append(avg_time)
        print(f"  Потоков {t}: {avg_time:.4f} с (за {repeats} запусков)")

# Построение графика времени выполнения
plt.figure(figsize=(10,6))
for t in threads_list:
    plt.plot(sizes, results[t], marker='o', label=f"{t} потоков")
plt.xlabel("Размер матрицы n")
plt.ylabel("Время (сек)")
plt.title("Зависимость времени умножения матриц от размера и числа потоков")
plt.legend()
plt.grid(True)
plt.savefig("benchmark_time.png")
plt.show()

# Построение графика ускорения (speedup) относительно 1 потока
plt.figure(figsize=(10,6))
for t in threads_list:
    if t == 1: continue
    speedup = [results[1][i] / results[t][i] for i in range(len(sizes))]
    plt.plot(sizes, speedup, marker='s', label=f"{t} потоков")
plt.plot(sizes, [1]*len(sizes), 'k--', label="Идеальное ускорение (1x)")
plt.xlabel("Размер матрицы n")
plt.ylabel("Ускорение (T1 / Tp)")
plt.title("Ускорение параллельной версии")
plt.legend()
plt.grid(True)
plt.savefig("benchmark_speedup.png")
plt.show()

# Вывод таблицы результатов
print("\n" + "="*60)
print("РЕЗУЛЬТАТЫ (время в секундах):")
print("n\t" + "\t".join([f"{t} потоков" for t in threads_list]))
for i, n in enumerate(sizes):
    row = f"{n}\t" + "\t".join([f"{results[t][i]:.4f}" for t in threads_list])
    print(row)
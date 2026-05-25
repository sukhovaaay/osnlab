import sys
import numpy as np

def read_matrix(filename):
    with open(filename, 'r') as f:
        n = int(f.readline().strip())
        # считываем все числа из файла (могут быть разбиты по строкам)
        data = list(map(float, f.read().split()))
    if len(data) != n * n:
        raise ValueError(f"Количество элементов в {filename} не равно {n}×{n}")
    return n, np.array(data).reshape(n, n)

def main():
    if len(sys.argv) != 4:
        print("Usage: python verify.py <A_file> <B_file> <C_file>")
        sys.exit(1)
    
    n1, A = read_matrix(sys.argv[1])
    n2, B = read_matrix(sys.argv[2])
    n3, C = read_matrix(sys.argv[3])
    
    if n1 != n2 or n1 != n3:
        print("Размеры матриц не совпадают")
        sys.exit(1)
    
    expected = np.dot(A, B)
    if np.allclose(C, expected, rtol=1e-3, atol=1e-6):
        print("Верификация ПРОЙДЕНА: результаты совпадают.")
    else:
        diff = np.abs(C - expected)
        print(f"Верификация НЕ ПРОЙДЕНА. Макс. расхождение: {np.max(diff)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
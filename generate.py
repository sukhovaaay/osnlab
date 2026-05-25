import sys
import numpy as np

def main():
    if len(sys.argv) != 4:
        print("Usage: python generate.py <n> <file_A> <file_B>")
        sys.exit(1)
    n = int(sys.argv[1])
    A = np.random.rand(n, n)
    B = np.random.rand(n, n)
    with open(sys.argv[2], 'w') as f:
        f.write(f"{n}\n")
        np.savetxt(f, A, fmt='%.6f')
    with open(sys.argv[3], 'w') as f:
        f.write(f"{n}\n")
        np.savetxt(f, B, fmt='%.6f')
    print(f"Сгенерированы матрицы {n}×{n}")

if __name__ == "__main__":
    main()
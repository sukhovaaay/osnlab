#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>
#include <omp.h>
#include <cmath>
#include <cstdlib>

using namespace std;

// Чтение матрицы из текстового файла
bool readMatrix(const string& filename, vector<double>& data, int& n) {
    ifstream fin(filename);
    if (!fin.is_open()) {
        cerr << "Ошибка открытия файла: " << filename << endl;
        return false;
    }
    fin >> n;
    if (n <= 0) {
        cerr << "Неверный размер матрицы" << endl;
        return false;
    }
    size_t size = n * n;
    data.resize(size);
    for (size_t i = 0; i < size; ++i) {
        fin >> data[i];
        if (fin.fail()) {
            cerr << "Ошибка чтения данных из файла" << endl;
            return false;
        }
    }
    fin.close();
    return true;
}

// Запись матрицы в текстовый файл
bool writeMatrix(const string& filename, const vector<double>& data, int n) {
    ofstream fout(filename);
    if (!fout.is_open()) {
        cerr << "Ошибка создания файла: " << filename << endl;
        return false;
    }
    fout << n << endl;
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            fout << data[i * n + j];
            if (j != n - 1) fout << " ";
        }
        fout << endl;
    }
    fout.close();
    return true;
}

// Параллельное умножение матриц C = A * B
void multiplyMatrices(const vector<double>& A, const vector<double>& B,
                      vector<double>& C, int n, int num_threads) {
    omp_set_num_threads(num_threads);
    fill(C.begin(), C.end(), 0.0);
    
    #pragma omp parallel for collapse(2) schedule(static)
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            double sum = 0.0;
            for (int k = 0; k < n; ++k) {
                sum += A[i * n + k] * B[k * n + j];
            }
            C[i * n + j] = sum;
        }
    }
}

int main(int argc, char* argv[]) {
    if (argc < 4) {
        cerr << "Использование: " << argv[0]
             << " <файл_A> <файл_B> <выходной_файл> [число_потоков]" << endl;
        return 1;
    }
    
    string fileA = argv[1];
    string fileB = argv[2];
    string fileC = argv[3];
    int num_threads = (argc >= 5) ? atoi(argv[4]) : omp_get_max_threads();
    
    vector<double> A, B, C;
    int nA, nB;
    
    if (!readMatrix(fileA, A, nA)) return 1;
    if (!readMatrix(fileB, B, nB)) return 1;
    if (nA != nB) {
        cerr << "Размеры матриц не совпадают" << endl;
        return 1;
    }
    int n = nA;
    C.resize(n * n);
    
    double start = omp_get_wtime();
    multiplyMatrices(A, B, C, n, num_threads);
    double end = omp_get_wtime();
    double elapsed = end - start;
    
    size_t elem_count = 3 * (size_t)n * n;   // A + B + C
    size_t memory_bytes = elem_count * sizeof(double);
    
    cout << "Время выполнения: " << elapsed << " секунд" << endl;
    cout << "Размер матрицы: " << n << " x " << n << endl;
    cout << "Количество элементов (A+B+C): " << elem_count << endl;
    cout << "Объем памяти: " << memory_bytes << " байт (~"
         << memory_bytes / (1024.0 * 1024.0) << " MB)" << endl;
    cout << "Использовано потоков: " << num_threads << endl;
    
    if (!writeMatrix(fileC, C, n)) return 1;
    cout << "Результат записан в файл " << fileC << endl;
    
    return 0;
}
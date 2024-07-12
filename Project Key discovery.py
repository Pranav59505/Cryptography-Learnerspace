def minor_matrix(matrix, i, j):
    return [row[:j] + row[j + 1:] for row in (matrix[:i] + matrix[i + 1:])]


def determinant_matrix(matrix):
    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    determinant = 0
    for c in range(len(matrix)):
        determinant += ((-1) ** c) * matrix[0][c] * determinant_matrix(minor_matrix(matrix, 0, c))
    return determinant


def mod_inv(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError(f"No modular inverse for {a} under modulus {m}")


def inverse(matrix, modulus=26):
    determinant = determinant_matrix(matrix) % modulus
    if determinant == 0:
        raise ValueError("Matrix is not invertible")

    det_inv = mod_inv(determinant, modulus)

    # Special case for 2x2 matrix
    if len(matrix) == 2:
        return [[matrix[1][1] * det_inv % modulus, -matrix[0][1] * det_inv % modulus],
                [-matrix[1][0] * det_inv % modulus, matrix[0][0] * det_inv % modulus]]

    # Find matrix of cofactors
    cofactors = []
    for r in range(len(matrix)):
        cofactor_row = []
        for c in range(len(matrix)):
            minor = minor_matrix(matrix, r, c)
            cofactor_row.append(((-1) ** (r + c)) * determinant_matrix(minor) % modulus)
        cofactors.append(cofactor_row)

    cofactors = list(map(list, zip(*cofactors)))  # Transpose matrix
    for r in range(len(cofactors)):
        for c in range(len(cofactors[r])):
            cofactors[r][c] = (cofactors[r][c] * det_inv) % modulus

    return cofactors


def multiply_matrices(A, B, modulus=26):
    rows_A = len(A)
    cols_A = len(A[0])
    cols_B = len(B[0])
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]

    # Perform matrix multiplication
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
            result[i][j] %= modulus  # Ensure result is within modulo

    return result


def char_to_num(x):  # Converting characters into numbers
    return ord(x) - 65


plaintext = str(input())
ciphertext = str(input())

l = len(plaintext)
m = len(ciphertext)

Plaintext_Matrix = [[] for _ in range(l // 3)]
Ciphertext_Matrix = [[] for _ in range(m // 3)]

for i in range(l // 3):
    for j in range(3):
        Plaintext_Matrix[i].append(char_to_num(plaintext[i * 3 + j]))

for i in range(m // 3):
    for j in range(3):
        Ciphertext_Matrix[i].append(char_to_num(ciphertext[i * 3 + j]))

Plaintext_Matrix = list(map(list, zip(*Plaintext_Matrix)))  # Transpose plaintext matrix to fit multiplication
Key_Matrix = multiply_matrices(Ciphertext_Matrix, inverse(Plaintext_Matrix))

print("Key matrix:")
for row in Key_Matrix:
    print(" ".join(chr(int(num) + ord('A')) for num in row))

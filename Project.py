# Encryption
plaintext = str(input())
key = str(input())
if len(plaintext) % 3 == 1:
    plaintext = plaintext + "XX"  # padding 2 characters to make plaintext multiple of key size
elif len(plaintext) % 3 == 2:
    plaintext = plaintext + "X"  # padding 1 character to make plaintext multiple of key size
l = len(plaintext)
KeyMatrix = [[] for _ in range(3)]
Plaintext_Matrix = [[] for _ in range(l // 3)]


def char_to_num(x):  # Converting characters into numbers
    return ord(x) -65

for i in range(3):
    for j in range(3):
        KeyMatrix[i].append(char_to_num(key[i * 3 + j]))  # Making Key Matrix
for i in range(l // 3):
    for j in range(3):
        Plaintext_Matrix[i].append(char_to_num(plaintext[i * 3 + j]))


def Multiplication(A, B):
    rows_A = len(KeyMatrix)
    cols_A = len(KeyMatrix[0])
    cols_B = len(Plaintext_Matrix)
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]

    # Perform matrix multiplication
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += KeyMatrix[i][k] * Plaintext_Matrix[j][k]

    return result


Ciphertext = ''
for rows in Multiplication(KeyMatrix, Plaintext_Matrix):
    for i in range(l // 3):
        Ciphertext = Ciphertext + chr(rows[i] % 26 + ord('A'))
print(Ciphertext)

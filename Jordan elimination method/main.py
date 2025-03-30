def gaussJordanElimination(matrix, constants):
    n = len(matrix)

    for i in range(n):
        matrix[i].append(constants[i])

    for i in range(n):
        if matrix[i][i] == 0:
            for k in range(i + 1, n):
                if matrix[k][i] != 0:
                    matrix[i], matrix[k] = matrix[k], matrix[i]
                    k = n

        pivot = matrix[i][i]
        if pivot == 0:
            raise ValueError("Matrix is singular and cannot be solved.")

        for j in range(n + 1):
            matrix[i][j] /= pivot

        for k in range(n):
            if k != i:
                factor = matrix[k][i]
                for j in range(n + 1):
                    matrix[k][j] -= factor * matrix[i][j]


    solution = []
    for i in range(n):
        solution.append(matrix[i][-1])

    return solution


with open("matrix.txt", "r") as file:
    lines = file.readlines()
    matrix = []
    constantColumn = []

    for i in range(len(lines)):
        row = lines[i].strip().split(",")
        if i != len(lines) - 2 and i != len(lines) - 1:
            rowValues = []
            for j in range(len(row)):
                rowValues.append(float(row[j]))
            matrix.append(rowValues)
        elif i == len(lines) - 1:
            for j in range(len(row)):
                constantColumn.append(float(row[j]))


print(constantColumn)
print(matrix)


solution = gaussJordanElimination(matrix, constantColumn)

print("Solution:", solution)

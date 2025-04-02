def gaussJordanElimination(matrix, constants):
    n = len(matrix)

    for i in range(n):
        matrix[i].append(constants[i])

    rank = 0
    for col in range(n):
        pivot_row = None
        flag = False

        for row in range(rank, n):
            if not flag and abs(matrix[row][col]) > 1e-10:
                pivot_row = row
                flag = True


        if pivot_row is not None:

            if pivot_row != rank:
                matrix[rank], matrix[pivot_row] = matrix[pivot_row], matrix[rank]

            pivot = matrix[rank][col]
            for j in range(col, n + 1):
                matrix[rank][j] /= pivot

            for row in range(n):
                if row != rank and abs(matrix[row][col]) > 1e-10:
                    factor = matrix[row][col]
                    for j in range(col, n + 1):
                        matrix[row][j] -= factor * matrix[rank][j]

            rank += 1

    for row in range(rank, n):
        if abs(matrix[row][-1]) > 1e-10:
            return None

    if rank < n:
        return "Nieoznaczony"

    solution = []
    for i in range(n):
        solution.append(matrix[i][-1])

    return solution


with open("j.txt", "r") as file:
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

solution = gaussJordanElimination(matrix, constantColumn)

if solution is None:
    print("Układ jest sprzeczny - brak rozwiązań.")
elif solution == "Nieoznaczony":
    print("Układ jest nieoznaczony - nieskończenie wiele rozwiązań.")
else:
    print("Rozwiązanie:", solution)
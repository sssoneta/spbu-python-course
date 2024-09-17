# Operation on vectors

def the_scalar_product_of_vectors(vector_1, vector_2):
    """
    Функция the_scalar_product_of_vectors проверяет, имеют ли векторы одинаковую длину. Если нет, она возвращает None.
    В противном случае, функция вычисляет скалярное произведение, перемножая соответствующие элементы векторов и суммируя результаты.
    Параметры:
        vector_1 (list): Первый вектор, представленный в виде списка чисел.
        vector_2 (list): Второй вектор, представленный в виде списка чисел.
    Возвращаемое значение:
        int: Скалярное произведение векторов vector_1 и vector_2, если они имеют одинаковую длину.
        None: Если векторы имеют разную длину.
    """
    if len(vector_1) != len(vector_2):
        return None
    else:
        p = 0
        for i in range(len(vector_1)):
            p += vector_1[i] * vector_2[i]
        return p


def vector_length(vector):
    """"
    Функция vector_length вычисляет длину вектора, представленного в виде списка чисел.
    Параметры:
    vector (list): Вектор, представленный в виде списка чисел.
    Возвращаемое значение:
        int: Длина вектора, округленная до целого числа
     """
    s = 0
    for i in vector:
        s += i**2
    return int(pow(s, 0.5))


def the_angle_between_the_vectors(vector_1, vector_2):
    """
    Функция the_angle_between_the_vectors вычисляет угол между двумя векторами,
    заданными в виде списков чисел, используя скалярное произведение и длины векторов.
    Параметры:
    vector_1 (list): Первый вектор, представленный в виде списка чисел.
    vector_2 (list): Второй вектор, представленный в виде списка чисел.
    Возвращаемое значение:
    float: Угол между векторами в радианах, c точностью до двух знаков после запятой.

    """
    s = the_scalar_product_of_vectors(vector_1, vector_2)
    angle = s / (vector_length(vector_1)*vector_length(vector_2))
    return round(angle, 2)


# Operations on matrices


def matrix_addition(matrix_1, matrix_2):
    if len(matrix_1) != len(matrix_2) or len(matrix_1[0]) != len(matrix_2[0]):
        return None
    else:
        matrix_sum = [[0]*len(matrix_1[0]) for i in range(len(matrix_1))]
        for i in range(len(matrix_1)):
            for j in range(len(matrix_1[0])):
                matrix_sum[i][j] = matrix_1[i][j] + matrix_2[i][j]
        return matrix_sum


def matrix_multiplication(matrix_1, matrix_2):
    if len(matrix_1[0]) != len(matrix_2):
        return None
    else:
        matrix_mult = [[0]*len(matrix_2[0]) for i in range(len(matrix_1))]
        for i in range(len(matrix_1)):
            for j in range(len(matrix_2[0])):
                for r in range(len(matrix_2)):
                    matrix_mult[i][j] += int(matrix_1[i][r]) * int(matrix_2[r][j])
        return matrix_mult


def matrix_transposition(matrix):
    matrix_trans = [[0]*len(matrix) for i in range(len(matrix[0]))]
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            matrix_trans[j][i] = matrix[i][j]
    return matrix_trans



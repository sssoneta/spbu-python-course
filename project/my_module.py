# Operation on vectors

from math import pi, acos
def the_scalar_product_of_vectors(vector_1, vector_2):
    """
    Function the_scalar_product_of_vectors checks whether the vectors have the same length. If not, it returns None.
    Otherwise, the function calculates the scalar product by multiplying the corresponding elements of the vectors
    and summing the results.
    Parameters:
    vector_1 (list): The first vector, represented as a list of numbers.
    vector_2 (list): The second vector, represented as a list of numbers.
    Return value:
    int: The scalar product of vectors vector_1 and vector_2, if they have the same length.
    None: If the vectors have different lengths.

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
    The vector_length function calculates the length of a vector represented as a list of numbers.
    Parameters:
    vector (list): A vector represented as a list of numbers.
    Return value:
    int: The length of the vector, rounded to an integer

    """
    s = 0
    for i in vector:
        s += i**2
    return round(pow(s, 0.5), 2)


def the_angle_between_the_vectors(vector_1, vector_2):
    """
    The_angle_between_the_vectors function calculates the angle between two vectors
    given as lists of numbers using the scalar product and the lengths of the vectors.
    Parameters:
    vector_1 (list): The first vector, represented as a list of numbers.
    vector_2 (list): The second vector, represented as a list of numbers.
    Return value:
    float: The angle between the vectors in radians, with an accuracy of two decimal places.

    """
    s = the_scalar_product_of_vectors(vector_1, vector_2)
    angle = s / (vector_length(vector_1) * vector_length(vector_2))
    print(s, vector_length(vector_1), vector_length(vector_2))
    angle = acos(angle)*180/pi
    return round(angle)


# Operations on matrices


def matrix_addition(matrix_1, matrix_2):
    """
    Adds two matrices together.
    Args:
    matrix_1 (list of lists): The first matrix.
    matrix_2 (list of lists): The second matrix.
    Returns:
    list of lists: The sum of the two matrices, or None if the matrices have
    different dimensions.
    Raises:
    TypeError: If either input is not a list of lists.
    """
    if len(matrix_1) != len(matrix_2) or len(matrix_1[0]) != len(matrix_2[0]):
        return None
    else:
        matrix_sum = [[0]*len(matrix_1[0]) for _ in range(len(matrix_1))]
        for i in range(len(matrix_1)):
            for j in range(len(matrix_1[0])):
                matrix_sum[i][j] = matrix_1[i][j] + matrix_2[i][j]
        return matrix_sum


def matrix_multiplication(matrix_1, matrix_2):
    """
    The matrix_multiplication function multiplies two matrices represented as nested lists.
    Parameters:
    matrix_1 (list of lists): The first matrix.
    matrix_2 (list of lists): The second matrix.
    Return value:
    list of lists: The product of two matrices if the number of columns in the first matrix is equal to the number of rows in the second matrix.
    None: If the number of columns in the first matrix is not equal to the number of rows in the second matrix.
    Exceptions:
    TypeError: Occurs if one or both of the input arguments are not lists or nested lists.

    """
    if len(matrix_1[0]) != len(matrix_2):
        return None
    else:
        matrix_mult = [[0]*len(matrix_2[0]) for _ in range(len(matrix_1))]
        for i in range(len(matrix_1)):
            for j in range(len(matrix_2[0])):
                for r in range(len(matrix_2)):
                    matrix_mult[i][j] += int(matrix_1[i][r]) * int(matrix_2[r][j])
        return matrix_mult


def matrix_transposition(matrix):
    """
    The matrix_transposition function transposes a matrix represented as a nested list.
    Transposing a matrix means exchanging rows and columns.
    The function passes through each element of the original matrix matrix using nested for loops.
    For each matrix[i][j] element (row i, column j), the function assigns the value of the matrix_trans[j][i] element
    (row j, column i). Thus, the rows and columns of the original matrix are swapped.
    Parameters:
    matrix (list of lists): The matrix to be transposed.
    Return value:
    list of lists: A transposed matrix represented as a nested list.
    Exceptions:
    TypeError: Occurs if the input argument is not a list or a nested list.

    """

    if not matrix:
        return []
    else:
        matrix_trans = [[0]*len(matrix) for _ in range(len(matrix[0]))]
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                matrix_trans[j][i] = matrix[i][j]
        return matrix_trans

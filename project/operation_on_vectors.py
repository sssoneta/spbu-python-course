# Operation on vectors

from math import pi, acos


def the_scalar_product_of_vectors(vector_1: list[int], vector_2: list[int]):
    """
    Function the_scalar_product_of_vectors checks whether the vectors have the same length. If not, it returns None.
    Otherwise, the function calculates the scalar pro1duct by multiplying the corresponding elements of the vectors
    and summing the results.

    Parameters:
    -----------
    vector_1 (list): The first vector, represented as a list of numbers.
    vector_2 (list): The second vector, represented as a list of numbers.

    Return value:
    -------------
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


def vector_length(vector: list[int]):
    """
    The vector_length function calculates the length of a vector represented as a list of numbers.

    Parameters:
    -----------
    vector (list): A vector represented as a list of numbers.

    Return value:
    -------------
    int: The length of the vector, rounded to an integer

    """
    s = 0
    for i in vector:
        s += i**2
    return round(pow(s, 0.5), 2)


def the_angle_between_the_vectors(vector_1: list[int], vector_2: list[int]):
    """
    The_angle_between_the_vectors function calculates the angle between two vectors
    given as lists of numbers using the scalar product and the lengths of the vectors.

    Parameters:
    -----------
    vector_1 (list): The first vector, represented as a list of numbers.
    vector_2 (list): The second vector, represented as a list of numbers.

    Return value:
    -------------
    float: The angle between the vectors in radians, with an accuracy of two decimal places.

    """
    s = the_scalar_product_of_vectors(vector_1, vector_2)
    angle = s / (vector_length(vector_1) * vector_length(vector_2))
    angle = acos(angle) * 180 / pi
    return round(angle)

from .my_module import *


def test_1_the_scalar_product_of_vectors():
    assert the_scalar_product_of_vectors([2, -5], [-1, 0]) == -2


def test_2_the_scalar_product_of_vectors():
    assert the_scalar_product_of_vectors([1, 1], [2, 1, 4, 9]) is None


def test_3_the_scalar_product_of_vectors():
    assert the_scalar_product_of_vectors([1, 2, -4], [6, -1, 1]) == 0


def test_1_vector_length():
    assert vector_length([3, 4, 0]) == 5


def test_2_vector_length():
    assert vector_length([-5, 8]) == int(pow(89, 0.5))


def test_3_vector_length():
    assert vector_length([-2, 0, 5]) == int(pow(29, 0.5))


def test_1_the_angle_between_the_vectors():
    assert the_angle_between_the_vectors([1, 1, -2], [1, 0, -1]) == 30


def test_2_the_angle_between_the_vectors():
    assert the_angle_between_the_vectors([2, -2, 0], [3, 0, -3]) == 60


def test_1_matrix_addition():
    assert matrix_addition([[1, 2], [3, 4]], [[5, 6], [7, 8]]) == [[6, 8], [10, 12]]


def test_2_matrix_addition():
    assert matrix_addition([[1, 2], [3, 4]], [[5, 6, 7], [8, 9, 10]]) is None


def test_3_matrix_addition():
    assert matrix_addition([[]], [[]]) == [[]]


def test_4_matrix_addition():
    assert matrix_addition([[1]], [[2]]) == [[3]]


def test_5_matrix_addition():
    assert matrix_addition([[-1, -2], [-3, -4]], [[1, 2], [3, 4]]) == [[0, 0], [0, 0]]


def test_1_matrix_multiplication():
    assert matrix_multiplication([[1, 2], [3, 4]],  [[5, 6], [7, 8]]) == [[19, 22], [43, 50]]


def test_2_matrix_multiplication():
    assert matrix_multiplication([[1, 2, 3], [3, 4, 1]], [[5, 6, 7], [8, 9, 10]]) is None


def test_3_matrix_multiplication():
    assert matrix_multiplication([[1]], [[2]]) == [[2]]


def test_4_matrix_multiplication():
    assert matrix_multiplication([[]], [[]]) is None

def test_1_matrix_transposition():
    assert matrix_transposition([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]


def test_2_matrix_transposition():
    assert matrix_transposition([]) == []


def test_3_matrix_transposition():
    assert matrix_transposition([[1]]) == [[1]]


def test_4_matrix_transposition():
    assert matrix_transposition([[1, 2], [3, 4]]) == [[1, 3], [2, 4]]



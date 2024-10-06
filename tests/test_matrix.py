from project.operation_on_matrix import *

import pytest


def test_matrix_addition_valid():
    matrix_1 = [[1, 2], [3, 4]]
    matrix_2 = [[5, 6], [7, 8]]
    expected_result = [[6, 8], [10, 12]]
    assert matrix_addition(matrix_1, matrix_2) == expected_result


def test_matrix_addition_different_dimensions():
    matrix_1 = [[1, 2], [3, 4]]
    matrix_2 = [[5, 6, 7], [8, 9, 10]]
    assert matrix_addition(matrix_1, matrix_2) is None


def test_matrix_addition_empty():
    matrix_1 = [[]]
    matrix_2 = [[]]
    assert matrix_addition(matrix_1, matrix_2) == [[]]


def test_matrix_addition_single_element():
    matrix_1 = [[1]]
    matrix_2 = [[2]]
    expected_result = [[3]]
    assert matrix_addition(matrix_1, matrix_2) == expected_result


def test_matrix_addition_negative_numbers():
    matrix_1 = [[-1, -2], [-3, -4]]
    matrix_2 = [[1, 2], [3, 4]]
    expected_result = [[0, 0], [0, 0]]
    assert matrix_addition(matrix_1, matrix_2) == expected_result


def test_matrix_multiplication_valid():
    matrix_1 = [[1, 2], [3, 4]]
    matrix_2 = [[5, 6], [7, 8]]
    expected_result = [[19, 22], [43, 50]]
    assert matrix_multiplication(matrix_1, matrix_2) == expected_result


def test_matrix_multiplication():
    matrix_1 = [[1, 2, 4], [3, 4, 9]]
    matrix_2 = [[5, 6], [7, 8], [9, 0]]
    expected_result = [[55, 22], [124, 50]]
    assert matrix_multiplication(matrix_1, matrix_2) == expected_result


def test_matrix_multiplication_different_dimensions():
    matrix_1 = [[1, 2], [3, 4]]
    matrix_2 = [[5, 6, 7, 0], [8, 9, 10, 11], [1, 2, 3, 4]]
    assert matrix_multiplication(matrix_1, matrix_2) is None


def test_matrix_multiplication_empty():
    matrix_1 = [[]]
    matrix_2 = [[]]
    assert matrix_multiplication(matrix_1, matrix_2) is None


def test_matrix_multiplication_single_element():
    matrix_1 = [[1]]
    matrix_2 = [[2]]
    expected_result = [[2]]
    assert matrix_multiplication(matrix_1, matrix_2) == expected_result


def test_matrix_multiplication_identity():
    matrix_1 = [[1, 2], [3, 4]]
    matrix_2 = [[1, 0], [0, 1]]
    assert matrix_multiplication(matrix_1, matrix_2) == matrix_1


def test_matrix_multiplication_negative_numbers():
    matrix_1 = [[-1, -2], [-3, -4]]
    matrix_2 = [[1, 2], [3, 4]]
    expected_result = [[-7, -10], [-15, -22]]
    assert matrix_multiplication(matrix_1, matrix_2) == expected_result


def test_matrix_transposition_valid():
    matrix = [[1, 2, 3], [4, 5, 6]]
    expected_result = [[1, 4], [2, 5], [3, 6]]
    assert matrix_transposition(matrix) == expected_result


def test_matrix_transposition_empty():
    matrix = []
    assert matrix_transposition(matrix) == []


def test_matrix_transposition_single_element():
    matrix = [[1]]
    assert matrix_transposition(matrix) == [[1]]


def test_matrix_transposition_square():
    matrix = [[1, 2], [3, 4]]
    expected_result = [[1, 3], [2, 4]]
    assert matrix_transposition(matrix) == expected_result


def test_matrix_transposition_invalid_input_type():
    with pytest.raises(TypeError):
        matrix_transposition(1)  # Не список


def test_matrix_transposition_invalid_input_type_2():
    with pytest.raises(TypeError):
        matrix_transposition([[1, 2], 3])  # Не список списков

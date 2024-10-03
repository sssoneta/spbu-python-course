from project.operation_on_vectors_and_matrix import *

import pytest


def test_scalar_product_valid():
    vector_1 = [1, 2, 3]
    vector_2 = [4, 5, 6]
    assert the_scalar_product_of_vectors(vector_1, vector_2) == 32


def test_scalar_product_different_lengths():
    vector_1 = [1, 2, 3]
    vector_2 = [4, 5]
    assert the_scalar_product_of_vectors(vector_1, vector_2) is None


def test_vector_length_valid():
    vector = [3, 4]
    assert vector_length(vector) == 5.0


def test_vector_length_empty():
    vector = []
    assert vector_length(vector) == 0.0


def test_vector_length_negative():
    vector = [-3, -4]
    assert vector_length(vector) == 5.0


def test_vector_length_zero():
    vector = [0, 0, 0]
    assert vector_length(vector) == 0.0


def test_angle_between_vectors_valid():
    vector_1 = [1, 2]
    vector_2 = [3, 4]
    assert the_angle_between_the_vectors(vector_1, vector_2) == 11


def test_angle_between_vectors_orthogonal():
    vector_1 = [1, 0]
    vector_2 = [0, 1]
    assert the_angle_between_the_vectors(vector_1, vector_2) == 90


def test_angle_between_vectors_different_lengths():
    vector_1 = [1, 2, 3]
    vector_2 = [4, 5]
    with pytest.raises(TypeError):
        the_angle_between_the_vectors(vector_1, vector_2)

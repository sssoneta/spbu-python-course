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










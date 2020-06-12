import numpy as np


def calculate_correlation(first_array, second_array):
    return np.corrcoef(first_array, second_array)[0, 1]
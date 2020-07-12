import numpy as np

from app.api.utils.Text import NAN_ELEMENT


def calculate_correlation(first_array, second_array):
    first_array_wo_nan, second_array_wo_nan = [], []

    # filter our pair where at least one element is 'N/A'
    for (el1, el2) in zip(first_array, second_array):
        if el1 is NAN_ELEMENT or el2 is NAN_ELEMENT:
            continue
        first_array_wo_nan.append(el1)
        second_array_wo_nan.append(el2)

    return round(np.corrcoef(first_array_wo_nan, second_array_wo_nan)[0, 1], 4)


def calculate_ngrams_correlation(first_keywords, second_keywords):
    first_array, second_array = [], []
    for key in first_keywords.keys() | second_keywords.keys():
        first_array.append(first_keywords.get(key, 0))
        second_array.append(second_keywords.get(key, 0))

    return round(np.corrcoef(first_array, second_array)[0, 1], 4)
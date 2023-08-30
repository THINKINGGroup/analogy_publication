import pytest

from src.analogy.data import load_sample_data


def test_sample_dataset():
    dataset = load_sample_data()

    assert dataset.shape[0] == 2438

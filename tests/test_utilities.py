import os

import pytest

from src.analogy.utils.file_utils import check_file_extension, check_is_directory, check_is_file


@pytest.mark.parametrize(
    ("resource_path", "file_expected", "directory_expected"),
    [
        ("src/analogy/data/sample.csv", True, False),
        ("src/analogy/data", False, True),
        ("src/analogy/data/data.txt", False, False),
        ("src/analogy/data/csv", False, False),
        (None, False, False),
    ],
)
def test_file_utilities(resource_path, file_expected, directory_expected):
    status_ext = check_file_extension(resource_path)
    status_file = check_is_file(resource_path)
    status_dir = check_is_directory(resource_path)

    assert status_ext == file_expected
    assert status_file == file_expected
    assert status_dir == directory_expected

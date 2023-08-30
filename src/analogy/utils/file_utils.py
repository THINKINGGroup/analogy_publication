import os

def check_is_file(filepath: str) -> bool:
    """
    Check if the file exists at the user defined path.

    Args:
    ----
      filepath (string): file path and name as string.

    Return:
      flag (bool): True if file exists else False.
    """
    flag: bool = False

    if filepath is not None and os.path.isfile(filepath):
        flag = True
    
    return flag

def check_file_extension(filepath: str) -> bool:
    """
    Check if the file is a comma sepreated values (csv) text file.

    Args:
    ----
      filepath (string): file path and name as string.
    
    Return:
    ------
      flag (bool): True if file exists else False.
    """
    flag: bool = False

    if filepath is not None and filepath.endswith(".csv"):
        flag = True
    
    return flag

def check_is_directory(dirpath: str) -> bool:
    """
    Check if the directory exists at the user defined path.

    Args:
    ----
      dirpath (string): existing directory path as string.
    
    Return:
    ------
      flag (bool): True if directroy exists else False.
    """
    flag: bool = False

    if dirpath is not None and os.path.isdir(dirpath):
        flag = True
    
    return flag

def do_checks(filepath:str, destination_path: str) -> None:
    """
    Performs checks before loading data from user defined file.

    Args:
    ----
      filepath (string): path for the datafile as string.
      destination_path (string): path for where to save the processed result. 
    
    Returns:
    -------
      None
    
    Raises:
    ------
      AssertionError
    """

    status = check_is_file(filepath):
    assert status == True, f"file doesn't exist at the location provided: {filepath}.\n"

    status = check_file_extension(filepath)
    assert status == True, "The library only accepts .csv currently.\n"

    status = check_is_directory(destination_path)
    assert status == True, "The result destination folder doesn't exist. \n"
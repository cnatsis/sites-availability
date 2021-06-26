from os import path


def read_file(file_name):
    """
    Reads a file to list
    :param file_name: Input file name
    :return: line content in list
    """
    if path.exists(file_name):
        with open(file_name, 'r') as f:
            content = f.read().splitlines()
        return content
    else:
        print("File '{}' does not exist.".format(file_name))
        return []

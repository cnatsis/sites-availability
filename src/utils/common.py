from os import path


def read_file_to_list(file_name):
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


def read_file_to_tuple(file_name):
    """
    Reads files in tuples of string
    :param file_name: Input file name
    :return: line content in tuple list
    """
    tuples = []
    with open(file_name) as f:
        for line in f:
            tuples.append(tuple(line.rstrip().split()))
        f.close()
    return tuples

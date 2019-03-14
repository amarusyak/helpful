def dict_passage_permutations(data):
    """
    Function that finds all possible passages through a given dictionary.
    :param data: dictionary, to operate on.
    :return: List of lists that corresponds to every passage of a given dictionary.
    """
    result = list()
    for key, value in data.items():
        if isinstance(value, list):
            result.extend(map(lambda v: [key, v], value))
        elif isinstance(value, dict):
            result.extend(list(map(lambda v: [key] + v, dict_passage_permutations(value))))
        elif isinstance(value, str):
            result.append([key, value])
        else:
            err_msg = "Acceptable types are: 'str', 'list', 'dict'; '{t}' given - {v}"
            raise TypeError(err_msg.format(t=type(value), v=value))
    return result


def compare_list_of_dicts(first, second):
    """
    Simple comparator of two lists of dictionaries.
    :param first: a first list of dictionaries
    :param second: a second list of dictionaries
    :return: True, if lists are equal; otherwise - False
    """
    assert len(first) == len(second)
    return all([f_item in second for f_item in first])

def dict_passage_permutations(data: dict) -> list:
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


def compare_lists_of_dicts(first: list, second: list) -> bool:
    """
    Simple comparator of two lists of dictionaries.
    :param first: a first list of dictionaries
    :param second: a second list of dictionaries
    :return: True, if lists are equal; otherwise - False
    """
    len_err_msg = ("len(first) != len(second)\n"
                   "{f} != {s}".format(f=len(first), s=len(second)))
    assert (len(first) == len(second)), len_err_msg
    return all([f_item in second for f_item in first])


def diffdict(first: dict, second: dict, symmetric_match: bool = True, strict_match: bool = True, path='') -> list:
    """
    Detects a difference between two given dictionaries.
    :param first: first dictionary to compare
    :param second: second dictionary to compare
    :param symmetric_match: If False - ignores dict keys in the second dict that is not present in the first dict
    :param strict_match: If False - tuples and dicts are compared only by values, order is ignored
    :param path: INTERNAL - uses for recursion; the path to exact key
    :return: a list of "diff" messages
    """
    diff = list()

    # Values are dicts
    if isinstance(first, dict) and isinstance(second, dict):
        for key in set(first.keys()).difference(set(second.keys())):
            message = f"{path} -> Key '{key}' not found in the 2nd dict."
            diff.append(message)

        if symmetric_match:
            for key in set(second.keys()).difference(set(first.keys())):
                message = f"{path} -> Key '{key}' not found in the 1st dict."
                diff.append(message)

        for key in set(first.keys()).intersection(set(second.keys())):
            new_path = key if not path else f"{path}.{key}"
            diff.extend(diffdict(first=first[key], second=second[key],
                                 symmetric_match=symmetric_match, strict_match=strict_match, path=new_path))

    # Values are iterables
    elif isinstance(first, (list, tuple)) and isinstance(second, (list, tuple)):
        if not strict_match:
            is_simple = True
            for el in first:
                is_simple &= isinstance(el, (str, float, int))
            for el in second:
                is_simple &= isinstance(el, (str, float, int))
        else:
            is_simple = False

        if is_simple:
            first_set = set(first)
            second_set = set(second)
            first_only = first_set - second_set
            second_only = second_set - first_set

            if first_only:
                message = "[{els}] element(s) is(are) in 1st dict but not in 2nd dict.".format(
                    els=', '.join(str(el) for el in first_only))
                if path:
                    message = f"{path} -> {message}"
                diff.append(message)
            if second_only:
                message = "[{els}] element(s) is(are) in 2nd dict but not in 1st dict.".format(
                    els=', '.join(str(el) for el in second_only))
                if path:
                    message = f"{path} -> {message}"
                diff.append(message)
        else:
            for (index, element) in enumerate(first):
                new_path = f"{path}[{index}]"

                # Try to get the element by the index from the second dict.
                try:
                    second_element = second[index]
                except IndexError:
                    message = f"{new_path} -> Element '{first[index]}' not found in the 2nd dict."
                    diff.append(message)
                    continue

                diff.extend(diffdict(first=element, second=second_element,
                                     symmetric_match=symmetric_match, strict_match=strict_match, path=new_path))

            # Add extra elements in the second list into diff list.
            if len(second) > len(first):
                for index in range(len(first), len(second)):
                    new_path = f"{path}[{index}]"

                    message = f"{new_path} -> Element '{second[index]}' not found in the 1st dict."
                    diff.append(message)

    # String
    elif isinstance(first, str) and isinstance(second, str):
        if str(first) != str(second):
            message = f"{path} -> '{first}' != '{second}'"
            diff.append(message)

    # Float
    elif isinstance(first, float) and isinstance(second, float):
        if first != second and abs(first - second) > 0.00001:
            message = f"{path} -> {first:.2f} != {second:.2f}"
            diff.append(message)

    # Int
    elif isinstance(first, int) and isinstance(second, int):
        if first != second:
            message = f"{path} -> {first} != {second}"
            diff.append(message)

    # Other types
    elif isinstance(first, type(second)):
        if first != second:
            message = f"{path} -> {first} != {second}"
            diff.append(message)

    # Different types:
    else:
        message = 'Values have different type: {tf}, {ts}.'.format(tf=type(first), ts=type(second))
        if path:
            message = f"{path} -> {message}"
        diff.append(message)

    return diff

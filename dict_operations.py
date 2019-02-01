def nested_dict_passage_permutations(d, perm=None, parent_key=None):
    """
    Function that finds all possible passages through a given dict.
    Max dictionary depth: 3.
    :param d: REQUIRED - dictionary, to operate on.
    :param perm: OPTIONAL - already formed list of possible passages.
    :param parent_key: OPTIONAL - first item of some amount of new.
        passages that will be added to the result.
    :return: List of lists that corresponds to every passage of a 
        given dictionary.
    """
    permutations = perm if perm else list()
    for key, value in d.items():
        if isinstance(value, str):
            permutations.append([key, value])
        if isinstance(value, list):
            for item in value:
                p = [parent_key, key, item] if parent_key else [key, item]
                permutations.append(p)
        if isinstance(value, dict):
            nested_dict_passage_permutations(d=value,
                                             perm=permutations,
                                             parent_key=key)
    return permutations

__author__ = 'AChen'

def nested_max(obj):
    """Return the maximum item stored in <obj>.

    You may assume all the items are positive, and calling
    nested_max on an empty list returns 0.

    @type obj: int | list
    @rtype: int

    >>> nested_max(17)
    17
    >>> nested_max([1, 2, [1, 2, [3], 4, 5], 4])
    5
    """
    if isinstance(obj, int):
        return obj
    else:
        max = 0
        for lst_i in obj:
            if nested_max(lst_i) > max:
                max = nested_max(lst_i)
        return max

def length(obj):
    """Return the length of <obj>.

    The *length* of a nested list is defined as:
    1. 0, if <obj> is a number.
    2. The maximum of len(obj) and the lengths of the nested lists contained
       in <obj>, if <obj> is a list.

    @type obj: int | list
    @rtype: int

    >>> length(17)
    0
    >>> length([1, 2, [1, 2], 4])
    4
    >>> length([1, 2, [1, 2, [3], 4, 5], 4])
    5
    """
    if isinstance(obj, int):
        return 0
    else:
        max_length = len(obj)
        for i in obj:
            max_length = max(max_length, length(i))
        return max_length

def equal(obj1, obj2):
    """Return whether two nested lists are equal, i.e., have the same value.

    Note: order matters.

    @type obj1: int | list
    @type obj2: int | list
    @rtype: bool
    >>> equal(3, 3)
    True
    >>> equal([4], [4])
    True
    >>> equal(17, [1, 2, 3])
    False
    >>> equal([1, 2, [1, 2], 4], [1, 2, [1, 2], 4])
    True
    >>> equal([1, 2, [1, 2], 4], [4, 2, [2, 1], 3])
    False
    """
    if isinstance(obj1, int) and isinstance(obj2, int):
        if obj1 != obj2:
            return False
        else:
            return True
    elif isinstance(obj1, int) and not isinstance(obj2, int):
        return False
    elif not isinstance(obj1, int) and isinstance(obj2, int):
        return False
    else:
        for i in range(len(obj1)):
            return equal(obj1[i], obj2[i])



if __name__ == '__main__':
    import doctest
    doctest.testmod()

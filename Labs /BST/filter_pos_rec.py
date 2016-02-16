__author__ = 'AChen'

from rec_linked_list import *

def filter_pos_rec(lst):
    """
    @type lst: LinkedListRec
    >>> lst = LinkedListRec([3, -10, 4, 0])
    >>> pos = filter_pos_rec(lst)
    >>> str(pos)
    '3 -> 4'

    """
    if lst.is_empty():
        return lst
    else:
        pos_rec = LinkedListRec([])
        if lst._first > 0:
            pos_rec._first = lst._first
            pos_rec._rest = filter_pos_rec(lst._rest)
        else:
            pos_rec = filter_pos_rec(lst._rest)
        return pos_rec

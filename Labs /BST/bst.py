__author__ = 'AChen'

class BinarySearchTree:
    """Binary Search Tree class.

    This class represents a binary tree satisfying the Binary Search Tree
    property: for every node, its value is >= all items stored in its left
    subtree, and < all items stored in its right subtree.
    """

    # === Private Attributes ===
    # @type _root: object
    #     The item stored at the root of the tree, or None if the tree is empty.
    # @type _left: BinarySearchTree | None
    #     The left subtree, or None if the tree is empty
    # @type _right: BinarySearchTree | None
    #     The right subtree, or None if the tree is empty

    # === Representation Invariants ===
    #  - If _root is None, then so are _left and _right. This represents an empty BST.
    #  - If _root is not None, then _left and _right are BSTs.
    #  - All items in _left are <= _root, and all items in _right are >= _root.

    def __init__(self, root):
        """Initialize a new BST with the given root value.

        If <root> is None, the tree is empty, and the subtrees are None.
        If <root> is not None, the subtrees are empty.

        @type self: BinarySearchTree
        @type root: object
            A value for the root of the BST. If None, the BST is empty.
        @rtype: None
        """
        if root is None:
            self._root = None
            self._left = None
            self._right = None
        else:
            self._root = root
            self._left = BinarySearchTree(None)
            self._right = BinarySearchTree(None)

    def is_empty(self):
        """Return True if self is empty.

        @type self: BinarySearchTree
        @rtype: bool

        >>> bst = BinarySearchTree(None)
        >>> bst.is_empty()
        True
        >>> bst = BinarySearchTree(10)
        >>> bst.is_empty()
        False
        """
        return self._root is None

    def print(self, depth=0):
        """Print all of the items in this BST,
        where the root is printed before all of its subtrees,
        and every value is indented to show its depth.

        @type self: BinarySearchTree
        @rtype: None
        """
        if not self.is_empty():
            print(depth * '  ' + str(self._root))
            self._left.print(depth + 1)
            self._right.print(depth + 1)

    def __contains__(self, item):
        """Return True if item is in this BST.

        @type self: BinarySearchTree
        @type item: object
        @rtype: bool

        >>> bst = BinarySearchTree(3)
        >>> bst._left = BinarySearchTree(2)
        >>> bst._right = BinarySearchTree(5)
        >>> 3 in bst
        True
        >>> 5 in bst
        True
        >>> 2 in bst
        True
        >>> 4 in bst
        False
        """
        if self.is_empty():
            return False
        elif item == self._root:
            return True
        elif item < self._root:
            return item in self._left # or, self._left.__contains__(item)
        else:
            return item in self._right # # or, self._right.__contains__(item)

    # ------------------------------------------------------------------------
    # Lab 7 Exercises
    # ------------------------------------------------------------------------
    def height(self):
        """Return the height of this BST.

        @type self: BinarySearchTree
        @rtype: int

        >>> BinarySearchTree(None).height()
        0
        >>> bst = BinarySearchTree(7)
        >>> bst.height()
        1
        >>> bst._left = BinarySearchTree(5)
        >>> bst.height()
        2
        >>> bst._right = BinarySearchTree(9)
        >>> bst.height()
        2
        """
        # TODO
        if self.is_empty():
            return 0
        else:
            return 1 + max(self._left.height(), self._right.height())

    def items(self):
        """Return all of the items in the BST in sorted order.

        @type self: BinarySearchTree
        @rtype: list

        >>> BinarySearchTree(None).items()
        []
        >>> bst = BinarySearchTree(7)
        >>> left = BinarySearchTree(3)
        >>> left._left = BinarySearchTree(2)
        >>> left._right = BinarySearchTree(5)
        >>> right = BinarySearchTree(11)
        >>> right._left = BinarySearchTree(9)
        >>> right._right = BinarySearchTree(13)
        >>> bst._left = left
        >>> bst._right = right
        >>> bst.items()
        [2, 3, 5, 7, 9, 11, 13]
        >>> t = BinarySearchTree(3)
        >>> l = BinarySearchTree(2)
        >>> r = BinarySearchTree(4)
        >>> t._left = l
        >>> t._right = r
        >>> t.items()
        [2, 3, 4]
        """
        # TODO
        if self.is_empty():
            return []
        elif self._left.is_empty():
            return [self._root]
        else:
            lst = []
            lst.extend(self._left.items())
            lst.extend([self._root])
            lst.extend(self._right.items())
            return lst

    def smaller(self, item):
        """Return all of the items in the BST strictly smaller than <item>
        in sorted order.

        @type item: object
        @rtype: list

        >>> bst = BinarySearchTree(7)
        >>> left = BinarySearchTree(3)
        >>> left._left = BinarySearchTree(2)
        >>> left._right = BinarySearchTree(5)
        >>> right = BinarySearchTree(11)
        >>> right._left = BinarySearchTree(9)
        >>> right._right = BinarySearchTree(13)
        >>> bst._left = left
        >>> bst._right = right
        >>> bst.items()
        [2, 3, 5, 7, 9, 11, 13]
        >>> bst.smaller(6)
        [2, 3, 5]
        >>> bst.smaller(13)
        [2, 3, 5, 7, 9, 11]
        """
        # TODO
        lst = self.items()
        to_r = []
        for i in lst:
            if i < item:
                to_r.append(i)
        return to_r

    # Mutating methods

    def insert(self, item):
        """Insert <item> into this BST, maintaining the BST property.

        Do not change positions of any other items.

        @type self: BinarySearchTree
        @type item: object
        @rtype: None

        >>> bst = BinarySearchTree(10)
        >>> bst.insert(3)
        >>> bst.insert(20)
        >>> bst._root
        10
        >>> bst._left._root
        3
        >>> bst._right._root
        20
        """
        # TODO
        if self.is_empty():
            self._root = item
        elif item > self._root:
            self._right.insert(item)
        elif item < self._root:
            self._left.insert(item)
        else:
            pass

    def rotate_right(self):
        """Rotate the BST clockwise, i.e. make the left subtree the root.

        @type self: BinarySearchTree
        @rtype: object

        >>> bst = BinarySearchTree(7)
        >>> left = BinarySearchTree(3)
        >>> right = BinarySearchTree(11)
        >>> left._left = BinarySearchTree(2)
        >>> left._right = BinarySearchTree(5)
        >>> bst._left = left
        >>> bst._right = right
        >>> bst.print()
        7
          3
            2
            5
          11
        >>> bst.rotate_right()
        >>> bst.print()
        3
          2
          7
            5
            11
        >>> bst.rotate_right()
        >>> bst.print()
        2
          3
            7
              5
              11
        """
        # TODO
        new_root = self._left._root
        old_root = BinarySearchTree(self._root)
        old_right_tree = self._right
        old_left_left_tree = self._left._left
        old_left_right_tree = self._left._right
        self._root = new_root
        self._left = old_left_left_tree
        old_root._left = old_left_right_tree
        old_root._right = old_right_tree
        self._right = old_root


    def rotate_left(self):
        """Rotate the BST counter-clockwise, i.e. make the right subtree the root.

        @type self: BinarySearchTree
        @rtype: object

        >>> bst = BinarySearchTree(7)
        >>> left = BinarySearchTree(3)
        >>> left._left = BinarySearchTree(2)
        >>> left._right = BinarySearchTree(5)
        >>> right = BinarySearchTree(11)
        >>> right._left = BinarySearchTree(9)
        >>> right._right = BinarySearchTree(13)
        >>> bst._left = left
        >>> bst._right = right
        >>> bst.print()
        7
          3
            2
            5
          11
            9
            13
        >>> bst.rotate_left()
        >>> bst.print()
        11
          7
            3
              2
              5
            9
          13
        >>> bst.rotate_left()
        >>> bst.print()
        13
          11
            7
              3
                2
                5
              9
        """
        # TODO
        new_root = self._right._root
        old_root = BinarySearchTree(self._root)
        old_l = self._left
        old_r_l = self._right._left
        old_r_r = self._right._right
        old_root._left = old_l
        old_root._right = old_r_l
        self._root = new_root
        self._left = old_root
        self._right = old_r_r

    # ------------------------------------------------------------------------
    # Implementation of deletion - we'll cover this on Friday
    # ------------------------------------------------------------------------
    def delete(self, item):
        """Remove *one* occurrence of item from this tree.

        Do nothing if <item> is not in the tree.

        @type self: BinarySearchTree
        @type item: object
        @rtype: None

        >>> bst = BinarySearchTree(7)
        >>> left = BinarySearchTree(3)
        >>> left._left = BinarySearchTree(2)
        >>> left._right = BinarySearchTree(5)
        >>> right = BinarySearchTree(11)
        >>> right._left = BinarySearchTree(9)
        >>> right._right = BinarySearchTree(13)
        >>> bst._left = left
        >>> bst._right = right
        >>> bst.items()
        [2, 3, 5, 7, 9, 11, 13]
        >>> bst.delete(13)
        >>> bst.items()
        [2, 3, 5, 7, 9, 11]
        >>> bst.delete(9)
        >>> bst.items()
        [2, 3, 5, 7, 11]
        >>> bst.delete(2)
        >>> bst.items()
        [3, 5, 7, 11]
        >>> bst.delete(5)
        >>> bst.items()
        [3, 7, 11]
        >>> bst.delete(7)
        >>> bst.items()
        [3, 11]
        """
        if not self.is_empty():
            if self._root == item:
                self.delete_root()
            elif item < self._root:
                self._left.delete(item)
            else:
                self._right.delete(item)

    def delete_root(self):
        """Remove the root of this tree.

        Precondition: this tree is *non-empty*.

        @type self: BinarySearchTree
        @rtype: None
        """
        if self._left.is_empty() and self._right.is_empty():
            self._root = None
            self._left = None
            self._right = None
        elif self._left.is_empty():
            self._root = self._right.extract_min()
        else:
            self._root = self._left.extract_max()

    def extract_max(self):
        """Remove and return the maximum item stored in this tree.

        Precondition: this tree is *non-empty*.

        @type self: BinarySearchTree
        @rtype: object
        """
        if self._right.is_empty():
            temp = self._root
            # Copy left subtree to self, because root node is removed.
            # Note that self = self._left does NOT work!
            self._root = self._left._root
            self._right = self._left._right
            self._left = self._left._left
            return temp
        else:
            return self._right.extract_max()

    def extract_min(self):
        """Remove and return the minimum item stored in this tree.

        Precondition: this tree is *non-empty*.

        @type self: BinarySearchTree
        @rtype: object
        """
        if self._left.is_empty():
            temp = self._root
            self._root = self._right._root
            self._left = self._right._left
            self._right = self._right._right
            return temp
        else:
            return self._left.extract_min()

if __name__ == "__main__":
    import doctest
    doctest.testmod()

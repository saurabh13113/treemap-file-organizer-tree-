"""
Assignment 2: Trees for Treemap

=== Module Description ===
This module contains the basic tree interface required by the treemap
visualiser. You will both add to the abstract class, and complete a
concrete implementation of a subclass to represent files and folders on your
computer's file system.
"""
from __future__ import annotations

import math
import os
from random import randint
from typing import List, Tuple, Optional


def get_colour() -> Tuple[int, int, int]:
    """This function picks a random colour selectively such that it is not on
    the grey scale. The colour is close to the grey scale if the r g b values
    have a small variance. This function checks if all the numbers are close
    to the mean, if so, it shifts the last digit by 150.

    This way you can't confuse the leaf rectangles with folder rectangles,
    because the leaves will always be a colour, never close to black / white.
    """
    rgb = [randint(0, 255), randint(0, 255), randint(0, 255)]
    avg = sum(rgb) // 3
    count = 0
    for item in rgb:
        if abs(item - avg) < 20:
            count += 1
    if count == 3:
        rgb[2] = (rgb[2] + 150) % 255
    return tuple(rgb)


class TMTree:
    """A TreeMappableTree: a tree that is compatible with the treemap
    visualiser.

    This is an abstract class that should not be instantiated directly.

    You may NOT add any attributes, public or private, to this class.
    However, part of this assignment will involve you implementing new public
    *methods* for this interface.
    You should not add any new public methods other than those required by
    the client code.
    You can, however, freely add private methods as needed.

    === Public Attributes ===
    rect: The pygame rectangle representing this node in the visualization.
    data_size: The size of the data represented by this tree.

    === Private Attributes ===
    _colour: The RGB colour value of the root of this tree.
    _name: The root value of this tree, or None if this tree is empty.
    _subtrees: The subtrees of this tree.
    _parent_tree: The parent tree of this tree; i.e., the tree that contains
    this tree as a subtree, or None if this tree is not part of a larger tree.
    _expanded: Whether this tree is considered expanded for visualization.
    _depth: The depth of this tree node in relation to the root.

    === Representation Invariants ===
    - data_size >= 0
    - If _subtrees is not empty, then data_size is equal to the sum of the
      data_size of each subtree.
    - _colour's elements are each in the range 0-255.
    - If _name is None, then _subtrees is empty, _parent_tree is None, and
      data_size is 0.
      This setting of attributes represents an empty tree.
    - if _parent_tree is not None, then self is in _parent_tree._subtrees
    - if _expanded is True, then _parent_tree._expanded is True
    - if _expanded is False, then _expanded is False for every tree
      in _subtrees
    - if _subtrees is empty, then _expanded is False
    """

    rect: Tuple[int, int, int, int]
    data_size: int
    _colour: Tuple[int, int, int]
    _name: str
    _subtrees: List[TMTree]
    _parent_tree: Optional[TMTree]
    _expanded: bool
    _depth: int

    def __init__(self, name: str, subtrees: List[TMTree],
                 data_size: int = 0) -> None:
        """Initializes a new TMTree with a random colour, the provided name
        and sets the subtrees to the list of provided subtrees. Sets this tree
        as the parent for each of its subtrees.

        Precondition: if <name> is None, then <subtrees> is empty.
        """
        self.rect = (0, 0, 0, 0)
        self._parent_tree = None
        self._depth = 0
        self._expanded = False

        # 1. Initialize: - self._name
        #                - self._colour (use the get_colour() function)
        #                - self._subtrees
        #                - self.data_size
        # 2. Set this tree as the parent for each of its subtrees.
        #
        # NOTES: - self._expanded will be changed in task 5
        #        - Leaf nodes will have data_size set to the size of the file
        #        - Internal nodes will have the data_size = 0
        #           -> this needs to be updated based on the sizes of subtrees
        #
        self._name = name
        self._colour = get_colour()
        self._subtrees = subtrees
        if not self._subtrees:
            self.data_size = data_size
        else:
            self.data_size = 0
            for tr in self._subtrees:
                tr._parent_tree = self
                self.data_size += tr.data_size

    def is_empty(self) -> bool:
        """Returns True iff this tree is empty.
        """
        return self._name is None

    def get_parent(self) -> Optional[TMTree]:
        """Returns the parent of this tree.
        """
        return self._parent_tree

    # **************************************************************************
    # ************* TASK 2: UPDATE AND GET RECTANGLES **************************
    # **************************************************************************

    def update_rectangles(self, rect: Tuple[int, int, int, int]) -> None:
        """Updates the rectangles in this tree and its descendants using the
        treemap algorithm to fill the area defined by the <rect> parameter.
        """
        # Read the Treemap Algorithm description in the handout thoroughly and
        # implement this algorithm to set the <rect> parameter for each
        # tree node.
        #
        # NOTES: - Empty folders should not take up any space
        #        - Both files AND folders need to be assigned a rect attribute
        #        - Don't forget that the last subtree occupies remaining space
        #        - tip: use "tuple unpacking assignment" for easy extraction:
        #           -> x, y, width, height = rect
        #
        if self.data_size == 0:
            self.rect = (0, 0, 0, 0)
        elif not self._subtrees:
            self.rect = rect
        else:
            self.rect = rect
            self.update_rectangles_helper(rect)

    def update_rectangles_helper(self, rect: Tuple[int, int, int, int]) -> None:
        """ Helper method for update_rectangles """
        x, y = rect[0], rect[1]
        tot_w = 0
        tot_h = 0
        for sub in self._subtrees:
            if rect[2] > rect[3]:
                wi = math.floor((sub.data_size / self.data_size) * rect[2])
                if sub == self._subtrees[-1]:
                    wi = self.rect[2] - tot_w
                tot_w += wi
                sub.update_rectangles((x, y, wi, rect[3]))
                x += wi
            elif rect[2] <= rect[3]:
                le = math.floor((sub.data_size / self.data_size) * rect[3])
                if sub == self._subtrees[-1]:
                    le = self.rect[3] - tot_h
                tot_h += le
                sub.update_rectangles((x, y, rect[2], le))
                y += le

    def get_rectangles(self) -> List[Tuple[Tuple[int, int, int, int],
                                           Tuple[int, int, int]]]:
        """Returns a list with tuples for every leaf in the displayed-tree
        rooted at this tree. Each tuple consists of a tuple that defines the
        appropriate pygame rectangle to display for a leaf, and the colour
        to fill it with.
        """
        lst = []
        if self._subtrees == [] or not self._expanded:
            lst.append((self.rect, self._colour))
        else:
            for tr in self._subtrees:
                lst.extend(tr.get_rectangles())
        return lst

        # NOTES: - This method will be modified in Task 6 to return both leaf
        #          nodes and internal nodes which are not expanded
        #

    # **************************************************************************
    # **************** TASK 3: GET_TREE_AT_POSITION ****************************
    # **************************************************************************

    def get_tree_at_position(self, pos: Tuple[int, int]) -> Optional[TMTree]:
        """Returns the leaf in the displayed-tree rooted at this tree whose
        rectangle contains position <pos>, or None if <pos> is outside of this
        tree's rectangle.

        If <pos> is on the shared edge between two or more rectangles,
        always return the leftmost and topmost rectangle (wherever applicable).
        """
        # NOTES: - This method will be modified in Task 6 to return either a
        #          leaf node or an internal node which is not expanded
        #
        if not self._subtrees:
            lower = (self.rect[0], self.rect[1])
            upper = (self.rect[0] + self.rect[2],
                     self.rect[1] + self.rect[3])
            if lower[0] <= pos[0] <= upper[0] and lower[1] <= pos[1] <= \
                    upper[1]:
                return self
            else:
                return None
        else:
            lower = (self.rect[0], self.rect[1])
            upper = (self.rect[0] + self.rect[2],
                     self.rect[1] + self.rect[3])
            if lower[0] <= pos[0] <= upper[0] and lower[1] <= pos[1] <= \
                    upper[1]:
                return self.get_tree_at_position_helper(pos)
        return None

    def get_tree_at_position_helper(self, pos: Tuple[int, int]) -> \
            Optional[TMTree]:
        """Helper function for get_tree_at_position.
        """
        if self._expanded:
            for sub in self._subtrees:
                if sub.get_tree_at_position(pos) is not None:
                    return sub.get_tree_at_position(pos)
        else:
            return self
        return None
    # **************************************************************************
    # ********* TASK 4: MOVE, CHANGE SIZE, DELETE, UPDATE SIZES ****************
    # **************************************************************************

    def update_data_sizes(self) -> int:
        """Updates the data_size attribute for this tree and all its subtrees,
        based on the size of their leaves, and return the new size of the given
        tree node after updating.

        If this tree is a leaf, return its size unchanged.
        """
        # NOTES: - This method is called after some change is made to the tree
        #          so that the change of is reflected in all ancestor
        #          nodes which are affected. (i.e., one leaf node size being
        #          modified results in size changes for its ancestral nodes)
        #
        if not self._subtrees:
            return self.data_size
        else:
            self.data_size = 0
            for tr in self._subtrees:
                tr.update_data_sizes()
                self.data_size += tr.data_size
        return self.data_size

    def change_size(self, factor: float) -> None:
        """Changes the value of this tree's data_size attribute by <factor>.
        Always rounds up the amount to change, so that it's an int, and
        some change is made. If the tree is not a leaf, this method does
        nothing.
        """
        # NOTES: - factor is a percentage in the form of a decimal.
        #          (i.e., factor = 0.01 should increase size by 1%)
        #        - factor may be negative
        #        - the lower limit on data_size is 1 (i.e., you can't let the
        #          size decrease below 1)
        #
        if not self._subtrees:
            change = math.ceil(abs(factor) * self.data_size)
            if factor < 0:
                self.data_size -= change
            else:
                self.data_size += change
            if self.data_size < 1:
                self.data_size = 1

    def delete_self(self, val: bool = False) -> bool:
        """Removes the current node from the visualization and
        returns whether the deletion was successful. Only do this if this node
        has a parent tree.

        Do not set self._parent_tree to None, because it might be used
        by the visualizer to go back to the parent folder.
        """
        # NOTES: - if this tree node is an "only child", you need to
        #          recursively keep deleting the empty folder above
        #        - the root node should not be deleted, and the size won't be
        #          updated if the root node is attempted to be deleted
        #
        if self._parent_tree is not None:
            self._parent_tree._subtrees.remove(self)
            if len(self._parent_tree._subtrees) == 0:
                self._parent_tree.delete_self(True)
            val = True
        return val

    # **************************************************************************
    # ************* TASK 5: UPDATE_COLOURS_AND_DEPTHS **************************
    # **************************************************************************

    def update_depths(self, depth: int = 0) -> None:
        """Updates the depths of the nodes, starting with a depth of 0 at this
        tree node.
        """
        self._depth = depth  # Update the depth attribute of the current node.
        for child in self._subtrees:
            child.update_depths(depth + 1)

    def max_depth(self) -> int:
        """Returns the maximum depth of the tree, which is the maximum length
        between a leaf node and the root node.
        """
        if not self._subtrees:
            return 0
        max_depth = 0
        stack = [(self, 0)]
        while stack:
            node, depth = stack.pop()
            max_depth = max(max_depth, depth)
            for child in node._subtrees:
                stack.append((child, depth + 1))
        return max_depth

    def update_colours(self, step_size: int) -> None:
        """Updates the colours so that the internal tree nodes are
        shades of grey depending on their depth. The root node will be black
        (0, 0, 0) and all internal nodes will be shades of grey depending on
        their depth, where the step size determines the shade of grey.
        Leaf nodes should not be updated.
        """
        if self._subtrees:
            col = self._depth * step_size
            self._colour = (col, col, col)
            for sub in self._subtrees:
                sub.update_colours(step_size)

    def update_colours_and_depths(self) -> None:
        """This method is called any time the tree is manipulated or right after
        instantiation. Updates the _depth and _colour attributes throughout
        the tree.
        """
        # 1. Call the update depths method you wrote.
        # 2. Find the maximum depth of the tree.
        # 3. Use the maximum depth to determine the step_size.
        # 4. Call the update_colours method and use step_size as the parameter.
        self.update_depths()
        maxd = self.max_depth()
        if maxd > 1:
            step_size = math.floor(200 / (maxd - 1))
        elif maxd == 0:
            step_size = 0
        else:
            step_size = math.floor(200)
        self.update_colours(step_size)

    # **************************************************************************
    # ********* TASK 6: EXPAND, COLLAPSE, EXPAND ALL, COLLAPSE ALL *************
    # **************************************************************************

    def expand(self) -> None:
        """Sets this tree to be expanded. But not if it is a leaf.
        """
        if self._subtrees:
            self._expanded = True

    def expand_all(self) -> None:
        """Sets this tree and all its descendants to be expanded, apart from the
        leaf nodes.
        """
        if self._subtrees:
            self._expanded = True
            for sub in self._subtrees:
                sub.expand_all()

    def collapse(self, count: int = 0) -> None:
        """Collapses the parent tree of the given tree node and also collapse
        all of its descendants.
        """
        # NOTES: - This method could be called with any node on the tree.
        #        - After this method is called, the parent of the given node
        #          should not be expanded, and any node underneath this tree
        #          should not be expanded.
        #
        self._expanded = False
        if count == 1:
            for sub in self._subtrees:
                sub.collapse(count)
        else:
            if self._parent_tree:
                count = 1
                self._parent_tree.collapse(count)

    def collapse_all(self) -> None:
        """ Collapses ALL nodes in the tree.
        """

        # NOTES - This should work if it is called on any node in the tree.
        #       - After this method is called, _expanded should be set to false
        #         for all nodes in the tree.
        self._expanded = False
        if self._subtrees:
            for sub in self._subtrees:
                sub.collapse()
        if self._parent_tree:
            self._parent_tree.collapse_all()

    # **************************************************************************
    # ************* TASK 7 : DUPLICATE MOVE COPY_PASTE *************************
    # **************************************************************************

    def move(self, destination: TMTree) -> None:
        """If this tree is a leaf, and <destination> is not a leaf, moves this
        tree to be the last subtree of <destination>. Otherwise, does nothing.
        """
        if self._subtrees == [] and destination._subtrees != []:
            new = FileSystemTree(self.get_full_path())
            new.data_size = self.data_size
            new._parent_tree = destination
            destination._subtrees.append(new)
            self._parent_tree._subtrees.remove(self)
            self._parent_tree.data_size -= self.data_size

    def duplicate(self) -> Optional[TMTree]:
        """Duplicates the given tree, if it is a leaf node. It stores
        the new tree with the same parent as the given leaf. Returns the
        new node. If the given tree is not a leaf, does nothing.
        """

        # NOTES: - make good use of the FileSystemTree constructor to
        #          instantiate a new node.
        if not self._subtrees and self._parent_tree:
            path = self.get_full_path()
            new_node = FileSystemTree(path)
            new_node._parent_tree = self._parent_tree
            self._parent_tree._subtrees.append(new_node)
            return new_node
        return None

    def copy_paste(self, destination: TMTree) -> None:
        """If this tree is a leaf, and <destination> is not a leaf, this method
        copies the given, and moves the copy to the last subtree of
        <destination>. Otherwise, does nothing.
        """
        if self._subtrees == [] and destination._subtrees != []:
            path = self.get_full_path()
            new_node = FileSystemTree(path)
            new_node.data_size = self.data_size
            new_node._parent_tree = destination
            destination._subtrees.append(new_node)

    # **************************************************************************
    # ************* HELPER FUNCTION FOR TESTING PURPOSES  **********************
    # **************************************************************************

    def tree_traversal(self) -> List[Tuple[str, int, Tuple[int, int, int]]]:
        """For testing purposes to see the depth and colour attributes for each
        internal node in the tree. Used for passing test case 5.
        """
        if len(self._subtrees) > 0:
            output_list = [(self._name, self._depth, self._colour)]
            for tree in self._subtrees:
                output_list += tree.tree_traversal()
            return output_list
        else:
            return []

    # **************************************************************************
    # *********** METHODS DEFINED FOR STRING REPRESENTATION  *******************
    # **************************************************************************
    def get_path_string(self) -> str:
        """Return a string representing the path containing this tree
        and its ancestors, using the separator for this OS between each
        tree's name.
        """
        if self._parent_tree is None:
            return self._name
        else:
            return self._parent_tree.get_path_string() + \
                self.get_separator() + self._name

    def get_separator(self) -> str:
        """Returns the string used to separate names in the string
        representation of a path from the tree root to this tree.
        """
        raise NotImplementedError

    def get_suffix(self) -> str:
        """Returns the string used at the end of the string representation of
        a path from the tree root to this tree.
        """
        raise NotImplementedError

    # **************************************************************************
    # **************** HELPER FUNCTION FOR TASK 7  *****************************
    # **************************************************************************
    def get_full_path(self) -> str:
        """Returns the path attribute for this tree.
        """
        raise NotImplementedError


class FileSystemTree(TMTree):
    """A tree representation of files and folders in a file system.

    The internal nodes represent folders, and the leaves represent regular
    files (e.g., PDF documents, movie files, Python source code files, etc.).

    The _name attribute stores the *name* of the folder or file, not its full
    path. E.g., store 'assignments', not '/Users/Diane/csc148/assignments'

    The data_size attribute for regular files is simply the size of the file,
    as reported by os.path.getsize.

    === Private Attributes ===
    _path: the path that was used to instantiate this tree.
    """
    _path: str

    def __init__(self, my_path: str) -> None:
        """Stores the directory given by <my_path> into a tree data structure
        using the TMTree class.

        Precondition: <my_path> is a valid path for this computer.
        """
        # 1. Initialize the single attribute: self._path
        # 2. Implement the algorithm described in the handout.
        #
        # NOTES: - Review OS module documentation summary provided!
        #        - Remember to make good use of the superclass constructor!
        #        - Notice that the size of folders is calculated in the TMTree
        #          initializer. Thus, set data_size = 0 for the folders
        subtrees = []
        self._path = my_path
        if os.path.isdir(self._path):
            ls = os.listdir(self._path)
            for pa in ls:
                pat = os.path.join(self._path, pa)
                subtrees.append(FileSystemTree(pat))
        size = os.path.getsize(self._path)
        name = os.path.basename(self._path)
        super().__init__(name, subtrees, size)

    def get_full_path(self) -> str:
        """Returns the file path for the tree object.
        """
        return self._path

    def get_separator(self) -> str:
        """Returns the file separator for this OS.
        """
        return os.sep

    def get_suffix(self) -> str:
        """Returns the final descriptor of this tree.
        """

        def convert_size(data_size: float, suffix: str = 'B') -> str:
            suffixes = {'B': 'kB', 'kB': 'MB', 'MB': 'GB', 'GB': 'TB'}
            if data_size < 1024 or suffix == 'TB':
                return f'{data_size:.2f}{suffix}'
            return convert_size(data_size / 1024, suffixes[suffix])

        components = []
        if len(self._subtrees) == 0:
            components.append('file')
        else:
            components.append('folder')
            components.append(f'{len(self._subtrees)} items')
        components.append(convert_size(self.data_size))
        return f' ({", ".join(components)})'


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'math', 'random', 'os', '__future__'
        ]
    })

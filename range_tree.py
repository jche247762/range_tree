import node
import tree_interface

class RangeSizeTree(tree_interface.RSTreeInterface):
    """
    Range Size Tree

    Implements the Range Size Tree interface.
    Supports insertion, removal and getting the node.
    """

    def __init__(self):
        """
        Initialise the tree, root node is none.
        """
        self.root = None

    def put(self, k):
        """
        Put the value K into the tree.

        Hint McHintFace: watch out for duplicates!
        :param k: The key to insert into the tree.
        """

        node_k = node.Node(k)

        if self.root is None:
            self.root = node_k
            return

        current = self.root

        # Traverse through the tree.
        while True:
            # If it's lower than; Go left
            current.increment_subtree()
            if k <= current.get_key():
                if current.get_left() is None:
                    current.set_left(node_k)
                    node_k.set_parent(current)
                    return
                else:
                    current = current.get_left()
            # Else; Go right
            else:
                if current.get_right() is None:
                    current.set_right(node_k)
                    node_k.set_parent(current)
                    return
                else:
                    current = current.get_right()

    def get(self, k):
        """
        Get the node(s) with key `k`.
            - If there is none, return an empty array.

        E.g.
              3
           /     \
          1       5
         / \     / \
        1   2   4   6


        get(1) => returns array of both 1 (parent 1), 1 (parent 3)
        NOTE: ordered LEFT TO RIGHT!

        :param k: The key to get.
        :return: Array of Node's with key K.
        """

        return_arr = []

        # Start at the root
        current = self.root

        while current is not None:
            if k == current.get_key():
                return_arr.append(current)

            if k <= current.get_key():
                current = current.get_left()

            elif k > current.get_key():
                current = current.get_right()

        return list(reversed(return_arr))

    def remove(self, k):
        """
        Remove's the value from the tree.

        Note: with duplicates, find the "FIRST DEEPEST OCCURRENCE"

        E.g.
              3
           /     \
          1       5
         / \     / \
        1   2   4   6

        Remove (1)

              3
           /     \
          1       5
           \     / \
            2   4   6

        :param k: value to remove from the tree.
        :return: The removed node. None if node not found OR cannot be removed.
        """

        # Find the node to remove.

        current = self.root
        found_node = None
        while current is not None:
            if k == current.get_key():
                found_node = current

            if k <= current.get_key():
                current = current.get_left()
            else:
                current = current.get_right()

        # Cases (A) We couldn't find the node to remove, or (B) it has two children.
        if found_node is None:
            return None
        elif (found_node.get_left() is not None) and (found_node.get_right() is not None):
            return None

        replacement = found_node.get_left()
        if replacement is None:
            replacement = found_node.get_right()

        if found_node == self.root:
            self.root = replacement
        else:
            if found_node == found_node.get_parent().get_left():
                found_node.get_parent().set_left(replacement)
            else:
                found_node.get_parent().set_right(replacement)

            if replacement is not None:
                replacement.set_parent(found_node.get_parent())

        # Update the subtree sizes
        current = found_node.get_parent()
        while current is not None:
            current.decrement_subtree()
            current = current.get_parent()

        return found_node

    def range_size(self, a, b):
        """
        Calculates the size between two keys.
        (Inclusive!)

        e.g.
          2
         / \
        1  3

        range_size(1, 1) => 1

        e.g. #2
                    5
                /       \
              3          7
            /   \      /   \
          2      4    6     8
         / \     \        /  \
        1   3     5      8   10

        range_size(3, 7) => 7

        :param a: A key to search between.
        :param b: A key to search between.
        :return: Number of nodes between the two keys.
        """

        if self.root is None:
            return 0

        # Shortcut - if there's only one range, count the number of nodes.
        if a == b:
            return len(self.get(a))

        low = a if a < b else b
        high = b if a < b else a

        current = self.root
        low_count = 0

        # Check the root
        if low <= self.root.get_key():
            current = self.root.get_left()
        else:
            current = self.root.get_right()

        while current is not None:
            if low <= current.get_key():
                if high >= current.get_key() >= low:
                    low_count += 1
                if current.get_right() is not None and current.get_right().get_key() >= low:
                    low_count += current.get_right().get_subtree_size()
                current = current.get_left()
            else:
                current = current.get_right()

        current = self.root
        high_count = 0

        if self.root.get_key() <= high:
            current = self.root.get_right()
        else:
            current = self.root.get_left()

        while current is not None:
            if current.get_key() <= high:
                if low <= current.get_key() <= high:
                    high_count += 1
                if current.get_left() is not None and current.get_left().get_key() <= high:
                    high_count += current.get_left().get_subtree_size()
                current = current.get_right()
            else:
                current = current.get_left()

        # Count the roots
        count = 0
        if low <= self.root.get_key() <= high:
            count += 1
        count += low_count + high_count

        return count


################################################################################
# The following functions are not tested
# They are provided for you to run and test.
################################################################################

def main():
    pass


if __name__ == "__main__":
    print("Running main method of RangeSizeTree")
    main()
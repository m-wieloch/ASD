#!/usr/bin/python
# -*- coding: utf-8 -*-
# Maciej Wieloch, 303080


class Element:
    def __init__(self, key, data):
        self.key = key
        self.data = data
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def search(self, key, element=None):
        if element is None:
            element = self.root

        if element.key == key:
            return element.data
        elif element.key < key:
            if element.right is not None:
                element = self.search(key, element.right)
            else:
                element = None
        elif element.key > key:
            if element.left is not None:
                element = self.search(key, element.left)
            else:
                element = None
        return element

    def insert(self, key, data):
        new_element = Element(key, data)
        if self.root is None:
            self.root = new_element
        else:
            element = self.root
            insertion = False

            while not insertion:
                if element.key < key:
                    if element.right is None:
                        element.right = new_element
                        insertion = True
                    else:
                        element = element.right
                if element.key > key:
                    if element.left is None:
                        element.left = new_element
                        insertion = True
                    else:
                        element = element.left
                if element.key == key:
                    element.data = data
                    insertion = True

    def delete(self, key):
        previous_element = None
        actual_element = self.root
        deleted = False

        while not deleted:
            if key < actual_element.key:
                previous_element = actual_element
                actual_element = actual_element.left

            elif key > actual_element.key:
                previous_element = actual_element
                actual_element = actual_element.right

            elif actual_element.key == key:
                # no child nodes
                if actual_element.right is None and actual_element.left is None:
                    if previous_element.right == actual_element:
                        previous_element.right = None
                        deleted = True
                    elif previous_element.left == actual_element:
                        previous_element.left = None
                        deleted = True
                # one child node
                elif actual_element.right is None and actual_element.left is not None:
                    if previous_element.right == actual_element:
                        previous_element.right = actual_element.left
                        deleted = True
                    elif previous_element.left == actual_element:
                        previous_element.left = actual_element.left
                        deleted = True
                elif actual_element.right is not None and actual_element.left is None:
                    if previous_element.right == actual_element:
                        previous_element.right = actual_element.right
                        deleted = True
                    elif previous_element.left == actual_element:
                        previous_element.left = actual_element.right
                        deleted = True
                # two child nodes
                elif actual_element.right is not None and actual_element.left is not None:
                    old_parent = actual_element
                    new_parent = None

                    previous_element = actual_element
                    actual_element = actual_element.right

                    while new_parent is None:
                        if actual_element.left is None:
                            new_parent = actual_element
                            if new_parent.right is not None and previous_element is not old_parent:
                                previous_element.left = new_parent.right
                            elif previous_element is not old_parent:
                                previous_element.left = None
                            elif previous_element is old_parent:
                                previous_element.right = new_parent.right
                        else:
                            previous_element = actual_element
                            actual_element = actual_element.left

                    old_parent.key = new_parent.key
                    old_parent.data = new_parent.data
                    deleted = True

    def print(self):
        return self._print(self.root)

    def _print(self, root):
        if root.left is not None:
            self._print(root.left)

        print('Key: {}, Value = {}'.format(root.key, root.data))

        if root.right is not None:
            self._print(root.right)

    def height(self):
        return self._height(self.root)

    def _height(self, root):
        if root is not None:
            left_element = self._height(root.left)
            right_element = self._height(root.right)

            if left_element < right_element:
                return 1 + right_element
            else:
                return 1 + left_element
        else:
            return 0

    def print_tree(self):
        print("==============")
        self._print_tree(self.root, 0)
        print("==============")

    def _print_tree(self, node, lvl):
        if node is not None:
            self._print_tree(node.right, lvl + 10)

            print()
            for i in range(10, lvl + 10):
                print(end=" ")
            print(node.key)
            self._print_tree(node.left, lvl + 10)


if __name__ == '__main__':
    test = BST()
    keys = [50, 15, 62, 5, 20, 58, 91, 3, 8, 37, 60, 24]
    dataset = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']

    for i in range(len(keys)):
        test.insert(keys[i], dataset[i])

    print('Drzewo 2D:')
    test.print_tree()
    test.print()
    key = 24
    print('\nWartosc pod kluczem: {} jest rowna: {}\n'.format(key, test.search(24)))
    test.insert(15, 'AA')
    test.insert(6, 'M')
    test.delete(62)
    test.insert(59, 'N')
    test.insert(100, 'P')
    test.delete(8)
    test.delete(15)
    test.insert(55, 'R')
    test.delete(50)
    test.delete(5)
    test.delete(24)
    print('Wysokosc drzewa wynosi: {}\n'.format(test.height()))
    test.print()
    print('\nDrzewo 2D:')
    test.print_tree()

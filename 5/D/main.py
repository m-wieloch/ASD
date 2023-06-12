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


class AVL(BST):
    def RR(self, actual_element):
        left_element = actual_element.left
        previous_element = left_element.right
        left_element.right = actual_element
        actual_element.left = previous_element

        return left_element

    def LR(self, actual_element):
        right_element = actual_element.right
        previous_element = right_element.left
        right_element.left = actual_element
        actual_element.right = previous_element

        return right_element

    def rate(self, element):
        if element is None:
            return 0
        else:
            return self._height(element.left) - self._height(element.right)

    def balance(self, element):
        element_rate = self.rate(element)

        right_element = element.right
        left_element = element.left
        right_element_rate = self.rate(right_element)
        left_element_rate = self.rate(left_element)

        if element_rate < -1:
            if right_element_rate > 0:
                element.right = self.RR(right_element)
                return self.LR(element)
            else:
                return self.LR(element)

        elif element_rate > 1:
            if left_element_rate < 0:
                element.left = self.LR(left_element)
                return self.RR(element)
            else:
                return self.RR(element)
        else:
            return element

    def insert(self, key, data):
        new_element = Element(key, data)
        previous_elements = {}

        if self.root is None:
            self.root = new_element
        else:
            element = self.root
            insertion = False

            while not insertion:
                if element.key < key:
                    previous_elements[element] = -1
                    if element.right is None:
                        element.right = new_element
                        insertion = True
                    else:
                        element = element.right
                if element.key > key:
                    previous_elements[element] = 1
                    if element.left is None:
                        element.left = new_element
                        insertion = True
                    else:
                        element = element.left
                if element.key == key:
                    element.data = data
                    insertion = True

        # Balancing tree after inserting
        elements_to_balance = list(previous_elements.keys())
        for bkey in range(len(elements_to_balance) - 2):
            index = -1 - bkey - 2
            rebalance = self.balance(elements_to_balance[index + 1])

            if previous_elements[elements_to_balance[index]] == -1:
                elements_to_balance[index].right = rebalance
            else:
                elements_to_balance[index].left = rebalance

        self.root = self.balance(self.root)

    def delete(self, key):
        previous_element = None
        actual_element = self.root
        deleted = False
        previous_elements = {}

        while not deleted:
            if key < actual_element.key:
                previous_elements[actual_element] = 1
                previous_element = actual_element
                actual_element = actual_element.left

            elif key > actual_element.key:
                previous_elements[actual_element] = -1
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

        # Balancing tree after deleting
        elements_to_balance = list(previous_elements.keys())
        for bkey in range(len(elements_to_balance) - 2):
            index = -1 - bkey - 1
            rebalance = self.balance(elements_to_balance[index + 1])

            if previous_elements[elements_to_balance[index]] == -1:
                elements_to_balance[index].right = rebalance
            else:
                elements_to_balance[index].left = rebalance

        self.root = self.balance(self.root)


if __name__ == '__main__':
    test = AVL()
    keys = [50, 15, 62, 5, 2, 1, 11, 100, 7, 6, 55, 52, 51, 57, 8, 9, 10, 99, 12]
    dataset = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'R', 'S', 'T']

    for idx in range(len(keys)):
        test.insert(keys[idx], dataset[idx])

    print('Drzewo 2D:')
    test.print_tree()
    test.print()
    skey = 10
    print('\nWartosc pod kluczem: {} jest rowna: {}\n'.format(skey, test.search(skey)))

    rem_keys = [50, 52, 11, 57, 1, 12]
    print('Usuwam nastepujace klucze z drzewa: {}'.format(rem_keys))
    for idx in range(len(rem_keys)):
        test.delete(rem_keys[idx])

    print('Dodaje klucz 3 o wartosci AA')
    test.insert(3, 'AA')

    print('Dodaje klucz 4 o wartosci AA')
    test.insert(4, 'BB')

    print('Usuwam klucz 7')
    test.delete(7)

    print('Usuwam klucz 8')
    test.delete(8)

    print('Drzewo 2D:')
    test.print_tree()
    test.print()

#!/usr/bin/python
# -*- coding: utf-8 -*-
# Maciej Wieloch, 303080


class Element:
    def __init__(self):
        self.keys = []
        self.children = []
        self.is_last = False

    def size(self):
        return len(self.keys)


class Btree:
    def __init__(self, max_size):
        self.max_size = max_size
        self.min_size = (max_size + 1) // 2
        self.root = Element()
        self.root.is_last = True

    def insert(self, key):
        if not self.root.size() is self.max_size:
            self.insert_as_child(self.root, key)
        else:
            root = self.root

            element = Element()
            self.root = element
            element.children.append(root)

            # Nastepuje podzial potomka
            child = element.children[0]

            next_element = Element()
            next_element.is_last = child.is_last

            element.children.insert(1, next_element)
            element.keys.append(child.keys[self.min_size - 1])

            next_element.keys = child.keys[self.min_size: self.max_size]
            child.keys = child.keys[0: self.min_size - 1]

            if not child.is_last:
                next_element.children = child.children[self.min_size: self.max_size + 1]
                child.children = child.children[0: self.min_size]

            self.insert_as_child(element, key)

    def insert_as_child(self, element, key):
        index = element.size() - 1

        if not element.is_last:
            while index >= 0 and key < element.keys[index]:
                index = index - 1

            index = index + 1
            if element.children[index].size() == self.max_size:

                # Nastepuje podzial potomka
                child = element.children[index]

                next_element = Element()
                next_element.is_last = child.is_last

                element.children.insert(index + 1, next_element)
                element.keys.insert(index, child.keys[self.min_size - 1])

                next_element.keys = child.keys[self.min_size: self.max_size]
                child.keys = child.keys[0: self.min_size - 1]

                if not child.is_last:
                    next_element.children = child.children[self.min_size: self.max_size + 1]
                    child.children = child.children[0: self.min_size]

                if key > element.keys[index]:
                    index = index + 1

            self.insert_as_child(element.children[index], key)

        else:
            element.keys.append(0)

            while index >= 0 and key < element.keys[index]:
                element.keys[index + 1] = element.keys[index]
                index = index - 1

            element.keys[index + 1] = key

    def print_tree(self):
        print("==============")
        self._print_tree(self.root, 0)
        print("==============")

    def _print_tree(self, node, lvl):
        if node.size() > 0:
            for i in range(node.size() + 1):
                if len(node.children) > 0:
                    self._print_tree(node.children[i], lvl + 1)
                if i < node.size():
                    print(lvl * '  ', node.keys[i])


if __name__ == '__main__':

    test = Btree(3)
    dataset = [5, 17, 2, 14, 7, 4, 12, 1, 16, 8, 11, 9, 6, 13, 0, 3, 18, 15, 10, 19]
    for i in dataset:
        test.insert(i)

    print('Dodanie kluczy do drzewa z listy: {}'.format(dataset))
    test.print_tree()

    test1 = Btree(3)
    for i in range(0, 20):
        test1.insert(i)

    print('\nDodanie tych samych 20 liczb do nowego drzewa kolejno od 0 do 19:')
    test1.print_tree()

    for i in range(20, 200):
        test1.insert(i)

    print('\nDodanie 180 liczb do drzewa kolejno od 20 do 199:')
    test1.print_tree()

    test2 = Btree(5)
    for i in range(0, 200):
        test2.insert(i)
    print('\nDodanie 200 liczb do nowego drzewa kolejno od 0 do 199:')
    test2.print_tree()


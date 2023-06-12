#!/usr/bin/python
# -*- coding: utf-8 -*-
# Maciej Wieloch, 303080

import random


class Element:
    def __init__(self, key, data, level):
        self.key = key
        self.data = data
        self.level = level
        self.next = [None for _ in range(self.level)]


class SkipList:
    def __init__(self, m_level):
        self.m_level = m_level
        self.head = Element(-1, None, self.m_level)
        self.level = 0

    def __str__(self):
        element = self.head.next[0]
        result = '\n'
        while element is not None:
            result = result + 'Key: ' + str(element.key) + ', Value = ' + str(element.data) + '\n'
            element = element.next[0]
        return result

    def search(self, key):
        actual = self.head

        for i in reversed(range(self.level)):
            while actual.next[i] and actual.next[i].key < key:
                actual = actual.next[i]

        actual = actual.next[0]

        if actual is not None and actual.key is key:
            return actual.data
        else:
            return 'Could not find given key.'

    def insert(self, key, data):
        result = [None for _ in range(self.m_level)]
        actual = self.head

        for i in reversed(range(self.level)):
            while actual.next[i] and actual.next[i].key < key:
                actual = actual.next[i]
            result[i] = actual

        actual = actual.next[0]

        if actual is not None and actual.key is key:
            actual.data = data
        else:
            new_level = self.random_level()

            if new_level > self.level:
                new_level = self.level + 1
                self.level = new_level
                result[new_level - 1] = self.head

            new_element = Element(key, data, new_level)

            for i in range(new_level):
                new_element.next[i] = result[i].next[i]
                result[i].next[i] = new_element

    def remove(self, key):
        result = [None for _ in range(self.m_level)]
        actual = self.head

        for i in reversed(range(self.level)):
            while actual.next[i] and actual.next[i].key < key:
                actual = actual.next[i]
            result[i] = actual

        actual = actual.next[0]

        if actual is not None and actual.key is key:
            for i in range(self.level):
                if result[i].next[i] is not actual:
                    break

                result[i].next[i] = actual.next[i]

            while self.head.next[self.level - 1] is self.head and 1 < self.level:
                self.level = self.level - 1

    def random_level(self, p=0.5):
        lvl = 1
        while random.random() < p and lvl < self.m_level:
            lvl = lvl + 1
        return lvl

    def displayList_(self):
        node = self.head.next[0]  # pierwszy element na poziomie 0
        keys = []  # lista kluczy na tym poziomie
        while node is not None:
            keys.append(node.key)
            node = node.next[0]

        for lvl in range(self.m_level - 1, -1, -1):
            print("{}: ".format(lvl), end=" ")
            node = self.head.next[lvl]
            idx = 0
            while node is not None:
                while node.key > keys[idx]:
                    print("  ", end=" ")
                    idx += 1
                idx += 1
                print("{:2d}".format(node.key), end=" ")
                node = node.next[lvl]
            print("")


if __name__ == '__main__':
    print('Tworze pusta liste z przeskokami o poziomie rownym 4')
    test = SkipList(4)
    test.displayList_()

    print('Wypelniam liste 15 kolejnymi kluczami o wartosci kolejnych liter:')
    keys = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    dataset = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o']

    for i in range(len(keys)):
        test.insert(keys[i], dataset[i])

    print('Wyswietlam wypelniona liste:')
    test.displayList_()
    print(test)

    print('Korzystajac z search, dana pod kluczem 2 wynosi: {}'.format(test.search(2)))
    print('Zamieniam dana pod kluczem 2 na wartosc: ASD')
    test.insert(2, 'ASD')
    print('Korzystajac z search, dana pod kluczem 2 wynosi: {}'.format(test.search(2)))
    print('Usuwam klucze nr: 5, 6, 7')
    test.remove(5)
    test.remove(6)
    test.remove(7)

    print('Wyswietlam liste po skasowaniu elementow:')
    test.displayList_()
    print(test)

    print('Wstawiam wartosc test pod klucz nr 6:')
    test.insert(6, 'test')

    print('Wyswietlam liste po dodaniu elementu:')
    test.displayList_()
    print(test)

#!/usr/bin/python
# -*- coding: utf-8 -*-
# Maciej Wieloch, 303080


class Element:
    def __init__(self, key, data):
        self.key = key
        self.data = data


def size_check(size):
    if size == 2:
        return True
    elif size % 2 == 0 or size <= 1:
        return False

    eq = int(size ** 0.5) + 1

    for i in range(3, eq, 2):
        if size % i == 0:
            return False
    return True


class MixedTable:
    def __init__(self, size, c1=1, c2=0):
        if size_check(size):
            self.size = size
        else:
            raise ValueError('Size must be odd number and != 1')

        self.c1 = c1
        self.c2 = c2
        self.tab = [None for _ in range(self.size)]
        self.elements = 0
        self.step = 1

    def __str__(self):
        result = ''
        for i in self.tab:
            if i is not None:
                result = result + str(i.key) + ': ' + str(i.data) + ' '
            else:
                result = result + "None "
        return result

    def mix(self, data):
        if isinstance(data, str):
            result = 0
            for c in data:
                result = result + ord(c)
            return self.mix(result)
        result = data % len(self.tab)
        return result

    def solve(self, data, step=1):
        result = (self.mix(data) + self.c1 * step + self.c2 * step ** 2) % self.size
        self.step = self.step + 1
        return result

    def search(self, key):
        found = False
        for element in self.tab:
            if element is not None:
                ek, ed = element.key, element.data
                if ek == key:
                    found = True
                    break
            else:
                found = False
        if found:
            return ed
        else:
            print("Given key not found")

    def insert(self, key, data, origin=None):
        if origin is None:
            mixed_key = self.mix(key)
        else:
            mixed_key = self.solve(key)

        if self.tab[mixed_key] is None:
            if origin is None:
                self.tab[mixed_key] = Element(key, data)
                self.elements = self.elements + 1
                self.step = 1
            else:
                self.tab[mixed_key] = Element(origin, data)
                self.elements = self.elements + 1
                self.step = 1

        else:
            if self.tab[mixed_key].key == key and (origin == key or origin is None):
                self.tab[mixed_key] = Element(key, data)
                if self.elements == self.size:
                    self.step = 1
                    return None

            mixed_key = self.solve(key)

            if origin is None:
                self.insert(mixed_key, data, key)
            else:
                if self.elements == self.size:
                    for i in self.tab:
                        if i.key == origin:
                            self.insert(mixed_key, data, origin)
                    print('Table is full, cant add data {} with key {}'.format(data, origin))
                    self.step = 1
                    return None
                else:
                    self.insert(mixed_key, data, origin)

    def remove(self, key):
        found = False
        for element in self.tab:
            if element is not None:
                ek = element.key
                if ek == key:
                    found = True
                    break

        if found:
            self.tab[key] = None
            self.elements = self.elements - 1
        else:
            print("Cant remove - given key not found")


def test1():
    print('========Test 1========')

    testTable = MixedTable(13)
    print('Tworze pusta tablice: {}'.format(testTable))

    print('Probuje wpisac wszystkie elementy:')
    testTable.insert(1, 'a')
    testTable.insert(2, 'b')
    testTable.insert(3, 'c')
    testTable.insert(4, 'd')
    testTable.insert(5, 'e')
    testTable.insert(18, 'f')
    testTable.insert(31, 'g')
    testTable.insert(8, 'h')
    testTable.insert(9, 'i')
    testTable.insert(10, 'j')
    testTable.insert(11, 'k')
    testTable.insert(12, 'l')
    testTable.insert(13, 'm')
    testTable.insert(14, 'n')
    testTable.insert(15, 'o')

    print('Tablica po wpisaniu elementow: {}'.format(testTable))

    print('Klucz 5: {}'.format(testTable.search(5)))
    print('Klucz 14: {}'.format(testTable.search(14)))

    print('Zamieniam wartosc klucza 5 na HelloWorld:')
    testTable.insert(5, 'HelloWorld')
    print('Klucz 5: {}'.format(testTable.search(5)))

    print('Usuwam zawartosc klucza 5: ')
    testTable.remove(5)
    print('Tablica po skasowaniu klucza: {}'.format(testTable))

    print('W klucz: "test" wrzucam daną "A":')
    testTable.insert('test', 'A')
    print('Wypisuje tablice: {}'.format(testTable))


def test2_1():
    print('\n========Test 2-1, c1=0, c2=1========')
    keys = [i * 13 for i in range(1, 16)]
    data = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o']

    testTable = MixedTable(size=13, c1=0, c2=1)

    for i in range(len(keys)):
        testTable.insert(keys[i], data[i])

    print(testTable)


def test2_2():
    print('\n========Test 2-2, c1=1, c2=0========')
    keys = [i * 13 for i in range(1, 16)]
    data = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o']

    testTable = MixedTable(13)

    for i in range(len(keys)):
        testTable.insert(keys[i], data[i])

    print(testTable)


def test2_3():
    print('\n========Test 2-3, c1=0, c2=1========')

    testTable = MixedTable(13, 0, 1)

    testTable.insert(1, 'a')
    testTable.insert(2, 'b')
    testTable.insert(3, 'c')
    testTable.insert(4, 'd')
    testTable.insert(5, 'e')
    testTable.insert(18, 'f')
    testTable.insert(31, 'g')
    testTable.insert(8, 'h')
    testTable.insert(9, 'i')
    testTable.insert(10, 'j')
    testTable.insert(11, 'k')
    testTable.insert(12, 'l')
    testTable.insert(13, 'm')
    testTable.insert(14, 'n')
    testTable.insert(15, 'o')

    print(testTable)


if __name__ == '__main__':
    test1()
    test2_1()
    test2_2()
    test2_3()

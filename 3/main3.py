#!/usr/bin/python
# -*- coding: utf-8 -*-
# Maciej Wieloch, 303080


class Queue:
    def __init__(self, size=5):
        self.tab = [None for i in range(size)]

        if size == 5:
            self.size = size
        else:
            self.size = len(self.tab)

        self.save_index = 0
        self.load_index = 0

    def __str__(self):
        s = '\nTablica: [ '
        for i in self.tab:
            if i is None:
                s = s + 'None '
            else:
                s = s + str(i) + ' '
        s = s + ']\nRozmiar tablicy: ' + str(self.size)
        s = s + '\nIndeks zapisywania: ' + str(self.save_index)
        s = s + '\nIndeks odczytywania: ' + str(self.load_index)
        return s

    def realloc(self, size):
        old_size = len(self.tab)
        return [self.tab[i] if i < old_size else None for i in range(size)]

    def is_empty(self):
        if self.save_index == self.load_index:
            return True
        else:
            return False

    def peek(self):
        return self.tab[self.load_index]

    def dequeue(self):
        if not self.is_empty():
            result = self.tab[self.load_index]

            self.tab[self.load_index] = None
            self.load_index = (self.load_index + 1) % self.size

            return result
        else:
            return None

    def enqueue(self, data):
        self.tab[self.save_index] = data
        self.save_index = (self.save_index + 1) % self.size

        if self.save_index == self.load_index:
            temp_tab = self.realloc(self.size * 2)

            for i in range(len(temp_tab)):
                temp_tab[i] = None
                self.save_index = i
                if self.save_index >= len(self.tab):
                    self.load_index = self.save_index - len(self.tab)
                    temp_tab[self.save_index] = self.tab[self.load_index]

            self.tab = temp_tab
            self.save_index = 0
            self.load_index = self.size
            self.size = self.size*2


if __name__ == '__main__':
    myQueue = Queue()
    print('Tworzę pustą kolejkę: {}'.format(myQueue.tab))

    elements = [1, 2, 3, 4]
    print('Wpisuje do niej nastepujące elementy: {}'.format(elements))

    for i in elements:
        myQueue.enqueue(i)

    print('Tablica kolejki po dopisaniu 4 elementów (enqueue): {}'.format(myQueue.tab))
    print('Korzystam z funkcji dequeue: {}'.format(myQueue.dequeue()))
    print('Korzystam z funkcji peek: {}'.format(myQueue.peek()))
    print('Obecny wygląd kolejki: {}'.format(myQueue))

    elements2 = [5, 6, 7, 8]

    print('Wpisuje do niej nastepujące elementy: {}'.format(elements2))

    for i in elements2:
        myQueue.enqueue(i)

    print('Tablica kolejki po dopisaniu kolejnych 4 elementów elementów (enqueue): {}'.format(myQueue.tab))

    print('Opróżnianie kolejki: ')
    for i in range(len(myQueue.tab)):
        if myQueue.tab[myQueue.load_index] is None:
            break
        print('Usuwane dane: {}'.format(myQueue.dequeue()))

    print('Obecny wygląd kolejki: {}'.format(myQueue))

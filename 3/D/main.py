#!/usr/bin/python
# -*- coding: utf-8 -*-
# Maciej Wieloch, 303080


Element_size = 6


class Element:
    def __init__(self):
        self.tab = [None for _ in range(Element_size)]
        # Liczba znajdujacych sie elementow
        self.contents = 0
        # Nastepny Element
        self.next = None

    def __str__(self):
        return str(self.tab)

    def add(self, data, index):
        # Straznik poprawnosci indexu
        if index > len(self.tab) - 1 or index < 0:
            raise IndexError('Index out of range [Element.add]')
        elif self.tab[index] is None:
            self.tab[index] = data
            self.contents = self.contents + 1
        else:
            # TODO
            self.tab[index:] = [self.tab[-1:index]] + self.tab[index:-1]
            self.tab[index] = data

            # Po przesunieciu/nadpisaniu konieczne jest obliczanie zajetosci tablicy na nowo
            self.contents = 0
            for i in range(len(self.tab)):
                if self.tab[i] is not None:
                    self.contents = self.contents + 1

    def delete(self, index):
        # Straznik poprawnosci indexu
        if index > len(self.tab) - 1 or index < 0:
            raise IndexError('Index out of range [Element.delete]')
        elif self.tab[index] is not None:
            deletion = self.tab[index]
            for i in range(index, (len(self.tab) - 1)):
                self.tab[i] = self.tab[i + 1]
                self.tab[i + 1] = None
            self.contents = self.contents - 1
            return deletion
        else:
            return 'Nothing to remove'


class UnrolledLinkedList:
    def __init__(self):
        self.head = None
        self.elements = 0

    def __str__(self):
        if self.head is None:
            return '[]'

        result = '['
        element = self.head

        while element is not None:
            result = result + '['

            for i in range(0, Element_size):
                result = result + str(element.tab[i])
                if i + 1 < Element_size:
                    result = result + ', '

            result = result + ']'

            if element.next is not None:
                result = result + ', '

            element = element.next

        result = result + ']'
        return result

    def get(self, index):
        if self.head is None:
            return 'List is empty'
        else:
            element_actual = self.elements
            element_goal = int(index/Element_size) + 1
            element = self.head

            while element_goal is not element_actual:
                element = element.next
                element_actual = element_actual - 1

            if element_actual == element_goal:
                index = index % Element_size
                return element.tab[index]

    def insert(self, data, index):
        if self.head is None:
            self.head = Element()
            self.elements = self.elements + 1
            self.head.add(data, index)
        else:
            element_actual = self.elements
            element_goal = int(index/Element_size) + 1
            element = self.head
            element_previous = None

            while element_goal is not element_actual:
                element_previous = element
                element = element.next
                element_actual = element_actual - 1

            if element_actual == element_goal:
                index = index % Element_size
                element.add(data, index)

            if element.contents == Element_size:
                next_elem = element
                content_to_move = int(Element_size / 2)

                new_element = Element()
                self.elements = self.elements + 1
                split_index = 0

                while next_elem.tab[content_to_move] is not None:
                    content = next_elem.delete(content_to_move)
                    new_element.add(content, split_index)
                    split_index = split_index + 1

                new_element.next = next_elem

                if element_previous is None:
                    self.head = new_element
                else:
                    element_previous.next = new_element

    def delete(self, index):
        if self.head is None:
            return 'List is empty'
        else:
            element_actual = self.elements
            element_goal = int(index/Element_size) + 1
            element = self.head
            element_previous = None
            element_previous2 = None

            while element_goal is not element_actual:
                element_previous2 = element_previous
                element_previous = element
                element = element.next
                element_actual = element_actual - 1

            if element_actual == element_goal:
                index = index % Element_size
                element.delete(index)

            if element.tab[int(Element_size / 2) - 1] is None:
                element.add(element_previous.delete(0), int(Element_size / 2) - 1)

                if element_previous.tab[int(Element_size / 2) - 1] is None:
                    ins_idx = int(Element_size / 2)

                    while element_previous.tab[0] is not None:
                        element.add(element_previous.delete(0), ins_idx)
                        ins_idx = ins_idx + 1

                    element_previous2.next = element


if __name__ == '__main__':
    Element_size = 6
    print('\nZmienna reprezentujaca rozmiar tabilcy ma wartosc = {}'.format(Element_size))
    print('Tworze liste...')
    myList = UnrolledLinkedList()
    print('Wyswietlam pusta liste: {}\n'.format(myList))

    data = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    for idx in range(9):
        print('Umieszczam dana = {} pod indeksem = {}'.format(data[idx], idx))
        myList.insert(data[idx], idx)

    print('\nLista po uzupelnieniu danymi: \n{}'.format(myList))
    print('Format: head, head.next, head.next.next')
    print('\nKorzystam z funkcji get do wypisania 4 elementu listy pod indeksem nr 3: {}'.format(myList.get(3)))

    print('\nUmieszczam dana = {} pod indeksem = {}'.format(10, 1))
    myList.insert(10, 1)

    print('Umieszczam dana = {} pod indeksem = {}'.format(11, 8))
    myList.insert(11, 8)

    print('\nAktualny stan listy: \n{}'.format(myList))

    print('\nUsuwam wartosc spod indeksu = {}'.format(1))
    myList.delete(1)
    print('\nUsuwam wartosc spod indeksu = {}'.format(2))
    myList.delete(2)

    print('\nLista po operacji usuwania dancych: \n{}'.format(myList))



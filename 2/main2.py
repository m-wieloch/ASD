#!/usr/bin/python
# -*- coding: utf-8 -*-
# Maciej Wieloch, 303080


class Element:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def __str__(self):
        if self.head is None:
            return '[]'
        else:
            result = '['
            result = result + str(self.head.data)
            next_elem = self.head.next

            while next_elem is not None:
                result = result + ' -> ' + str(next_elem.data)
                next_elem = next_elem.next
            return result + ']'

    def destroy(self):
        self.head = None

    def add(self, add_data):
        add_element = Element(add_data)
        add_element.next = self.head
        self.head = add_element

    def add_to_end(self, add_data):
        add_element = Element(add_data)
        if self.head is None:
            add_element.next = self.head
            self.head = add_element
        else:
            next_elem = self.head

            while next_elem is not None:
                if next_elem.next is None:
                    next_elem.next = add_element
                    break
                next_elem = next_elem.next

    def remove(self):
        if self.head is None:
            return 'Cant remove first element from empty list'
        else:
            self.head = self.head.next

    def remove_from_end(self):
        if self.head is None:
            return 'Cant remove element from empty list'
        else:
            next_elem = self.head

            while next_elem is not None:
                if next_elem.next.next is None:
                    next_elem.next = None
                    break
                next_elem = next_elem.next

    def is_empty(self):
        if self.head is None:
            return True
        else:
            return False

    def length(self):
        if self.head is not None:
            counter = 0
            next_elem = self.head

            while next_elem is not None:
                counter = counter + 1
                next_elem = next_elem.next
            return counter
        else:
            return 0

    def get(self):
        return self.head.data

    def reverse(self):
        last_elem = None
        elem = self.head

        while elem is not None:
            next_elem = elem.next
            elem.next = last_elem
            last_elem = elem
            elem = next_elem

        self.head = last_elem

    def take(self, n):
        result = LinkedList()

        if self.is_empty():
            return result

        if n > self.length():
            n = self.length()

        list_length = result.length()
        copy_of_list = self.head

        while list_length < n:
            result.add_to_end(copy_of_list.data)
            copy_of_list = copy_of_list.next
            list_length = result.length()

        return result

    def drop(self, n):
        result = LinkedList()

        if self.is_empty():
            return result

        if n > self.length():
            return result

        copy_of_list = self.head

        for i in range(n):
            copy_of_list = copy_of_list.next

        while copy_of_list.data is not None:
            result.add_to_end(copy_of_list.data)
            if copy_of_list.next is not None:
                copy_of_list = copy_of_list.next
            else:
                break

        return result


if __name__ == '__main__':
    """
    Dane:
    [('AGH', 'Kraków', 1919),
    ('UJ', 'Kraków', 1364),
    ('PW', 'Warszawa', 1915)
    ('UW', 'Warszawa', 1915)
    ('UP', 'Poznań', 1919)
    ('PG', 'Gdańsk', 1945)]
    """

    data_on_universities = LinkedList()
    print('Printuje pustą listę : {}'.format(data_on_universities))
    print('Czy lista jest pusta? : {}'.format(data_on_universities.is_empty()))
    print('Dodaje trzy elementy na poczatek listy...')
    data_on_universities.add(('PW', 'Warszawa', 1915))
    data_on_universities.add(('UJ', 'Kraków', 1364))
    data_on_universities.add(('AGH', 'Kraków', 1919))
    print('Printuje listę : {}'.format(data_on_universities))
    print('Dodaje reszte elementow na koniec listy...')
    data_on_universities.add_to_end(('UW', 'Warszawa', 1915))
    data_on_universities.add_to_end(('UP', 'Poznań', 1919))
    data_on_universities.add_to_end(('PG', 'Gdańsk', 1945))
    print('Printuje listę : {}'.format(data_on_universities))
    print('Czy lista jest pusta? : {}'.format(data_on_universities.is_empty()))
    print('Usuwam element z poczatku...')
    data_on_universities.remove()
    print('Printuje listę : {}'.format(data_on_universities))
    print('Usuwam element z konca...')
    data_on_universities.remove_from_end()
    print('Printuje listę : {}'.format(data_on_universities))
    print('Liczba elementow w liscie wynosi: {}'.format(data_on_universities.length()))
    print('Pierwszy element listy to: {}'.format(data_on_universities.get()))
    print('Odwracam liste...')
    data_on_universities.reverse()
    print('Printuje listę : {}'.format(data_on_universities))
    print('Pierwszy element listy to: {}'.format(data_on_universities.get()))
    print('Dwa pierwsze elementy listy to: {}'.format(data_on_universities.take(2)))
    print('Dwa ostatnie elementy listy to: {}'.format(data_on_universities.drop(2)))
    print('Kasuje liste...')
    data_on_universities.destroy()
    print('Printuje listę po jej skasowaniu: {}'.format(data_on_universities))

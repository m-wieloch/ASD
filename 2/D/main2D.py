#!/usr/bin/python
# -*- coding: utf-8 -*-
# Maciej Wieloch, 303080


class Element:
    def __init__(self, data):
        self.data = data
        self.next = None


def nil():
    return None


def create():
    return nil()


def destroy():
    return nil()


def cons(el, llist):
    if llist is not None:
        el.next = llist
        return el
    else:
        return el


def first(llist):
    return llist.data


def rest(llist):
    return llist.next


def add(el, llist):
    return cons(el, llist)


def add_to_end(el, llist):
    if is_empty(llist):
        return cons(el, llist)
    else:
        return cons(Element(first(llist)), add_to_end(el, rest(llist)))


def remove(llist):
    if llist is None:
        return None
    else:
        return rest(llist)


def remove_from_end(llist):
    return reverse(remove(reverse(llist)))


def is_empty(llist):
    if llist is None:
        return True
    else:
        return False


def length(llist):
    if llist is None:
        return 0
    else:
        return length(rest(llist)) + 1


def get(llist):
    return first(llist)


def reverse(llist):
    if length(llist) <= 1:
        return llist
    else:
        return add_to_end(Element(first(llist)), reverse(rest(llist)))


def take(llist, n):
    if is_empty(llist) or n >= length(llist):
        return llist
    else:
        if n == 0:
            return None
        if n == 1:
            return Element(first(llist))

        return cons(Element(first(llist)), take(rest(llist), n - 1))


def drop(llist, n):
    if n == 0:
        return llist
    if n >= length(llist):
        return None
    else:
        return drop(rest(llist), n - 1)


def llist_print(llist):
    if llist is None:
        return '[]'
    else:
        result = '['
        result = result + str(llist.data)
        next_elem = llist.next

        while next_elem is not None:
            result = result + ' -> ' + str(next_elem.data)
            next_elem = next_elem.next
        return result + ']'


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

    data_on_universities = create()
    print('Printuje pustą listę : {}'.format(llist_print(data_on_universities)))
    print('Czy lista jest pusta? : {}'.format(is_empty(data_on_universities)))
    print('Dodaje trzy elementy na poczatek listy...')
    data_on_universities = add(Element(('PW', 'Warszawa', 1915)), data_on_universities)
    data_on_universities = add(Element(('UJ', 'Kraków', 1364)), data_on_universities)
    data_on_universities = add(Element(('AGH', 'Kraków', 1919)), data_on_universities)
    print('Printuje listę : {}'.format(llist_print(data_on_universities)))
    print('Dodaje reszte elementow na koniec listy...')
    data_on_universities = add_to_end(Element(('UW', 'Warszawa', 1915)), data_on_universities)
    data_on_universities = add_to_end(Element(('UP', 'Poznań', 1919)), data_on_universities)
    data_on_universities = add_to_end(Element(('PG', 'Gdańsk', 1945)), data_on_universities)
    print('Printuje listę : {}'.format(llist_print(data_on_universities)))
    print('Czy lista jest pusta? : {}'.format(is_empty(data_on_universities)))
    print('Usuwam element z poczatku...')
    data_on_universities = remove(data_on_universities)
    print('Printuje listę : {}'.format(llist_print(data_on_universities)))
    print('Usuwam element z konca...')
    data_on_universities = remove_from_end(data_on_universities)
    print('Printuje listę : {}'.format(llist_print(data_on_universities)))
    print('Liczba elementow w liscie wynosi: {}'.format(length(data_on_universities)))
    print('Pierwszy element listy to: {}'.format(get(data_on_universities)))
    print('Odwracam liste...')
    data_on_universities = reverse(data_on_universities)
    print('Printuje listę : {}'.format(llist_print(data_on_universities)))
    print('Pierwszy element listy to: {}'.format(get(data_on_universities)))
    print('Trzy pierwsze elementy listy to: {}'.format(llist_print(take(data_on_universities, 3))))
    print('Dwa ostatnie elementy listy to: {}'.format(llist_print(drop(data_on_universities, 2))))
    print('Kasuje liste...')
    data_on_universities = destroy()
    print('Printuje listę po jej skasowaniu: {}'.format(llist_print(data_on_universities)))
    llist_print(data_on_universities)



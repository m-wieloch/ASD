#!/usr/bin/python
# -*- coding: utf-8 -*-
# Maciej Wieloch, 303080


class Element:
    def __init__(self, data, prior):
        self.data = data
        self.prior = prior

    def __str__(self):
        return 'Data = ' + str(self.data) + ', priority = ' + str(self.prior)

    # '>' operator
    def __gt__(self, other):
        this_elem = self.prior
        other_elem = other.prior

        if this_elem > other_elem:
            return True
        elif this_elem < other_elem:
            return False
        else:
            return False

    # '<' operator
    def __lt__(self, other):
        this_elem = self.prior
        other_elem = other.prior

        if this_elem > other_elem:
            return False
        elif this_elem < other_elem:
            return True
        else:
            return False


class Heap:
    def __init__(self):
        self.queue = []
        self.size = len(self.queue)

    def print_tab(self):
        result = []

        if not self.is_empty():
            for idx in range(len(self.queue)):
                result.append((self.queue[idx].data, self.queue[idx].prior))

        print(result)

    def print_heap(self):
        print("==========================================")
        values = self.queue[:]
        max_level = self.size // 2
        level = 0
        idx = 1
        while values:
            result = (int(2*max_level/idx)+10) * ' '
            for k in range(0, idx):
                popped = values.pop(0)
                result = result + str(popped.prior) + '(' + str(popped.data) + ')' + int(10/idx)*' '
                if not values:
                    break
            print(result)
            level = level + 1
            idx = level * 2
        print("==========================================")

    def is_empty(self):
        if len(self.queue) == 0:
            return True
        else:
            return False

    def peek(self):
        result = self.queue[0]

        for idx in range(len(self.queue)):
            if result < self.queue[idx]:
                result = self.queue[idx]

        return result

    def dequeue(self):
        if self.is_empty():
            return None
        else:
            result = self.queue[0]

            self.queue[0], self.queue[-1] = self.queue[-1], self.queue[0]
            self.queue.pop(-1)
            self.size = self.size - 1

            for idx in range(self.size):
                parent_index = (idx - 1) // 2

                if self.queue[parent_index] < self.queue[idx] and parent_index != - 1:
                    self.queue[parent_index], self.queue[idx] = self.queue[idx], self.queue[parent_index]

            return result

    def enqueue(self, element):
        if self.is_empty():
            self.queue.append(element)
            self.size = self.size + 1
        else:
            index = self.size
            parent_index = (index - 1) // 2
            parent = self.queue[parent_index]
            self.queue.append(element)
            self.size = self.size + 1

            while parent < element:
                self.queue[index], self.queue[parent_index] = parent, element

                index = parent_index
                parent_index = (index - 1) // 2
                if parent_index == -1:
                    break

                parent, element = self.queue[parent_index], self.queue[index]


if __name__ == '__main__':
    test = Heap()
    priors = [4, 7, 2, 5, 7, 6, 2, 1]
    dataset = ['A', 'L', 'G', 'O', 'R', 'Y', 'T', 'M']

    print('Do pustej kolejki:')
    for i in range(len(priors)):
        print('Wpisuje dana = {} o priorytecie = {}'.format(dataset[i], priors[i]))
        test.enqueue(Element(dataset[i], priors[i]))

    print('\nWypisuje kolejke w postaci kopca: ')
    test.print_heap()

    print('Korzystam z funkcji dequeue: {}'.format(test.dequeue()))
    print('Korzystam z funkcji peek: {}'.format(test.peek()))

    print('\nWypisuje kolejke w postaci tablicy: ')
    test.print_tab()

    print('\nOpróżnienie kolejki z wypisaniem usuwanych danych (użycie dequeue w pętli dopóki w kolejce będą dane)')
    for _ in range(test.size):
        print('Dequeue: {}'.format(test.dequeue()))

    print('\nWypisuje kolejke w postaci kopca: ')
    test.print_heap()

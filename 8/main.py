#!/usr/bin/python
# -*- coding: utf-8 -*-
# Maciej Wieloch, 303080

from math import log
import random
from timeit import default_timer as timer

#######################################################################################################################
# ================================================ PIERWSZY ALGORYTM ================================================ #
#######################################################################################################################


class ElementBST:
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
        new_element = ElementBST(key, data)
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


# Heap methods
def heap_swap(tab, length, index):
    left = 2 * index + 1
    right = 2 * index + 2
    largest = index

    if left < length and tab[index] < tab[left]:
        largest = left

    if right < length and tab[largest] < tab[right]:
        largest = right

    if largest is not index:
        tab[index], tab[largest] = tab[largest], tab[index]
        heap_swap(tab, length, largest)


def heapify(tab):
    result = tab[:]

    for index in range(len(result) // 2, -1, -1):
        heap_swap(result, len(result), index)

    return result


def heapsorting(tab):
    result = tab[:]

    for index in range(len(result) - 1, 0, -1):
        result[index], result[0] = result[0], result[index]
        heap_swap(result, index, 0)

    return result


def heap2d(tab, width=None):
    # Z powodu problematycznego doboru parametrow (moja funkcja strasznie sie zaczela rozjezdzac dla wiekszej ilosci elementow)
    # skorzystalem z gotowej funkcji do printowania kopca:
    # https://gist.github.com/ydm/4f0c948bc0d151631621
    print("==============")

    first = lambda h: 2 ** h - 1
    last = lambda h: first(h + 1)
    level = lambda heap, h: heap[first(h):last(h)]
    prepare = lambda e, field: str(e).center(field)

    if width is None:
        width = max(len(str(e)) for e in tab)

    height = int(log(len(tab), 2)) + 1
    gap = ' ' * width

    for h in range(height):
        below = 2 ** (height - h - 1)
        field = (2 * below - 1) * width
        print(gap.join(prepare(e, field) for e in level(tab, h)))

    print("==============")

#######################################################################################################################
# ================================================= DRUGI ALGORYTM  ================================================= #
#######################################################################################################################


class ElementS:
    def __init__(self, value, data):
        self.value = value
        self.data = data

    # '>' operator
    def __gt__(self, other):
        this_elem = self.value
        other_elem = other.value

        if this_elem > other_elem:
            return True
        elif this_elem < other_elem:
            return False
        else:
            return False

    # '<' operator
    def __lt__(self, other):
        this_elem = self.value
        other_elem = other.value

        if this_elem > other_elem:
            return False
        elif this_elem < other_elem:
            return True
        else:
            return False


class ElementSList:
    def __init__(self):
        self.tab = []

    def __str__(self):
        result = '['

        for index in range(len(self.tab)):
            result = result + '(' + str(self.tab[index].value) + ', ' + self.tab[index].data + ')'

            if index is not len(self.tab) - 1:
                result = result + ', '

        result = result + ']'
        return result

    def insert(self, element: ElementS):
        self.tab.append(element)

    def swapsort(self):
        for index in range(len(self.tab)):
            min_index = index

            for next_index in range(index + 1, len(self.tab)):
                if self.tab[next_index] < self.tab[min_index]:
                    min_index = next_index

            self.tab[index], self.tab[min_index] = self.tab[min_index], self.tab[index]

    def shiftsort(self):
        for index in range(len(self.tab)):
            min_index = index

            for next_index in range(index + 1, len(self.tab)):
                if self.tab[next_index] < self.tab[min_index]:
                    min_index = next_index

            element = self.tab.pop(min_index)
            self.tab.insert(0, element)
        self.tab.reverse()


if __name__ == '__main__':
    print('\n###########################################################################################################')
    print('# ========================================= PIERWSZY ALGORYTM =========================================== #')
    print('###########################################################################################################\n\n')

    priors = [3, 6, 1, 8, 4, 12, 7, 13, 9, 22, 15, 5, 11, 16, 18, 20, 25, 21, 27, 30]
    dataset = ['']

    print('Początkowa tablica = {}'.format(priors))

    # Drzewo 2D
    testBST = BST()
    for i in range(len(priors)):
        testBST.insert(priors[i], dataset)

    print('\nWyswietlam drzewo 2D: ')
    testBST.print_tree()

    print('\nTworze kopiec i wyświetlam kopiec 2D: ')
    test_heap = heapify(priors)
    heap2d(test_heap)

    print('\nSortuje kopiec i wyswietlam wynik koncowy: ')
    test_heap_sorted = heapsorting(test_heap)
    print(test_heap_sorted)

    print('\nPorownanie heapify i enqueue:')
    random_priors = []
    for i in range(0, 10000):
        random_priors.append(random.randint(0, 1000))

    # class Heap
    start = timer()
    test_class = Heap()
    for i in range(len(random_priors)):
        test_class.enqueue(random_priors[i])

    stop = timer()
    delta = stop - start

    print('Czas budowania kopca dla klasy (metoda enqueue) wynosi: {}'.format(delta))

    # method Heap
    start = timer()
    test_method = heapify(random_priors)
    stop = timer()
    delta = stop - start

    print('Czas budowania kopca dla metody heapify wynosi: {}'.format(delta))

    print('\n\n###########################################################################################################')
    print('# ========================================== DRUGI ALGORYTM  ============================================ #')
    print('###########################################################################################################\n\n')

    print('Sortowanie przez wybieranie')

    dataset2 = [(5, 'A'), (5, 'B'), (7, 'C'), (2, 'D'), (5, 'E'), (1, 'F'), (7, 'G'), (5, 'H'), (1, 'I'), (2, 'J')]

    test_swap = ElementSList()
    test_shift = ElementSList()
    for i in range(len(dataset2)):
        test_swap.insert(ElementS(dataset2[i][0], dataset2[i][1]))
        test_shift.insert(ElementS(dataset2[i][0], dataset2[i][1]))

    print('Tablica przed sortowaniem (swap):\n{}'.format(test_swap))
    start = timer()
    test_swap.swapsort()
    stop = timer()
    delta = stop - start
    print('\nTablica po sortowaniu (swap):\n{}'.format(test_swap))
    print('\nCzas sortowania (swap): {}'.format(delta))

    print('Tablica przed sortowaniem (shift):\n{}'.format(test_shift))
    start = timer()
    test_shift.shiftsort()
    stop = timer()
    delta = stop - start
    print('\nTablica po sortowaniu (shift):\n{}'.format(test_shift))
    print('\nCzas sortowania (shift): {}'.format(delta))

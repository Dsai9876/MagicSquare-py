#!/usr/bin/env python
"""
Python 3.x
magic_square.py

Displays a solution to a Magic Square of a given size
using regular or prime numbers using the brute force method

Usage:
magic_square.py <size> <prime_#s_only=y|n>
e.g.: magic_square.py 6 n
v0.1
    * Initial version
"""

import sys
import math
import itertools

__author__ = 'Kevin K. <kbknapp@gmail.com>'

__VERSION = '3.0'

def print_square(square, size):
    print(('+---'*size) + '+')
    for i in range(0, len(square)):
        if (i+1) % size == 0:
            if square[i] > 99:
                print('|{}|'.format(square[i]))
            elif square[i] > 9:
                print('| {}|'.format(square[i]))
            else:
                print('| {} |'.format(square[i]))
            print(('+---'*size) + '+')
        else:
            if square[i] > 99:
                print('|{}'.format(square[i]), end='')
            elif square[i] > 9:
                print('| {}'.format(square[i]), end='')
            else:
                print('| {} '.format(square[i]), end='')

def sum_indices(the_list, indices):
    sum = 0
    for index in indices:
        sum += the_list[index]
    return sum

def is_prime(n):
    for i in range(2, int(math.sqrt(n))):
        if n % i == 0:
            return False
    return True

def increment_indices(square, numbers):
    square_len = len(square)
    square_dup = [square[i] for i in range(0, square_len)]
    r_i = square_len - 1
    numbers_len = len(numbers)
    n_i = square_len

    while True:
        while n_i == square_len:
            n_i = numbers.index(square_dup[r_i]) + 1
            if n_i == square_len:
                square_dup[r_i] = 0
                r_i -= 1
                if r_i < 0:
                    return (square, True)

        while numbers[n_i] in square_dup:
            n_i += 1
            if n_i == square_len:
                square_dup[r_i] = 0
                r_i -= 1
                break
        else:
            square_dup[r_i] = numbers[n_i]
            if 0 in square_dup:
                r_i += 1
                n_i = 0
            else:
                break

    square = [square_dup[i] for i in range(0, square_len)]
    return (square, False)

def solve_square(size, prime_only):
    square_size = size * size

    if prime_only:
        start = 3
        numbers = [p for p in range(start, square_size**2, 2) if is_prime(p)]
        numbers = numbers[:(square_size)]
    else:
        start = 1
        numbers = [i for i in range(start, (square_size) + 1)]

    rows = [[j for j in range(i*size, size*(i+1))] for i in range(0, size)]
    cols = [[j for j in range(i, (square_size)+i, size)] for i in range(0, size)]
    diags = []
    diags.append([i for i in range(0, (size+1)*size, size + 1)])
    diags.append([i for i in range((size-1), square_size - 1, size - 1)])

    magic_num = int(sum(numbers)/size)

    # Initialize the square
    square = [numbers[i] for i in range(0, square_size)]

    # DEBUG
    print('Square Size: {}'.format(square_size))
    print('Numbers: {}'.format(numbers))
    print('Magic Number: {}'.format(magic_num))
    print('Rows: {}'.format(rows))
    print('Cols: {}'.format(cols))
    print('Diags: {}'.format(diags))
    print('Initial square:')
    print_square(square, size)
    # END DEBUG

    solved = False
    while not solved:
        i = len(rows) - 1
        while i > -1:
            while sum_indices(square, rows[i]) != magic_num:
                square, no_more_inc = increment_indices(square, numbers)
                if no_more_inc:
                    return (square, False)
                else:
                    i = len(rows) - 1
            else:
                i -= 1
        solved = True
        for col in cols:
            while sum_indices(square, col) != magic_num:
                square, no_more_inc = increment_indices(square, numbers)
                if no_more_inc:
                    return (square, False)
                else:
                    solved = False
                    break
        if solved:
            for diag in diags:
                while sum_indices(square, diag) != magic_num:
                    square, no_more_inc = increment_indices(square, numbers)
                    if no_more_inc:
                        return (square, False)
                    else:
                        solved = False
                        break

    return (square, True)

def main(args):
    if len(args) != 2:
        return 'Usage: magic_square.py <size> <prime_only:y|n>'

    size = int(args[0])
    prime_only = False
    if args[1].lower() == 'y':
        prime_only = True

    (answer, solved) = solve_square(size, prime_only)

    if solved:
        print('Solved:')
        print_square(answer, size)
    else:
        print('No solution exists!')
        print('Ending Square:')
        print_square(answer, size)

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
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

def print_square(square, size):
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

def increment_indices(square, indices, numbers, duplicates=None):
    to_inc = [square[i] for i in indices]
    r_i = len(to_inc) - 1
    numbers_len = len(numbers)
    to_inc_len = len(to_inc)
    duplicates_len = len(duplicates)

    while r_i > 0:
        if to_inc[r_i] == 0:
            n_i = 0
        else:
            n_i = numbers.index(to_inc[r_i]) + 1
        if n_i == numbers_len:
            to_inc[r_i] = 0
            r_i -= 1
            continue
        while numbers[n_i] in duplicates:
            n_i += 1
            if n_i == numbers_len:
                to_inc[r_i] = 0
                r_i -= 1
                break
        if n_i != numbers_len:
            to_inc[r_i] = numbers[n_i]
            duplicates[r_i*(int(duplicates_len/to_inc_len)-1)] = numbers[n_i]
            if 0 in to_inc and r_i < to_inc_len:
                r_i += 1
            else:
                break

    for i, si  in enumerate(indices):
        square[si] = to_inc[i]
    return True

def indices_permutations(square, indices):
    to_permute = [square[i] for i in indices]
    return [l for l in itertools.permutations(to_permute)]

def solve_square(size, prime_only):
    square_size = size * size

    if prime_only:
        start = 3
        numbers = [p for p in range(start, square_size, 2) if is_prime(p)]
    else:
        start = 1
        numbers = [i for i in range(start, (square_size) + 1)]

    rows = [[j for j in range(i*size, size*(i+1))] for i in range(0, size)]
    cols = [[j for j in range(i, (square_size)+i, size)] for i in range(0, size)]
    diags = []
    diags.append([i for i in range(0, (size+1)*size, size + 1)])
    diags.append([i for i in range(0, (size-1)*size, size - 1)])

    magic_num = int(sum(numbers)/size)

    perms_per_row = 1
    for i in range(size, 0, -1):
        perms_per_row *= i

    # Initialize the square with 0's
    square = [0 for _ in range(0, square_size)]

    # DEBUG
    print('Square Size: {}'.format(square_size))
    print('Numbers: {}'.format(numbers))
    print('Magic Number: {}'.format(magic_num))
    print('Initial square:')
    print_square(square, size)
    # END DEBUG

    solved = False
    while not solved:
        for i, row in enumerate(rows):
            # Initialize the first row
            if sum([square[i] for i in row]) == 0:
                for r in row:
                    for n in numbers:
                        if n not in square:
                            square[r] = n
                            break

            while sum_indices(square, row) != magic_num:
                # Row does not equal magic number
                # Increment the row in reverse (least significant digit) order

                dups = []
                for j in range(0, i+1):
                    for t in rows[j]:
                        dups.append(square[t])
                if not increment_indices(square, row, numbers, dups):
                    return (square, False)

        # Get row permutations
        row_perms = [indices_permutations(square, row) for row in rows]

        c = 0
        p = [0 for _ in range(0, size)]
        r = size - 1
        while c < size:
            while sum_indices(square, cols[c]) != magic_num:
                # Col does not equal magic number
                # Rotate permutations
                if c > 0:
                    c = 0
                while p[r] == perms_per_row:
                    if r >= 0:
                        r -= 1
                        if r < 0:
                            return (square, False)
                for i in range(0, size):
                    square[rows[r][i]] = row_perms[r][p[r]][i]
                p[r] += 1
                while r < size - 1:
                    r += 1
                    p[r] = 0
                    for i in range(0, size):
                        square[rows[r][i]] = row_perms[r][p[r]][i]
                    p[r] += 1
            c += 1

        for diag in diags:
            if sum_indices(square, diag) != magic_num:
                solved = False
                break
            solved = True

        if solved:
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

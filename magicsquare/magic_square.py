#!/usr/bin/env python
"""
Python 3.x
magic_square.py

Displays a 6x6 Magic Square of prime numbers who's magic number is 666

v0.1
    * Initial version
"""

import sys
import math

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

def solve_square(size, magic_num, numbers):
    square_size = size * size
    rows = [[j for j in range(i*size, size*(i+1))] for i in range(0, size)]
    cols = [[j for j in range(i, (square_size)+i, size)] for i in range(0, size)]
    diag = [i for i in range(0, (size+1)*size, size + 1)]

    print('Square Size: {}'.format(square_size))
    print('Numbers: {}'.format(numbers))

    square = [0 for _ in range(0, square_size)]

    # Initialize the first diagnal
    for i, d in enumerate(diag):
        square[d] = numbers[i]

    print('Initial square:')
    print_square(square, size)

    diagnal_tries = 0
    increment_diag = False
    divisor = 1
    for i in range(0, size):
        divisor *= len(numbers) - i
    while True:
        percent = int(diagnal_tries/divisor)
        print('{}'.format([square[i] for i in diag]))
        #sys.stdout.write('\r')
        #sys.stdout.write('[%-100s] %d%%' % ('='*percent, percent))
        #sys.stdout.flush()
        solved = False
        diagnal_tries += 1
        if sum_indices(square, diag) == magic_num and not increment_diag:
            # Diagnal matches, we have a maybe...
            # Set and check rows
            break_from_rows = False
            for i, row in enumerate(rows):
                check_cols = False
                if break_from_rows:
                    break
                # Initialize the row
                if 0 in [square[r] for r in row]:
                    j = 0
                    for n in numbers:
                        if rows[i][j] in diag:
                            j += 1
                            if j == len(row):
                                break
                        if n in square:
                            continue
                        square[rows[i][j]] = n
                        j += 1
                        if j == len(row):
                            break
                if sum_indices(square, row) == magic_num:
                    check_cols = True
                    continue
                else:
                    check_cols = False
                    # Increment row
                    keep_going = True
                    rr_i = len(row) - 1
                    while keep_going:
                        if rr_i < 0:
                            # Row can't be incremented anymore
                            break_from_rows = True
                            break
                        if square[row[rr_i]] == numbers[-1]:
                            for n in numbers:
                                if n in [square[r] for r in row]:
                                    continue
                                square[row[rr_i]] = n
                                break
                            rr_i -= 1
                        else:
                            n_index = numbers.index(square[row[rr_i]]) + 1
                            while numbers[n_index] in square and n_index <= len(numbers):
                                n_index += 1
                                if n_index == len(numbers):
                                    n_index = 0
                                    rr_i -= 1
                            while numbers[n_index] in [square[r] for r in row]:
                                n_index += 1
                                if n_index == len(numbers):
                                    for n in numbers:
                                        if n in [square[r] for r in row]:
                                            continue
                                        square[row[rr_i]] = n
                                        break
                                    rr_i -= 1
                                    break
                            else:
                                square[row[rr_i]] = numbers[n_index]
                                if sum_indices(square, row) == magic_num:
                                    keep_going = False
            if check_cols:
                print('All rows match:')
                print_square(square, size)
                for i, col in enumerate(cols):
                    if sum_indices(square, col) == magic_num:
                        if i == len(cols) - 1:
                            solved = True
                        continue
                    else:
                        break
                if solved:
                    return (square, True)
                else:
                    increment_diag = True
        else:
            increment_diag = False
            # Increment the diagnal in reverse order
            keep_going = True
            rd_i = len(diag) - 1
            while keep_going:
                if rd_i < 0:
                    return (square, False)
                if square[diag[rd_i]] == numbers[-1]:
                    square[diag[rd_i]] = 0
                    increment_diag = True
                    rd_i -= 1
                else:
                    if square[diag[rd_i]] != 0:
                        n_index = numbers.index(square[diag[rd_i]]) + 1
                    else:
                        n_index = 0
                    while numbers[n_index] in [square[d] for d in diag]:
                        n_index += 1
                        if n_index == len(numbers):
                            square[diag[rd_i]] = 0
                            rd_i -= 1
                            increment_diag = True
                            break
                    else:
                        square[diag[rd_i]] = numbers[n_index]
                        keep_going = False
            if keep_going:
                return (square, False)

def main(args):
    if len(args) != 3:
        return 'Usage: magic_square.py <size> <magic_number> <prime_only:y|n>'

    size = int(args[0])
    magic_num = int(args[1])

    if args[2].lower() == 'y':
        start = 3
        numbers = [p for p in range(start, size*size, 2) if is_prime(p)]
    else:
        start = 1
        numbers = [i for i in range(start, (size*size) + 1)]


    (answer, solved) = solve_square(size, magic_num, numbers)

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

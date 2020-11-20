# Query what level of sudoku, scrape from the web and solve
#
# Written by Jim Ogren
#
import Sudoku

levels = {"1" : "Easy", "2" : "MEDIUM", "3" : "HARD", "4" : "EVIL"}

def print_levels(levels):
    for level in levels:
        print(f'Level {level} = \"{levels[level]}\"')

# Query level, scrape a sudoku from the web and solve
flag = True
while(flag):
    print_levels(levels)
    level = input('Select level of sudoku or press q to quit: ')

    if level == 'q':
        flag = False
    elif level in levels:
        sudoku = Sudoku.fetchSudoku(level)
        Sudoku.run_solver(sudoku)
    else:
        print('Unknown level')

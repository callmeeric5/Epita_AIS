# Puzzels

## Flip the sign
![](https://cdn.jsdelivr.net/gh/callmeeric5/imageHost/img/Flip_the_sign.jpg)

### solution
```python
height, width = [int(i) for i in input().split()]
ch = []
for i in range(height):
    line = input().split()
    ch.append(line)
lst = []
for i in range(height):
    line = input().split()
    for j, c in enumerate(line):
        if c == 'X':
            lst.append(int(ch[i][j]))

good = True
for i in range(len(lst) - 1):
    if (lst[i] > 0) == (lst[i + 1] > 0):
        good = False
        break

# Write an answer using print
# To debug: print("Debug messages...", file=sys.stderr, flush=True)

print("true" if good else "false")
```
## Reverse minesweeper
![](https://cdn.jsdelivr.net/gh/callmeeric5/imageHost/img/Reverse_minesweeper.jpg)

```python
import sys
import math

w = int(input())
h = int(input())
board = ['.'*(w+2)]
for i in range(h):
    board.append('.' + input() + '.')
board.append('.'*(w+2))

output = [['.']*w for i in range(h)]

for i in range(h):
    for j in range(w):
        s = 0
        if(board[i+1][j+1] != 'x'):
            for k in range(3):
                for l in range(3):
                    if(board[i+k][j+l] == 'x'):
                        s += 1
        if(s > 0):
            output[i][j] = str(s)
# Write an answer using print
# To debug: print("Debug messages...", file=sys.stderr, flush=True)
for i in range(h):
    print(''.join(output[i]))
```

### Sudoku Validator
![](https://cdn.jsdelivr.net/gh/callmeeric5/imageHost/img/Sudoku_Validator.jpg)
```python
import sys
import math
def check_grid(grid):
    def is_valid_group(group):
        return sorted(group) == list(range(1, 10))
    
    for row in grid:
        if not is_valid_group(row):
            return False
    
    for col in range(9):
        column = [grid[row][col] for row in range(9)]
        if not is_valid_group(column):
            return False
    
    for x in range(0, 9, 3):
        for y in range(0, 9, 3):
            sub_grid = []
            for i in range(3):
                for j in range(3):
                    sub_grid.append(grid[x + i][y + j])
            if not is_valid_group(sub_grid):
                return False

    return True

grid = []
for i in range(9):
    grid.append(list(map(int, input().split())))

if check_grid(grid):
    print("true")
else:
    print("false")
```

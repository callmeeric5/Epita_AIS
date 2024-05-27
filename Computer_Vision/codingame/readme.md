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

# maze-transform

<img src='images/maze-icon.png' width=100 align='left' hspace='5' vspace='5'/>

Inspired by a particular Computerphile video. Generates mazes (2d
array of booleans) and solves them by converting into a compact
graph and running textbook algorithms. Usage:

```shell
$ ./maze-gen 100 50 file.png  # 100x50 maze
$ ./maze-solve file.png file-solved.png
```

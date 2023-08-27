#!/usr/bin/env python3

"""
usage:
    solve <src> <dst> [--method=<method>]
    solve (-h | --help)

options:
    -h --help          show this page.
    --method=<method>  choose a solving method, one of:
                         bf (breadth first, default),
                         df (depth first),
                         rm (random mouse)
"""

from libmaze.vendor.docopt import docopt
from libmaze.read import maze_from_file
from libmaze.solvers import random_mouse, breadth_first, depth_first
from libmaze.transform import transform
from libmaze.plot import plot_path, plot_heatmap
import json


def get_solver_plotter(string):
    default = {
        'bf': (breadth_first, plot_path),
        'df': (depth_first,   plot_path),
        'rm': (random_mouse,  plot_heatmap),
    }
    return default.get(string, default['bf'])


if __name__ == '__main__':
    args = docopt(__doc__)
    src  = args['<src>']
    dst  = args['<dst>'] + '.png'
    dstjson  = args['<dst>'] + '.json'
    maze = maze_from_file(src)
    with open(dstjson, 'w') as f:
    	json.dump(maze.array, f)
    solver, plotter = get_solver_plotter(args['--method'])
    path = solver(*transform(maze))
    plotter(
        maze,
        path,
        ).save(dst)

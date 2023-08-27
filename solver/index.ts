import * as fs from 'fs';
import { keccak_256 } from '@noble/hashes/sha3';

class Position {
    x: number;
    y: number;
    constructor(x: number, y: number) {
        this.x = x;
        this.y = y;
    }

    compare(pos: Position): boolean {
        return this.x === pos.x && this.y === pos.y;
    }
}

enum Square {
    Wall,
    None,
    Tried,
    Path,
}

function printMaze(grid: number[][]){
    let maze = "";
    for (let y = 0; y < grid.length; y++) {
        for (let x = 0; x < grid.length; x++) {
            maze += grid[y][x];
        }
        maze += "\n";
    }
    console.log(maze);
}

function solve(solution: number[][], pos: Position, end: Position): boolean {
    if (pos.x === end.x && pos.y === end.y) {
        solution[pos.y][pos.x] = Square.Path;
        return true;
    } else if (solution[pos.y][pos.x] === Square.Wall || solution[pos.y][pos.x] === Square.Tried) {
        return false;
    }
    solution[pos.y][pos.x] = Square.Tried;
    if (pos.x < solution.length - 1 && solve(solution, new Position(pos.x + 1, pos.y), end)) {
        solution[pos.y][pos.x] = Square.Path;
        return true;
    }
    if (pos.y < solution.length - 1 && solve(solution, new Position(pos.x, pos.y + 1), end)) {
        solution[pos.y][pos.x] = Square.Path;
        return true;
    }
    if (pos.x > 0 && solve(solution, new Position(pos.x - 1, pos.y), end)) {
        solution[pos.y][pos.x] = Square.Path;
        return true;
    }
    if (pos.y > 0 && solve(solution, new Position(pos.x, pos.y - 1), end)) {
        solution[pos.y][pos.x] = Square.Path;
        return true;
    }
    return false;
}

function buildPath(solution: number[][], start: Position, end: Position): Position[] {
    let path: Position[] = [];
    let pos = start;
    while (pos.x !== end.x || pos.y !== end.y) {
        path.push(pos);
        if (pos.x < solution.length - 1 && solution[pos.y][pos.x + 1] === Square.Path && path.find(p => p.compare(new Position(pos.x + 1, pos.y))) === undefined) {
            pos = new Position(pos.x + 1, pos.y);
        } else if (pos.y < solution.length - 1 && solution[pos.y + 1][pos.x] === Square.Path && path.find(p => p.compare(new Position(pos.x, pos.y + 1))) === undefined) {
            pos = new Position(pos.x, pos.y + 1);
        } else if (pos.x > 0 && solution[pos.y][pos.x - 1] === Square.Path && path.find(p => p.compare(new Position(pos.x - 1, pos.y))) === undefined) {
            pos = new Position(pos.x - 1, pos.y);
        } else if (pos.y > 0 && solution[pos.y - 1][pos.x] === Square.Path && path.find(p => p.compare(new Position(pos.x, pos.y - 1))) === undefined) {
            pos = new Position(pos.x, pos.y - 1);
        }
        // console.log(pos);
    }
    path.push(pos);
    return path;
}

function buildArray(path: Position[]) {
    let array: number[] = [];
    for (const pos of path) {
        array.push(pos.x);
        array.push(pos.y);
    }
    return array;
}

function hashPath(path: number[]) {
    let computedHash: Uint8Array | null = null;
    for (let i = 0; i < path.length; i+=32) {
      const chunk = path.slice(i, i + 32);
      if (computedHash == null) {
        computedHash = keccak_256(Uint8Array.from([1].concat(chunk)))
      } else {
        computedHash = keccak_256(Uint8Array.from([1].concat(Array.from(computedHash)).concat(chunk)))
      }
    }
    return computedHash;
  }

const file = process.argv[2];
// console.log(file);
const metadata = fs.readFileSync(`${file}.json`, 'utf8');
const maze: number[][] = JSON.parse(metadata);
// console.log(json);
// const maze = json[0];
// printMaze(maze);
const start = new Position(maze[0].indexOf(2), 0);
const end = new Position(maze[maze.length - 1].indexOf(3), maze.length - 1);
const size = maze.length;
let solution: number[][] = new Array(size).fill(Square.None).map(() => new Array(size).fill(Square.None));
for (let x = 0; x < size; x++) {
    for (let y = 0; y < size; y++) {
        if (maze[y][x] === 0) {
            solution[y][x] = Square.Wall;
        }
    }
}
solve(solution, start, end);
// printMaze(solution);
const path = buildPath(solution, start, end);
const array = buildArray(path);
const hash = hashPath(array);
let outfile = fs.createWriteStream(`${file}.soln.txt`);
hash?.forEach((byte) => outfile.write(byte.toString(16)));
#!/bin/bash

N=8

echo "Generating mazes..."
for j in {16..63}
do
	num=$(( $j * 23 ))
	for (( i=0; i<= $num; i++ ))
    do
        ((k=k%N)); ((k++==0)) && wait
        ./gen ${j} ${j} bread/maze_${j}_${i} &
    done
done

echo "Solving mazes..."
for j in {16..63}
do
	num=$(( $j * 23 ))
	for (( i=0; i<= $num; i++ ))
    do
        ((m=m%N)); ((m++==0)) && wait
        ts-node solver/index.ts bread/maze_${j}_${i} &
    done
done

echo "Generating metadata..."
./generate_metadata.py

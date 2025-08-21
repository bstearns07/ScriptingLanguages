#########################################################################################
# Title: Lab 2-1
# Author: Ben Stearns
# Date: 8-19-24
# Description: Application simulation various types of "random walks"
########################################################################################

# random_walk_1d.py
import matplotlib.pyplot as plt
from random import choice #imports only what is needed from the module
from typing import List, Tuple, Optional
from random import seed
import statistics as stats

def step_1d() -> int:
    """Return a single step: -1 (left) or +1 (right)."""
    return choice([-1, 1])


def walk_1d(n_steps: int) -> List[int]:
    """
    Simulate a 1-D random walk for n_steps.
    Returns the list of positions after each step (length == n_steps).
    Start at position 0 (not included in the list).
    """
    pos = 0
    path: List[int] = []
    for _ in range(n_steps):
        pos += step_1d()
        path.append(pos)
    return path


def stats_1d(path: List[int]) -> Tuple[int, int, int, int]:
    """
    Return (final_pos, min_pos, max_pos, returns_to_origin).
    A 'return to origin' counts each time the path position equals 0.
    """
    final_pos = path[-1] if path else 0
    min_pos = min(path) if path else 0
    max_pos = max(path) if path else 0
    returns = sum(1 for p in path if p == 0)
    return final_pos, min_pos, max_pos, returns

# defines a function that calculates the average final position across many walk trials
def average_max_min_final_distance(n_steps: int, trials: int, rng_seed: Optional[int] = 42) -> Tuple[float, int, int]: #rng_seed can be an integer or None using a type hint

    #if rng_seed has no value, no seeding happens. That way you can choose to have the same random numbers generated or not
    if rng_seed is not None:
        seed(rng_seed)  # reproducibility

    distances = [] # for storing final positions of each walk

    #for each trial the user chooses to run, store a walk and append it's final distance from origin to the array
    for _ in range(trials):
        path = walk_1d(n_steps)
        distances.append(abs(path[-1])) # only appends the absolute value of the final position (converts negative numbers to positive)

    #return the mean/average of all the final positions stored
    return stats.mean(distances), max(distances), min(distances)

# random_walk_2d.py
from random import choice, seed
from typing import List, Tuple

Step2D = Tuple[int, int]  # (dx, dy)

DIRECTIONS: List[Step2D] = [(1,0), (-1,0), (0,1), (0,-1)]  # E, W, N, S

def step_2d() -> Step2D:
    return choice(DIRECTIONS)

def walk_2d(n_steps: int, rng_seed: Optional[int] = 42) -> List[Tuple[int, int]]:
    if rng_seed is not None:
        seed(rng_seed)
    x, y = 0, 0
    path: List[Tuple[int, int]] = []
    for _ in range(n_steps):
        dx, dy = step_2d()
        x, y = x + dx, y + dy
        path.append((x, y))
    return path

#function for calculating the Euclidean distance for a set of coordinates (distance from origin (0,0))
def euclidean_distance(x: int, y: int) -> float:
    return (x*x + y*y) ** 0.5

#define a function to simulate a collection of x,y coordinates to simulate a 2d walk
def ascii_board(path: List[Tuple[int,int]], radius: int = 10) -> str:
    """
    Return a string for a simple ASCII grid.
    'S' = start, 'E' = end, '*' = visited.
    """
    visited = set(path)#stored all coordinates as a "set" collection, which can be more easily checked for a particular coordinates
    end = path[-1] if path else (0,0)# stores the last coordinates in the path as the ending position
    rows: List[str] = []#for storing each row's string

    #define a for loop to represent a row going up and down from radius to -radius
    for yy in range(radius, -radius-1, -1):
        row = [] #represents an array of characters representing the current row

        #define a loop from -radius to +radius to represent a grid going left to right
        for xx in range(-radius, radius+1):

            #determine the character the current row position
            if (xx, yy) == (0,0):
                ch = 'S'
            elif (xx, yy) == end:
                ch = 'E'
            elif (xx, yy) in visited:
                ch = '*'
            else:
                ch = '.'
            row.append(ch)#append the character to the rows string
        rows.append("".join(row))#append the row to the list of rows
    return "\n".join(rows)# returns all rows as a string with new lines between each row to represent the final grid

#identifies a could block only executed if this file is ran directly vs. through an import
if __name__ == "__main__":

    #run a single test walk run of N number of steps, store the stats, then print stats
    N = 1000  # try 10, 100, 1000
    path = walk_1d(N)
    final_pos, min_pos, max_pos, returns = stats_1d(path)

    print(f"1-D walk for {N} steps")
    print(f"Final position: {final_pos}")
    print(f"Min/Max visited: {min_pos}/{max_pos}")
    print(f"Returns to origin: {returns}")
    print("")

    #run a test trial of 1000 walks, each 100 steps long, and print the average final position of each walk
    finalPositionAverage, finalPositionMax, finalPositionMin = average_max_min_final_distance(100, 1000)
    print(f"Avg |final position| over 1000 trials of 100 steps: {finalPositionAverage:.2f}")
    print(f"Max |final position| over 1000 trials of 100 steps: {finalPositionMax}")
    print(f"Min |final position| over 1000 trials of 100 steps: {finalPositionMin}")
    print("")

    #run a 2d test run
    M = 100
    path = walk_2d(N, rng_seed=7)
    endx, endy = path[-1]
    print(f"2-D walk for {N} steps; end at ({endx}, {endy}), distance {euclidean_distance(endx, endy):.2f}\n")
    print(ascii_board(path, radius=10))

    def plot_path(path):
        xs = [0] + [p[0] for p in path]
        ys = [0] + [p[1] for p in path]
        plt.figure()
        plt.plot(xs, ys, marker='o', markersize=2, linewidth=1)
        plt.scatter([0], [0], s=50, label="start")
        plt.scatter([xs[-1]], [ys[-1]], s=50, label="end")
        plt.title(f"2-D Random Walk ({len(path)} steps)")
        plt.legend()
        plt.axis('equal')
        plt.show()




from typing import List, Tuple

# parses line of text from the input where '->' splits tuples of integers that are divided by ','
# e.g. 498,4 -> 498,6 -> 496,6 = [(498, 4), (498, 6), (496, 6)]


def parse_line_into_rock_paths(line: str) -> Tuple[List[Tuple[int, int]], int, int]:
    splits = line.split("->")
    splits = [x.strip() for x in splits]
    splits = [(x.split(",")) for x in splits]
    res = []

    width = 0
    floor = 0

    for split in splits:
        x = int(split[0])
        y = int(split[1])

        if x > width:
            width = x

        if y > floor:
            floor = y

        res.append((x, y))
    return (res, floor, width)


# defines a grid of chars from width and height
def create_grid(width: int, height: int) -> List[List[str]]:
    return [["." for i in range(width)] for j in range(height)]

# places rock paths on the grid where the path is filled by rocks from one coordinate tuple to another


def place_rocks_on_grid(grid: List[List[str]], rocks: List[Tuple[int, int]]):
    for i in range(len(rocks) - 1):
        x1, y1 = rocks[i]
        x2, y2 = rocks[i + 1]

        if x1 == x2:
            # vertical path
            for y in range(min(y1, y2), max(y1, y2) + 1):
                grid[y][x1] = "x"

        elif y1 == y2:
            # horizontal path
            for x in range(min(x1, x2), max(x1, x2) + 1):
                grid[y1][x] = "x"

# prints the grid to the console


def print_grid(grid: List[List[str]]):
    print("-------------")
    for row in grid:
        print("".join(row)+"\n")
    print("-------------")


# prints grid to file
def print_grid_to_file(grid: List[List[str]], file_name: str):
    with open(file_name, "w") as file:
        for row in grid:
            file.write("".join(row)+"\n")


# makes a new grid that contains only columns and rows that contain rocks


def clean_grid(grid: List[List[str]]):
    # find the min and max x and y values that contain rocks
    min_x = len(grid[0])
    max_x = 0
    min_y = len(grid)
    max_y = 0

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == "x":
                min_x = min(min_x, x)
                max_x = max(max_x, x)
                min_y = min(min_y, y)
                max_y = max(max_y, y)

    # create a new grid with the correct size
    # +2 to account for the border
    new_grid = create_grid(max_x - min_x + 3, len(grid))

    # copy the rocks from the old grid to the new grid
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == "x":
                # +1 to account for the border
                new_grid[y][x - min_x + 1] = "x"

    # replace the old grid with the new grid
    grid.clear()
    grid.extend(new_grid)

# puts sand on the grid. Sand is displayed as an 'o'. Sand starts at coordinate (500, 0) and falls down until it hits a rock


def place_sand_on_grid(grid: List[List[str]]):
    x, y = [500, 0]

    curr_coord = [x, y]

    while True:
        if curr_coord[1]+1 >= len(grid) or grid[curr_coord[1]][curr_coord[0]] == "o":
            return None

        grid_width = len(grid[0])-1
        grid_height = len(grid)-1	

        next_coords = [
            [curr_coord[0], min(curr_coord[1]+1, grid_height)],
            [min(curr_coord[0]-1, grid_width), min(curr_coord[1]+1, grid_height)],
            [min(curr_coord[0]+1, grid_width), min(curr_coord[1]+1, grid_height)],
        ]

        def hits_bottom(n_coord):
            n_coord_val = grid[n_coord[1]][n_coord[0]]
            if n_coord_val == "x" or n_coord_val == "o":
                return True

            return False

        hit_results = [[hits_bottom(x), x] for x in next_coords]

        if len([x[0] for x in hit_results if x[0] == True]) == 3:
            grid[curr_coord[1]][curr_coord[0]] = "o"
            return True

        curr_coord = [x for x in hit_results if x[0] == False][0][1]

# pours sand into the grid until the place sand method returns None


def pour_sand(grid: List[List[str]]):
    steps = 0
    while True:
        # input("Press Enter to continue...")
        res = place_sand_on_grid(grid)
        # print_grid(grid)
        print_grid_to_file(grid, "output.txt")
        if res == None:
            return steps
        steps += 1


def run(input_file_name: str, place_floor: bool):

    rock_lines = []

    total_floor = 0
    total_width = 0

    # reads the input file and parses each line
    with open(input_file_name) as lines:
        for line in lines:
            (rocks, floor, width) = parse_line_into_rock_paths(line)

            rock_lines.append(rocks)

            if (total_floor < floor):
                total_floor = floor

            if (total_width < width):
                total_width = width

        total_floor = total_floor + 3
        total_width = total_width * 2  + 2

        grid = create_grid(total_width, total_floor)

        if place_floor:
            place_rocks_on_grid(grid, [(0, total_floor-1), (total_width-1, total_floor-1)])

        for rocks in rock_lines:
            place_rocks_on_grid(grid, rocks)

    # clean_grid(grid)
    steps = pour_sand(grid)
    # print_grid(grid)
    print(f"steps: {steps}")

    return steps


run("input.txt", True)

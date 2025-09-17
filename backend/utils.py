from time import time
from math import sqrt


def get_filename(file_name: str):
    """
    This function extracts the name of the file, excluding the extension, from file_name.
    @param file_name: A string containing the name of the file
    @return:
    """
    return file_name.split(".")[0]


def get_file_content(file_path: str):
    """
    This function grabs the content of the file that is on the input path.
    @param file_path: The absolute or relative path to a file
    @return: The content of the file
    """
    with open(file_path, "r") as f:
        file = f.read()
    return file


def get_extension(file_name: str) -> str:
    """
    This function extracts the extension from a file name.
    @param file_name: A string containing the name of the file
    @return : The extension of the file name
    """
    return file_name.split(".")[-1]


def convert_coordinates_to_int(coordinates_in_string: str) -> complex:
    """
    This function converts coordinates in string to coordinates in complex form
    @param coordinates_in_string: This should be in the form x y
    @return: coordinates in complex form
    """
    points = list(map(float, (coordinates_in_string.split())))
    if len(points) == 2:
        coordinates = complex(points[0], points[1])
    else:
        raise SyntaxError("There should only be two coordinates")
    return coordinates


def pop_char(string: str, pos) -> str:
    """
    This function removes a certain character from a string given its index.
    @param string: An input string
    @param pos: The index of the character to be removed.
    @return: A string without the character at the index of pos.
    """
    li = list(string)
    li.pop(pos)
    return "".join(li)


def lerp(p0: complex, p1: complex, t: float) -> complex:
    """
    Linear interpolation function.
    :param p0: First point
    :param p1: Second point
    :param t: Parameter, ranging from 0-1
    :return: Point calculated using the two points and the value of the parameter t.
    """
    return (1 - t) * p0 + t * p1


def quadratic(a: float | int, b: float | int, c: float | int):
    """
    This function solves a quadratic equation.
    @param a: The coefficient of x squared
    @param b: The coefficient of x
    @param c: The constant
    @return: solutions
    """
    try:
        sol1 = ((-b + sqrt(b ** 2 - 4 * a * c)) / (2 * a))
    except (ValueError, ZeroDivisionError) as e:
        sol1 = None
    try:
        sol2 = ((-b - sqrt(b ** 2 - 4 * a * c)) / (2 * a))
    except (ValueError, ZeroDivisionError) as e:
        sol2 = None
    return sol1, sol2


def two_d_dist(p1: complex, p2: complex) -> float:
    """
    This function calculates the straight-line distance between the p1 and p2
    @param p1: First point
    @param p2: Second point
    @return: the straight-line distance between the p1 and p2 as a float.
    """
    return sqrt((p1.real - p2.real) ** 2 + (p1.imag - p2.imag) ** 2)


def arange(start: int, end: int, step: float | int = 1):
    """
    This function generates a list that starts with start, increments by step, ends with end.
    @param start:
    @param end:
    @param step:
    @return:
    """
    if start > end:
        raise IndexError
    li = []
    num = int((end - start) / step)
    # How many numbers are in the list
    element = start
    for x in range(num):
        li.append(element)
        element += step
    return li


def get_output_name():
    """

    @return:
    """
    return str(int(time())) + ".mp4"

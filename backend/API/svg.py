from utils import *
from bezier import CubicBezier, LinearBezier
import re


class SVG:

    def __init__(self, file_content: str):
        self.content = file_content
        self.funcs = []
        self.size = self.get_size()
        self.path = self.get_path()

    def get_size(self) -> tuple:
        """
        This function gets the size of the SVG image
        @return: A tuple of width and heigt
        """
        svg = re.findall("<svg.*>", self.content, flags=re.DOTALL)[0]
        width = float(re.findall(r"width=\".*?pt", svg)[0][7:-2])
        height = float(re.findall(r"height=\".*?pt", svg)[0][8:-2])
        return width, height

    def get_path(self) -> list:
        """
        This function extracts all coordinates in the SVG path element using regular expression
        @return: A list of all coordinates in the SVG path element
        """
        path = re.findall("<path.*/>", self.content, flags=re.DOTALL)[0]
        # Get a string inside the path element. The flag re.DOTALL is specified for the dot to cover the new line
        # character as well
        # <path matches the characters <path literally (case sensitive)
        # . matches any character (except for line terminators)
        # /> matches the characters /> literally (case sensitive)
        with_space = re.sub(r"\n", " ", path)
        # Replace each new line character with a space character in the path
        definition = re.findall(r"\".*\"", with_space)[0][1:-1]
        # Get the definition which is inside the <path> element, removing the
        in_coordinates = re.findall(r"[a-zA-Z]?-?\d+\.?\d*\s-?\d+\.?\d*z?", definition)
        # Get a list of coordinates
        return in_coordinates

    def parse_path(self) -> list:
        """
        This function parses the SVG image and convert the Bezier curves in the SVG path element to Python objects
        @return: A list of Bezier curve objects
        """
        self.current_point = complex(0, 0)
        # Variable to store the current point.
        # In SVG path element, a current point is always stored when rendering the curves.
        # For Cubic Bezier curves, control points cannot be currrent_point as they are not considered to be on the path.
        self.initial_point = complex(0, 0)
        self.relative_coordinates = False
        # Variable to store if the previous curve definition is relative or absolute
        self.l_or_c = False
        # Variable to store if the curve being defined is linear or cubic
        # if it's True, it's linear and if it's False, it's cubic
        self.points_list = []
        # A list to store the coordinates of points that define Bezier curves
        self.funcs_temp = []
        # A list to temporarily store Bezier curve objects
        for point in self.path:
            self._process_point(point)
        if len(self.funcs_temp) > 0:
            self.funcs.append(self.funcs_temp)
        return self.funcs

    def _process_point(self, point: str):
        """
        This function processes the input point.
        @param point: point a string
        """
        has_letter = re.search("[a-zA-z]", point)
        # If the string has a letter, that means it's a starting point.
        if has_letter:
            letter = point[has_letter.start():has_letter.end()]
            # has_letter.start() gives the starting index of the letter
            # has_letter.end() gives the final index of the letter
            self.point_in_int = convert_coordinates_to_int(pop_char(point, has_letter.start()))
            # the coordinates as a string are converted to a complex number
            if letter.upper() != "Z":
                # Z means it's the end of the path element
                # It does not matter if Z is uppercase or lowercase.
                # To keep the information about the previous curve definition, self.relative_coordinates is unchanged for Z.
                self.relative_coordinates = letter.islower()
                # If the letter is lowercase, it's relative
                # If the letter is uppercase, it's absolute
            match letter:
                case "M" | "m":
                    self._process_m()
                case "C" | "c":
                    self._process_c()
                case "L" | "l":
                    self._process_l()
                case "z" | "Z":
                    self._process_z()
                case _:
                    raise SyntaxError("invalid SVG syntax")
        else:
            # the input point does not have a letter; it calls the process_coordinates function
            self.point_in_int = convert_coordinates_to_int(point)
            self._process_coordinates()

    def _process_coordinates(self):
        """
        This function processes coordinates without a letter
        It means it's coordinates of control points
        """
        if self.l_or_c:
            self._process_coordinates_linear()
        else:
            self._process_coordinates_cubic()

    def _process_coordinates_linear(self):
        """
        This function processes coordinates for a linear Bezier curve
        A linear Bezier curve is defined only by two points, and this function is only called when the point has no leter.
        Therefore, it's guranteed to be the last point of the curve definition
        """
        new_point = self.relative_coordinates * self.current_point + self.point_in_int
        # If it's relative coordinates, the current point is added to the point to get the destination point
        bez = self._create_bezier([self.current_point, new_point])
        # This creates a Linear Bezier curve object
        self.funcs_temp.append(bez)
        self.current_point = new_point
        # Update the current point


    def _process_coordinates_cubic(self):
        """
        This function processes coordinates for a cubic Bezier curve
        In this case, Bezier curve object is created only if there are four points.
        @return:
        """
        new_point = self.relative_coordinates * self.current_point + self.point_in_int
        # If they are relative coordinates, the current point is added to the point to get the destination point
        self.points_list.append(new_point)
        if len(self.points_list) == 4:
            self.current_point = new_point
            self.funcs_temp.append(self._create_bezier(self.points_list))
            self.points_list = [self.current_point]
            # points_list is updated, as cubi Bezier curve can be defined straight after without calling the command c/C.
            # In that case, the last point is recognized as the start point for the next cubic Bezier.

    def _process_m(self):
        """
        This function processes coordinates for the start of definition of an edge in path element
        """
        self.current_point = self.relative_coordinates * self.current_point + self.point_in_int
        # If they are relative coordinates, the current point is added to the point to get the destination point
        if len(self.funcs_temp) > 0:
            self.funcs.append(self.funcs_temp)
            self.funcs_temp = []
        # If there are already Bezier curves in self.funcs, rearrange it so that the pen tip doesn't have to "jump"
        # This implies that there are multiple edges in the SVG path definition
        self.initial_point = self.current_point

    def _process_c(self):
        """
        This function processes coordinates for the start of definition of a cubic Bezier curve
        """
        self.l_or_c = False
        new_point = self.relative_coordinates * self.current_point + self.point_in_int
        # If they are relative coordinates, the current point is added to the point to get the destination point
        self.points_list = [self.current_point, new_point]
        # The start point for a Cubic Bezier curve is the current point.
        # Current point is only updated at the end of definition

    def _process_l(self):
        """
        This function processes coordinates for the start of definition of a linear Bezier curve
        """
        self.l_or_c = True
        new_point = self.relative_coordinates * self.current_point + self.point_in_int
        # If they are relative coordinates, the current point is added to the point to get the destination point
        self.funcs_temp.append(self._create_bezier([self.current_point, new_point]))
        # The start point for a Linear Bezier curve is the current point, and end point is the new point
        self.current_point = new_point

    def _process_z(self):
        """
        This function processes coordinates for the end of path definition
        """
        self._process_coordinates()
        if self.current_point != self.initial_point:
            # If the path is not enclosed, a Linear Bezier curve (a straight line) is added between the initial point
            # and the last point
            self.funcs_temp.append(self._create_bezier([self.current_point, self.initial_point]))
        self.current_point = self.initial_point
        self.funcs.append(self.funcs_temp)
        self.funcs_temp = []
        # self.funcs_temp is made empty as there might be another path definition

    def _create_bezier(self, points: list):
        """
        This function creates a Bezier curve object using CubicBezier and LinearBezier class
        @param points: A list of coordinates of points for curve definition
        @return:
        """
        if len(points) == 4:
            return CubicBezier(points)
        elif len(points) == 2:
            return LinearBezier(points)
        else:
            raise ValueError("Only Linear and Cubic bezier is supported")


if __name__ == "__main__":
    with open("/Users/kohkihatori/NEA/backend/pictures/apple.svg", "r") as f:
        file = f.read()
    tes = SVG(file)
    funcs = tes.parse_path()

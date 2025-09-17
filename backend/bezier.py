from utils import *
from config import Config


class Bezier:

    degrees = {
        1: "Linear",
        2: "Quadratic",
        3: "Cubic",
        4: "Quartic",
    }

    def __init__(self, points):
        self.degree = None
        self.points = points

    def p(self, index: int):
        """
        This function returns coordinates of the point at the index in the self.points list
        @param index: index specifying the point
        @return: THe coordinates of the point as a complex number
        """
        return self.points[index]

    def __repr__(self) -> str:
        """
        This function creates a string representation of the Bezier curve, showing its degree and points
        @return: A string representation of the Bezier curve
        """
        out = f"{self.degrees[self.degree]} Bezier Curve: "
        for index, point in enumerate(self.points):
            out += f"Point{index + 1}: ({point.real}, {point.imag}) "
        return out


class LinearBezier(Bezier):

    def __init__(self, points):
        super().__init__(points)
        self.degree = 1
        self.dist = self.get_dist()

    def func(self, t: float):
        """
        This function returns the value of the Bezier curve for some value of t
        @param t: parametric variable
        @return: value of the Bezier curve
        """
        return lerp(self.p(0), self.p(1), t)

    def get_lims(self):
        """
        This function gets the minimum and maximum values of real and imaginary coordinates
        @return: A tuple consisting of xlim and ylim, which are tuples consisting of minimum and maximum x and y values
        """
        possible_maxima_minima = [self.p(0), self.p(1)]
        # The possible maxima and minima is the start point and end point, as there are only two points
        xs = [p.real for p in possible_maxima_minima]
        ys = [p.imag for p in possible_maxima_minima]
        xlim = (min(xs), max(xs))
        ylim = (min(ys), max(ys))
        return xlim, ylim

    def get_dist(self) -> float:
        """
        This function computes the distance between the start and end point
        @return: The distance betweeen the start and end point
        """
        return two_d_dist(self.p(0), self.p(1))


class CubicBezier(Bezier):

    def __init__(self, points):
        super().__init__(points)
        self.degree = 3
        self.dist = self.get_dist()

    def func(self, t: float) -> complex:
        """
        This function returns the value of the Bezier curve for some value of t
        @param t: parametric variable
        @return: value of the Bezier curve
        """
        return (1 - t) ** 3 * self.p(0) + 3 * (1 - t) ** 2 * t * self.p(1) + 3 * (1 - t) * t ** 2 * self.p(2) + t ** 3 * self.p(3)

    def get_lims(self):
        """
        This function gets the minimum and maximum values of real and imaginary coordinates
        @return: A tuple consisting of xlim and ylim, which are tuples consisting of minimum and maximum x and y values
        """
        possible_maxima_minima = [self.p(0), self.p(1), *self._get_solutions_to_derivatives()]
        # In this case, the possible maxima and minima are solutions to derivatives of real and imaginary components
        # of the Bezier curve that reside between 0 and 1
        xs = [p.real for p in possible_maxima_minima]
        ys = [p.imag for p in possible_maxima_minima]
        xlim = (min(xs), max(xs))
        ylim = (min(ys), max(ys))
        return xlim, ylim

    def get_dist(self) -> float:
        """
        This function computes the distance of the Bezier curve between the start and end point. It's done by
        approximating it by stepping through values of t from 0 to 1 by a step specified in the config file,
        and calculating the straight line distance between each t value and summing all values together.
        @return: The distance of the Bezier curve
        between the start and end point
        """
        t_steps = arange(0, 1 + Config.DT, Config.DT)
        points = []
        dist = 0
        for t in t_steps:
            points.append(self.func(t))
            if len(points) == 2:
                dist += two_d_dist(points[0], points[1])
                points.pop(0)
        return dist

    def _get_solutions_to_derivatives(self) -> list:
        """
        This function computes solutions to derivatives of each real and imaginary components of the Bezier curve
        that are between 0 and 1. It must be 0 and 1 as all Bezier curves are defined between the t value of 0 and 1.
        @return: A list of solutions
        """
        a = -3*self.p(0) + 9*self.p(1) - 9*self.p(2) + 3*self.p(3)
        b = 6*self.p(0) + -12*self.p(1) + 6*self.p(2)
        c = -3*self.p(0) + 3*self.p(1)
        """
        These are derived by simply expanding the brackets of Bezier curve  equation
        """
        tx1, tx2 = quadratic(a.real, b.real, c.real)
        ty1, ty2 = quadratic(a.imag, b.imag, c.imag)
        ts = [tx1, tx2, ty1, ty2]
        solutions = []
        for t in ts:
            if t is not None and 0 <= t <= 1:
                solutions.append(self.func(t))
        return solutions


class PolyBezier:

    def __init__(self, beziers: list):
        self.beziers = beziers
        # This is a list of Bezier curves that define the PolyBezier
        self.num = len(self.beziers)
        self.dist = self.get_dist()

    def get_lims(self):
        """
        This function gets the minimum and maximum values of real and imaginary coordinates
        @return: A tuple consisting of xlim and ylim, which are tuples consisting of minimum and maximum x and y values
        """
        lims = [bez.get_lims() for bez in self.beziers]
        xs = [lim[0] for lim in lims]
        ys = [lim[1] for lim in lims]
        xlim = (min(xs, key=lambda item: item[0])[0], max(xs, key=lambda item: item[1])[1])
        ylim = (min(ys, key=lambda item: item[0])[0], max(ys, key=lambda item: item[1])[1])
        return xlim, ylim

    def get_dist(self):
        """
        This function computes the distance of the PolyBezier curve between the start and end point.
        It simply adds up the distance of each Bezier curve
        @return: The distance of the Bezier curve
        between the start and end point
        """
        return sum([bez.dist for bez in self.beziers])

    def __repr__(self) -> str:
        """
        This function returns a string representation of the PolyBezier curve
        @return:A string representation of the PolyBezier curve
        """
        return f"PolyBezier object consisting of {self.num} bezier curves"

    def __len__(self) -> int:
        """
        This function returns the number of Bezier curves in the PolyBezier as the length of the object
        @return: The number of Bezier curves
        """
        return self.num

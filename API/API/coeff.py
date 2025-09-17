from math import e, pi



class Coefficient_calculator:

    """
    Calculates coefficients for rotating vectors whose sum draws the shape of input polybezier
    """

    def __init__(self, poly_bezier, num: int, by_dist: bool = False):
        self.poly_bezier = poly_bezier
        # PolyBezier object
        self.num_coeff = num
        # Number of vectors
        self.num_bez = len(self.poly_bezier)
        self.by_dist = by_dist
        # If this is true, each Bezier curve in the PolyBezier gets the range of t that is proportional to its distance.
        # If this is false, each Bezier curve gets the equal range of t.

    def get_coefficient(self, n: int):
        """
        This function computes the nth coefficient for the given PolyBezier curve.
        @param n: The frequency
        @return: The nth coefficient for self.poly_bezier
        """
        integrals = []
        self.denom = -n * 2 * pi * 1j
        # The denominator of the function to be integrated
        lower = 0
        upper = 0
        # The initial values of lower and upper limit.
        for index, bezier in enumerate(self.poly_bezier.beziers):
            if self.by_dist:
                upper += bezier.dist/self.poly_bezier.dist
                # It splits the curves equally by distance
                # The upper limit of the integral
            else:
                upper = (index+1)/self.num_bez
                # It splits the curves equally with the same range of t for all curves
            # The upper limit of the integral
            self.upper_e = e ** (self.denom * upper)
            # The value of the part that contains e for the upper limit
            self.lower_e = e ** (self.denom * lower)
            # The value of the part that contains e for the lower limit
            result = self._get_integral(bezier, n)
            integrals.append(result)
            lower = upper
            # The upper limit of current integral is the lower limit of next integral
        return sum(integrals)

    def _get_integral(self, bezier, n):
        """
        This function gets the integral of the input Bezier curve and for the input value of n.
        @param bezier: A Bezier curve object
        @param n: The frequency
        @return: The result of integral
        """
        if bezier.degree == 3:
            return self._get_integral_cubic(bezier, n)
        elif bezier.degree == 1:
            return self._get_integral_linear(bezier, n)
        else:
            raise SyntaxError("Only cubic and linear bezier curves are supported.")

    def _get_integral_linear(self, bezier, n: int) -> complex:
        """
        This function gets the integral of the input Linear Bezier curve and for the input value of n.
        @param bezier: A LinearBezier curve object
        @param n: The frequency
        @return: The result of integral
        """
        zero = bezier.p(0)
        one = bezier.p(1)
        if self.by_dist:
            dubydt = self.poly_bezier.dist/bezier.dist
        else:
            dubydt = self.num_bez
        if n == 0:
            result = ((zero + (one - zero) / 2) / dubydt)
        else:
            result = ((one * self.upper_e - zero * self.lower_e) / self.denom) - (dubydt * (one - zero) * (
                    self.upper_e - self.lower_e) / (self.denom ** 2))
        return result

    def _get_integral_cubic(self, bezier, n: int) -> complex:
        """
        This function gets the integral of the input Cubic Bezier curve and for the input value of n.
        @param bezier: A CubicBezier curve object
        @param n: The frequency
        @return: The result of integral
        """
        a = -bezier.p(0) + 3 * bezier.p(1) - 3 * bezier.p(2) + bezier.p(3)
        # coefficient of t cubed
        b = 3 * bezier.p(0) - 6 * bezier.p(1) + 3 * bezier.p(2)
        # coefficient of t squared
        c = -3 * bezier.p(0) + 3 * bezier.p(1)
        # coefficient of t
        d = bezier.p(0)
        # constant
        if self.by_dist:
            dubydt = self.poly_bezier.dist/bezier.dist
        else:
            dubydt = self.num_bez
        if n == 0:
            result = (a / 4 + b / 3 + c / 2 + d) / dubydt
        else:
            first = ((a + b + c + d) * self.upper_e - d * self.lower_e) / self.denom
            second = -(dubydt * ((3 * a + 2 * b + c) * self.upper_e - c * self.lower_e) / (self.denom ** 2))
            third = (dubydt ** 2 * ((6 * a + 2 * b) * self.upper_e - 2 * b * self.lower_e)) / (self.denom ** 3)
            fourth = -((dubydt ** 3 * 6*a * (self.upper_e - self.lower_e)) / (self.denom ** 4))
            # Each corresponds to a row of the quick technique of integration by parts.
            result = first + second + third + fourth
        return result

    def main(self) -> dict:
        """
        This function gets a dictionary of coefficients, with keys of frequency and values of coefficients
        @return: A dictionary of coefficients
        """
        n = 0
        coeffs = {}
        for i in range(self.num_coeff):
            coeff = self.get_coefficient(n)
            coeffs.update({n: [coeff.real, coeff.imag]})
            # The complex coefficient is decomposed to its real and imaginary part as JavaScript does not support
            # complex numbers
            if i % 2 == 0:
                n += i+1
            else:
                n *= -1
            # By doing this operation, n progresses like: 0, 1, -1, 2, -2, 3, -3, ....
        return coeffs


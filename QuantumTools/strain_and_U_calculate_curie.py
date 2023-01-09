#! /usr/bin/env python3

"""
Script to calculate Curie temperatures
"""

import argparse
import sys
from math import cos, sqrt, sin, pi, fsum
from scipy.integrate import dblquad

__author__ = "Joren Vanherck"
__copyright__ = "Copyright (C) 2020 Joren Vanherck"
__credits__ = ["Joren Vanherck", "Cihan Bacaksiz", "Bart Soree", "Milorad V. Milosevic",
               "Wim Magnus"]
__license__ = "apache-2.0"

if sys.version_info.major < 3 or (sys.version_info.major == 3 and sys.version_info.minor < 6):
    raise Exception(f"Python 3.6 or a more recent version is required.")


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        """
        Print error message together with program documentation when error occurs while parsing arguments

        Args:
            message: Custom message to print to error stream
        """
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

    def valid_spin_value(self, string):
        """
        Validate string specifying spin value and convert it into a float

        Args:
            string: spin value, e.g. "1.5" or "2"

        Returns:
            The spin value as float, if positive and half-integer.
            Otherwise, suitable error message is printed.
        """
        spin = float(string)

        if spin <= 0.0:
            msg = "Spin value should be >0, but received " + str(spin)
            self.error(msg)

        if spin % 0.5:
            msg = "Spin value should be half-integer, but received " + str(spin)
            self.error(msg)

        return spin

    def valid_anisotropy_value(self, string):
        """
        Validate string specifying an anisotropy value and convert it into a float

        Args:
            string: anisotropy value, e.g. "-0.5" or "0.11"

        Returns:
            The anisotropy value as float, if -1.0 <= anisotropy <= 1.0.
            Otherwise, a suitable error message is printed
        """
        anisotropy = float(string)

        if anisotropy < -1.0 or anisotropy > 1.0:
            msg = "The anisotropy should be in the range [-1..1], but received " + str(anisotropy)
            self.error(msg)

        return anisotropy


def parse_args():
    """
    Parse command line arguments

    Returns:
        list containing parsed and processed command line arguments in standard form
    """
    parser = MyParser(description="Calculate Curie temperature for materials "
                                  "with honeycomb or hexagonal lattice structure")
    required = parser.add_argument_group('required arguments')
    parser.add_argument("-l", "--lattice",
                        choices=['hon', 'hex'],
                        default='hon', help="Honeycomb or hexagonal lattice structure")
    required.add_argument("-S", "--spin",
                          type=parser.valid_spin_value,
                          required=True,
                          help="Spin value S (only positive half-integer values)")
    required.add_argument("-J", "--exchange",
                          action="append", nargs="+",
                          required=True,
                          type=float,
                          help="Exchange strengths in meV.\n"
                               "\t1st, 2nd and 3rd NN values for honeycomb lattice structure. (space-separated)\n"
                               "\tOnly 1st NN value for hexagonal lattice structure.")
    required.add_argument("-D", "--anisotropy",
                          action="append", nargs="+",
                          required=True,
                          type=parser.valid_anisotropy_value,
                          help="Anisotropy values (in range [-1..1]).\n"
                               "\t1st, 2nd and 3rd NN values for honeycomb lattice structure. (space-separated)\n"
                               "\tOnly 1st NN value for hexagonal lattice structure.")

    required.add_argument("-st", "--st",
                          required=True,
                          type=float,
                          help="Strain level .\n")

    required.add_argument("-u", "--u",
                          required=True,
                          type=float,
                          help="U.\n")
    required.add_argument("-out", "--out",
                          required=True,
                          type=str,
                          help="Output_name.\n")
    

    params = process_args_from_parser(parser) 
    return params


def process_args_from_parser(parser):
    """
    Convert arguments from parser into standard form

    Args:
        parser: argument parser that has parsed the command line arguments

    Returns:
        list containing main function arguments in standard form
    """
    opts = parser.parse_args()

    if opts.lattice == "hon":
        if len(opts.exchange[0]) != 3:
            msg = "For honeycomb lattice type, 3 exchange parameters are expected, but received " \
                  + str(len(opts.exchange[0]))
            parser.error(msg)

        if len(opts.anisotropy[0]) != 3:
            msg = "For honeycomb lattice type, 3 anisotropy parameters are expected, but received " \
                  + str(len(opts.anisotropy[0]))
            parser.error(msg)

        param_list = opts.exchange[0] + opts.anisotropy[0]

    else:
        if len(opts.exchange[0]) != 1:
            msg = "For hexagonal lattice type, 1 exchange parameters is expected, but received " \
                  + str(len(opts.exchange[0]))
            parser.error(msg)

        if len(opts.anisotropy[0]) != 1:
            msg = "For honeycomb lattice type, 1 anisotropy parameters is expected, but received " \
                  + str(len(opts.anisotropy[0]))
            parser.error(msg)

        param_list = [0.0, opts.exchange[0][0], 0.0, 0.0, opts.anisotropy[0][0], 0.0]
    param_list.append(opts.spin)
    param_list.append(opts.st)
    param_list.append(opts.u)
    param_list.append(opts.out)
    return param_list


class NegativePhiC(RuntimeError):
    """
    Exception raised when phi_Curie evaluates to a negative value

    Attributes:
        kx, ky: k_x and k_y at which the negative value occurred
        message: Explanation of the error
    """

    def __init__(self, kx, ky):
        self.kx = kx
        self.ky = ky
        self.message = f"phi_C evaluated to a negative value in the Brillouin zone " \
                       f"at (k_x, k_y) = ({self.kx / pi:.3f} pi, {self.ky / pi:.3f} pi).\n" \
                       f"This is unexpected."

        super().__init__(self.message)


def integrate_hexagonal_brillouin_zone_with_twelvefold_symmetry(integrand):
    """
    Integrate integrand with twelve-fold symmetry over hexagonal Brillouin zone and return tuple(integral, abserror)

    Integration over hexagonal Brillouin zone of integrand(k_x, k_y).
    The integrand must be twelve-fold symmetric and is integrated in
    the domain k_x=[0..2*pi/sqrt(3)], k_y=[0..x/sqrt(3)]

    Args:
        integrand: The function f(k_x, k_y) to integrate

    Returns:
        Tuple of floats containing integral and abs_error
    """
    (integral, abserror) = tuple(
        output * 12 for output in dblquad(
            lambda y, x: integrand(x, y), 0, 2.0 * pi / sqrt(3), lambda x: 0, lambda x: x / sqrt(3)
        )
    )

    return integral, abserror


def _zeta_2(x, y):
    """zeta_2(kx, ky) function"""
    return 4.0 * cos(sqrt(3.0) * x / 2.0) * cos(y / 2.0) + 2.0 * cos(y)


def _zmu_2(x, y):
    """6 - zeta_2(kx, ky) function"""
    return 4.0 * (sin((sqrt(3.0) * x - y) / 4.0) ** 2 + sin((sqrt(3.0) * x + y) / 4.0) ** 2 + sin(y / 2.0) ** 2)


def _zeta_1re(x, y):
    """zeta_{1,R}(kx, ky) function"""
    return cos(x / sqrt(3.0)) + 2.0 * cos(x / (2.0 * sqrt(3.0))) * cos(y / 2.0)


def _zmu_1re(x, y):
    """3 - zeta_{1,R}(kx, ky) function"""
    return 2.0 * (sin(x / (2.0 * sqrt(3.0))) ** 2 +
                  sin((x / sqrt(3.0) - y) / 4.0) ** 2 + sin((x / sqrt(3.0) + y) / 4.0) ** 2)


def _zeta_1im(x, y):
    """zeta_{1,I}(kx, ky) function"""
    return sin(x / sqrt(3.0)) - 2.0 * sin(x / (2.0 * sqrt(3.0))) * cos(y / 2.0)


def _zeta_3re(x, y):
    """zeta_{3,R}(kx, ky) function"""
    return cos(2.0 * x / sqrt(3.0)) + 2.0 * cos(x / sqrt(3.0)) * cos(y)


def _zmu_3re(x, y):
    """3 - zeta_{3,R}(kx, ky) function"""
    return 2.0 * (sin(x / sqrt(3.0)) ** 2 +
                  sin((x / sqrt(3.0) - y) / 2.0) ** 2 + sin((x / sqrt(3.0) + y) / 2.0) ** 2)


def _zeta_3im(x, y):
    """zeta_{3,I}(kx, ky) function"""
    return -sin(2.0 * x / sqrt(3.0)) + 2.0 * sin(x / sqrt(3.0)) * cos(y)


class Material:
    """
    A class keeping track of material parameters.
    J values are in meV
    """

    def __init__(self, J_1, J_2, J_3, AN_1, AN_2, AN_3, S):
        self.J_1 = J_1
        self.J_2 = J_2
        self.J_3 = J_3
        self.AN_1 = AN_1
        self.AN_2 = AN_2
        self.AN_3 = AN_3
        self.S = S
        self.J_TOT = 3 * self.J_1 + 6 * self.J_2 + 3 * self.J_3
        self.delta = (3 * self.AN_1 * self.J_1
                      + 6 * self.AN_2 * self.J_2
                      + 3 * self.AN_3 * self.J_3) / self.J_TOT

    def _eta_even(self, x, y):
        """eta_{E}(kx, ky) function"""
        return self.J_2 / self.J_TOT * _zeta_2(x, y)

    def _mu_even(self, x, y):
        """6*eta_2 - eta_{E}(kx, ky) function"""
        return self.J_2 / self.J_TOT * _zmu_2(x, y)

    def _aneta_even(self, x, y):
        """iota_{E}(kx, ky) function"""
        return self.AN_2 * self.J_2 / self.J_TOT * _zeta_2(x, y)

    def _eta_re(self, x, y):
        """eta_{R}(kx, ky) function"""
        return self.J_1 / self.J_TOT * _zeta_1re(x, y) \
               + self.J_3 / self.J_TOT * _zeta_3re(x, y)

    def _mu_re(self, x, y):
        """3*eta_1 + 3*eta_3 - eta_{R}(kx, ky) function"""
        return self.J_1 / self.J_TOT * _zmu_1re(x, y) \
               + self.J_3 / self.J_TOT * _zmu_3re(x, y)

    def _aneta_re(self, x, y):
        """3*eta_1*an_1 + 3*eta_3*an_3 - iota_{R}(kx, ky) function"""
        return self.AN_1 * self.J_1 / self.J_TOT * _zeta_1re(x, y) \
               + self.AN_3 * self.J_3 / self.J_TOT * _zeta_3re(x, y)

    def _eta_im(self, x, y):
        """eta_{I}(kx, ky) function"""
        return self.J_1 / self.J_TOT * _zeta_1im(x, y) \
               + self.J_3 / self.J_TOT * _zeta_3im(x, y)

    def _aneta_im(self, x, y):
        """iota_{I}(kx, ky) function"""
        return self.AN_1 * self.J_1 / self.J_TOT * _zeta_1im(x, y) \
               + self.AN_3 * self.J_3 / self.J_TOT * _zeta_3im(x, y)

    def phi_curie(self, x, y):
        """
        Calculate the phi_curie integrand at point k_x and k_y

        Args:
            x, y: point of integrand evaluation

        Returns:
            Value of integrand op specified point
        """
        real_diff = self._eta_re(x, y) - self._aneta_re(x, y)
        imaginary_diff = self._eta_im(x, y) - self._aneta_im(x, y)
        even_diff = self._eta_even(x, y) - self._aneta_even(x, y)
        a = 1 + self.delta - even_diff
        a_minus_real_diff = fsum(
            [self._aneta_even(x, y), self._aneta_re(x, y), self._mu_even(x, y), self._mu_re(x, y), self.delta])
        denominator = a_minus_real_diff * (a + real_diff) - imaginary_diff ** 2

        phi_curie = (a + real_diff) / denominator

        # The integrand should never become negative
        if phi_curie < 0:
            raise NegativePhiC(x, y)

        return phi_curie

    # Some constants
    reciprocal_cell_volume = 8 * pi ** 2 / sqrt(3)
    boltzmann_constant = 8.61733034e-2  # meV/K

    def calculate_curie_temperature(self):
        """
        Calculate the Curie temperature based on the stored material properties

        Returns:
            The calculated Curie temperature in Kelvin
        """
        # No sensible results for overall anti-ferromagnetic interaction
        if self.J_TOT < 0.0:
            #print(f"Please make sure that the total exchange strength J(0)=3*J1 + 6*J2 + 3*J3 is positive.\n"
             #     f"J(0) for the given parameters was {self.J_TOT:.4f}.")
            print(f"Tot J negative.\n")
            sys.exit(0)

        # for negative overall anisotropy, the Curie temperature vanishes
        if self.delta <= 0.0:
            return 0.0

        try:
            (integral, abs_error) = integrate_hexagonal_brillouin_zone_with_twelvefold_symmetry(self.phi_curie)
            inverse_curie_temp = Material.boltzmann_constant * 3 * integral / \
                                 (self.S * (self.S + 1) * self.J_TOT * self.reciprocal_cell_volume)
            return 1 / inverse_curie_temp
        except NegativePhiC as exc:
            print(exc)
            raise


if __name__ == '__main__':
    # parse command line arguments into standard form
    #MODIFICATION: now parser (both, class and function) recieves 3 more parameters: st,u,out (outputfile)
    # the new output of the parser is total_parsed_args and then parsed_args has just the original parameters that enter in the 
    # function material.
    total_parsed_args = parse_args()
    parsed_args = [total_parsed_args[0],total_parsed_args[1],total_parsed_args[2],total_parsed_args[3],total_parsed_args[4],total_parsed_args[5],total_parsed_args[6]]
    st = total_parsed_args[7]
    u = total_parsed_args[8]
    out = total_parsed_args[9]
    file_Tc = open('Tc_results.txt', 'w')
    #print(total_parsed_args)
    #print(parsed_args)
    #print(st,u,out)
    # Construct material from unpacked list of arguments
    material = Material(*parsed_args)

    try:
        file_Tc.write(str(st) + " " + str(u) + " " + str(material.calculate_curie_temperature()) )
        print(f"The Curie temperature is {material.calculate_curie_temperature():.2f} K")
    except NegativePhiC:
        sys.stderr.write(f"The Curie temperature could not be calculated.")
    file_Tc.close()

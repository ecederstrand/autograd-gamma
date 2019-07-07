from autograd.extend import primitive, defvjp
from autograd import numpy as np
from autograd.scipy.special import gammaln
from autograd.numpy.numpy_vjps import unbroadcast_f
from scipy.special import gammainc as _scipy_gammainc, gammaincc as _scipy_gammaincc

__all__ = [
    'gammainc', # regularized lower incomplete gamma function
    'gammaincc', # regularized upper incomplete gamma function
    'gamma', # gamma function
    'reg_lower_inc_gamma', # alias
    'reg_upper_inc_gamma'  # alias
]



gammainc = primitive(_scipy_gammainc)
gammaincc = primitive(_scipy_gammaincc)


def central_difference_of_(f):
    def _central_difference(ans, a, x):
        return unbroadcast_f(
            a,
            lambda g: g
            * (
                -f(a + 2 * DELTA, x)
                + 8 * f(a + DELTA, x)
                - 8 * f(a - DELTA, x)
                + f(a - 2 * DELTA, x)
            )
            / (12 * DELTA),
        )
    return _central_difference



defvjp(
    gammainc,
    central_difference_of_(gammainc),
    lambda ans, a, x: unbroadcast_f(x, lambda g: g * np.exp(-x + np.log(x)*(a - 1) - gammaln(a)))
)


defvjp(
    gammaincc,
    central_difference_of_(gammaincc),
    lambda ans, a, x: unbroadcast_f(x, lambda g: -g * np.exp(-x + np.log(x)*(a - 1) - gammaln(a)))
)


reg_lower_inc_gamma = gammainc
reg_upper_inc_gamma = gammaincc

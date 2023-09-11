from typing import Union

from abc import ABC, abstractmethod

import numpy as np
from scipy.special import ndtri
from scipy.stats import chi2


class BaseInterval(ABC):
    """
    Abstract base class for confidence interval calculation.
    """

    def __init__(
        self, numerator: Union[int, float], denominator: Union[int, float], alpha: float = 0.05
    ):
        """
        Args:
        ----
          numerator (int | float | None): the number of observed event.
          denominator (int | float | None): the denominator population at risk. Can be count or time.
          alpha (float): the confidence level required for the confidence interval. Default: 0.05 (95%).
        """
        super().__init__()
        self.numerator = numerator
        self.denominator = denominator
        self.alpha = alpha

    @abstractmethod
    def lower_bound(self) -> float:
        pass

    @abstractmethod
    def upper_bound(self) -> float:
        pass


class ChiSquaredConfidenceInterval(BaseInterval):
    """
    Chi-squared exact method:
    ------------------------

    A rate of events  r  is given by:
      r = O / n

    where:
      O  is the numerator number of observed events.
      n  is the denominator population-years at risk.

    Using the link between the Poisson and χ2  distributions the 100(1-alpha)%  confidence limits
    for an observed number of events O (such as the numerator of a rate) are given by:

      O_lower = χ2_lower/2

      O_upper = χ2_upper/2

    where,
      χ2_lower is the 100(alpha/2)th percentile value from the χ2 distribution with 2O degrees of freedom.
      χ2_upper is the 100(1-alpha/2)th percentile value from the χ2 distribution with 2O+2 degrees of freedom
    """

    def __init__(
        self, numerator: Union[int, float], denominator: Union[int, float], alpha: float = 0.05
    ):
        """
        Args:
        ----
          numerator (int | float | None): the number of observed event.
          denominator (int | float | None): the denominator population at risk. Can be count or time.
          alpha (float): the confidence level required for the confidence interval. Default: 0.05 (95%).
        """
        super().__init__(numerator, denominator, alpha)

    def upper_bound(self) -> float:
        b = chi2.ppf(1 - (self.alpha / 2), 2 * self.numerator + 2) / 2
        upper_ci: float = b / self.denominator
        return upper_ci

    def lower_bound(self) -> float:
        b = chi2.ppf((self.alpha / 2), (self.numerator * 2)) / 2
        lower_ci: float = b / self.denominator
        return lower_ci


class ByarsConfidenceInterval(BaseInterval):
    """
    As per the Public Health England Guidelines for Confidence Intervals (Version: 25 May 2018):
    Byar's method is used when the numerator (count) is at least 10. When the numerator is less than 10,
    the exact χ2  method is used.

    Byar's method:
    -------------

    A rate of events  r  is given by:
      r = O / n

    where:
      O  is the numerator number of observed events.
      n  is the denominator population-years at risk.

    The  100(1-alpha)%  confidence limits for the rate  r  are given by:
      r_lower = O_lower/n
      r_upper = O_upper/n

    where:
      O_lower and O_upper are the lower and upper confidence limits for the observed number of events.

    Using Byar's method the  100(1-alpha)%  confidence limits for the observed number of events are given by:

      O_lower = O(1 - 1/9O - z/3√O)^3

      O_upper = (O+1)(1 - 1/9(O+1) - z/3√(O+1))^3

    where:
      z is the 100(1-alpha/2)th percentile value from the Standard Normal distribution.
    """

    def __init__(
        self, numerator: Union[int, float], denominator: Union[int, float], alpha: float = 0.05
    ):
        """
        Args:
        ----
          numerator (int | float): the number of observed event.
          denominator (int | float): the denominator population at risk. Can be count or time.
          alpha (float): the confidence level required for the confidence interval. Default: 0.05 (95%).
        """
        super().__init__(numerator, denominator, alpha)

        self.chi_squared = ChiSquaredConfidenceInterval(numerator, denominator)

    def upper_bound(self) -> float:

        if self.numerator < 10:
            upper_ci = self.chi_squared.upper_bound()
        else:
            z = ndtri(1 - self.alpha / 2)
            c = 1 / (9 * (self.numerator + 1))
            b = 3 * (np.sqrt(self.numerator + 1))
            upper_o = (self.numerator + 1) * ((1 - c + (z / b)) ** 3)
            upper_ci = upper_o / self.denominator
        return upper_ci

    def lower_bound(self) -> float:

        if self.numerator is None:
            return 0.0

        if self.numerator < 10:
            lower_ci = self.chi_squared.lower_bound()
        else:
            z = ndtri(1 - self.alpha / 2)
            c = 1 / (9 * self.numerator)
            b = 3 * np.sqrt(self.numerator)
            lower_o = self.numerator * ((1 - c - (z / b)) ** 3)
            lower_ci = lower_o / self.denominator
        return lower_ci

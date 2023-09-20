from typing import List, Tuple, Type, Union

from abc import ABC
from datetime import datetime

import pandas as pd
from dateutil.relativedelta import relativedelta

from analogy.core.confidence_interval import BaseInterval, ByarsConfidenceInterval
from analogy.core.preprocessor import convert_str_to_datetime, format_datatypes
from analogy.data import load_sample_data


class Incidence:
    """
    Manages the automated incidence rate calculations on an user provided dataset.
    Normal use would initialise the object, then use any of:
      calculate_overall_incidence
      calculate_grouped_incidence

    Required Args:
      data (pd.DataFrame): User provided dataset to calculate incidence rates on.
      study_start_date (str): Start date of the study.
      study_end_date (str): Start date of the study.
      patient_start_col (str): column for the start date for patient follow-up.
      patient_end_col (str): column for the end date for patient follow-up

    Optional Args:
      conditions (List[str]): Default: []. Defines the list of columns for the base event dates.
      demography (List[str]): Default: []. Defines columns to use as grouping variables.
      person_years (int): Default: 1.0. Number of person years to scale by incidence rates by.
      alpha (float): Default: 0.05. Significance level for calulating error using Byar's method.
      increment_by_months (int): Default: 12. Number of months in each incidence calculation. By default returns yearly incidence rates.
      confidence_method (BaseInterval): Default: ByarsConfidenceInterval. Method to use for calculating confidence Interval.
      date_format (str): Default: 'ISO8601': the date format stored in the dataset.
    Returns:
      aggregated_df (pd.DataFrame): Aggregated Incidence rates with columns [Date, Group, Sub Group, Rate, Numerator, Denominator, CI_lower, CI_upper]
    """

    def __init__(
        self,
        data: pd.DataFrame,
        study_start_date: str,
        study_end_date: str,
        patient_start_col: str,
        patient_end_col: str,
        conditions: List[str] = [],
        demography: List[str] = [],
        person_years: Union[int, float] = 1.0,
        alpha: float = 0.05,
        increment_by_months: int = 12,
        confidence_method: Type[BaseInterval] = ByarsConfidenceInterval,
        date_format: str = "ISO8601",
    ) -> None:
        self.data = format_datatypes(
            data=data,
            condition_cols=conditions,
            demography_cols=demography,
            date_format=date_format,
            patient_follow_up_cols=[patient_start_col, patient_end_col],
        )
        self.__analysis_overall = None
        self.__analysis_subgroup = None
        self.study_start_date = convert_str_to_datetime(study_start_date, format=date_format)
        self.study_end_date = convert_str_to_datetime(
            study_end_date, format=date_format
        ) + relativedelta(years=0, months=0, days=1)
        self.patient_start_col = patient_start_col
        self.patient_end_col = patient_end_col
        self.conditions = conditions
        self.demography = demography
        self.person_years = person_years
        self.increment_by_months = increment_by_months
        self.dateformat = date_format
        self.confidence_method = confidence_method()

    def period_incidence(
        self,
        dataframe: pd.DataFrame,
        start_yr: datetime,
        end_yr: datetime,
        condition_col: str,
        group: str = "Overall",
        sub_group: str = "",
    ) -> Tuple[str, str, str, str, float, int, float, float, float]:
        """
        Function definition for period incidence calculation.

        Args:
            dataframe: the full or grouped pandas dataframe.
            start_yr: datetime value to start calculating incidence from.
            end_yr: datetime value to end calculating incidence on.
            datecol_name: baseline variable column name.

        Return:
            tuple (year, incidence rate, denominator, numerator, lower_ci, upper_ci, error_delta, count)

        """

        numerator = len(
            dataframe[
                (dataframe[condition_col].between(start_yr, end_yr, inclusive="left"))
                & (dataframe[self.patient_end_col] >= start_yr)
                & (dataframe[self.patient_start_col] < end_yr)
                & (dataframe[condition_col] > dataframe[self.patient_start_col])
            ]
        )
        denominator_df = dataframe[
            (
                (dataframe[self.patient_end_col] >= start_yr)
                & (dataframe[self.patient_start_col] < end_yr)
            )
            & (
                (dataframe[condition_col] >= start_yr)
                & (dataframe[condition_col] > dataframe[self.patient_start_col])
                | (dataframe[condition_col].isna())
            )
        ]

        start_period = denominator_df[self.patient_start_col].where(
            denominator_df[self.patient_start_col] > start_yr, start_yr
        )
        end_period = denominator_df[[self.patient_end_col, condition_col]].min(axis=1)
        end_period = end_period.where(end_period < end_yr, end_yr)
        delta = end_yr - start_yr
        time_contributed = (end_period - start_period).dt.days / delta.days

        denominator = float(time_contributed.sum() + 1e-8)

        point_inc = float((numerator / denominator) * self.person_years)

        lower_ci = self.confidence_method.lower_bound(numerator, denominator)
        upper_ci = self.confidence_method.upper_bound(numerator, denominator)

        return (
            condition_col,
            start_yr.date().strftime(self.dateformat),
            group,
            sub_group,
            point_inc,
            numerator,
            denominator,
            lower_ci * self.person_years,
            upper_ci * self.person_years,
        )

    def calculate_overall_incidence(self) -> pd.DataFrame:
        """
        Function definition for overall incidence rate calculation.
        """
        overall_df_list = []
        for condition_col in self.conditions:
            df_list = []
            current_period = self.study_start_date
            while current_period < self.study_end_date:
                delta = relativedelta(months=self.increment_by_months)
                end_period = min(self.study_end_date, current_period + delta)
                year_tuple = self.period_incidence(
                    self.data, current_period, end_period, condition_col
                )
                df_list.append(year_tuple)
                current_period += delta
            overall_df_list.append(
                pd.DataFrame(
                    df_list,
                    columns=[
                        "Condition",
                        "Date",
                        "Group",
                        "Subgroup",
                        "Incidence",
                        "Numerator",
                        "Denominator",
                        "Lower_CI",
                        "Upper_CI",
                    ],
                )
            )

        if len(overall_df_list) > 0:
            self.__analysis_overall = pd.concat(overall_df_list)
        else:
            self.__analysis_overall = pd.DataFrame()
        return self.__analysis_overall

    def calculate_grouped_incidence(self) -> pd.DataFrame:
        """
        Function definition for subgroup incidence rate calculation.
        """
        overall_df_list = []
        for condition_col in self.conditions:
            for demo in self.demography:
                subgroup_list = []
                for name, group in self.data.groupby(demo, observed=False):
                    current_period = self.study_start_date
                    while current_period < self.study_end_date:
                        delta = relativedelta(months=self.increment_by_months)
                        end_period = min(self.study_end_date, current_period + delta)
                        year_tuple = self.period_incidence(
                            group, current_period, end_period, condition_col, demo, name
                        )
                        subgroup_list.append(year_tuple)
                        current_period += delta
                group_df = pd.DataFrame(
                    subgroup_list,
                    columns=[
                        "Condition",
                        "Date",
                        "Group",
                        "Subgroup",
                        "Incidence",
                        "Numerator",
                        "Denominator",
                        "Lower_CI",
                        "Upper_CI",
                    ],
                )
                overall_df_list.append(group_df)

        if len(overall_df_list) > 0:
            self.__analysis_subgroup = pd.concat(overall_df_list)
        else:
            self.__analysis_subgroup = pd.DataFrame()

        return self.__analysis_subgroup

    def analyse(self) -> pd.DataFrame:
        overall_df = self.calculate_overall_incidence()
        subgroup_df = self.calculate_grouped_incidence()
        return pd.concat([overall_df, subgroup_df])


class Prevalence:
    """
    Manages the automated prevalence proportion calculations on an user provided dataset.
    Normal use would initialise the object, then use any of:
      calculate_overall_prevalence
      calculate_grouped_prevalence

    Required Args:
      data (pd.DataFrame): User provided dataset to calculate prevalence proportions on.
      study_start_date (str): Start date of the study.
      study_end_date (str): Start date of the study.
      patient_start_col (str): column for the start date for patient follow-up.
      patient_end_col (str): column for the end date for patient follow-up

    Optional Args:
      conditions (List[str]): Default: []. Defines the list of columns for the base event dates.
      demography (List[str]): Default: []. Defines columns to use as grouping variables.
      person_years (int): Default: 1.0. Number of person years to scale by incidence rates by.
      alpha (float): Default: 0.05. Significance level for calulating error using Byar's method.
      increment_by_months (int): Default: 12. Number of months in each incidence calculation. By default returns yearly incidence rates.
      confidence_method (BaseInterval): Default: ByarsConfidenceInterval. Method to use for calculating confidence Interval.
      date_format (str): Default: 'ISO8601': the date format stored in the dataset.
    Returns:
      aggregated_df (pd.DataFrame): Aggregated Incidence rates with columns [Date, Group, Sub Group, Rate, Numerator, Denominator, CI_lower, CI_upper]
    """

    def __init__(
        self,
        data: pd.DataFrame,
        study_start_date: str,
        study_end_date: str,
        patient_start_col: str,
        patient_end_col: str,
        conditions: List[str] = [],
        demography: List[str] = [],
        person_years: Union[int, float] = 1.0,
        alpha: float = 0.05,
        increment_by_months: int = 12,
        confidence_method: Type[BaseInterval] = ByarsConfidenceInterval,
        date_format: str = "ISO8601",
    ) -> None:
        self.data = format_datatypes(
            data=data,
            condition_cols=conditions,
            demography_cols=demography,
            date_format=date_format,
            patient_follow_up_cols=[patient_start_col, patient_end_col],
        )
        self.__analysis_overall = None
        self.__analysis_subgroup = None
        self.study_start_date = convert_str_to_datetime(study_start_date, format=date_format)
        self.study_end_date = convert_str_to_datetime(
            study_end_date, format=date_format
        ) + relativedelta(years=0, months=0, days=1)
        self.patient_start_col = patient_start_col
        self.patient_end_col = patient_end_col
        self.conditions = conditions
        self.demography = demography
        self.person_years = person_years
        self.increment_by_months = increment_by_months
        self.dateformat = date_format
        self.confidence_method = confidence_method()

    def point_prevalence(
        self,
        dataframe: pd.DataFrame,
        start_yr: datetime,
        condition_col: str,
        group: str = "Overall",
        sub_group: str = "",
    ) -> Tuple[str, str, str, str, float, int, int, float, float]:
        """
        Function definition for period incidence calculation.

        Args:
            dataframe: the full or grouped pandas dataframe.
            start_yr: datetime value to start calculating incidence from.
            datecol_name: baseline variable column name.

        Return:
            tuple (year, incidence rate, denominator, numerator, lower_ci, upper_ci, error_delta, count)

        """

        # event that occured before the year of interest which is a combination of outcome recording that is
        # before that year of interest
        numerator = float(
            len(
                dataframe[
                    (
                        (dataframe[self.patient_start_col] <= start_yr)
                        & (dataframe[self.patient_end_col] >= start_yr)
                    )
                    & (dataframe[condition_col] <= start_yr)
                ]
            )
        )

        # Patients who are in the practice at the start of the interested year, that is they enter the cohort
        # before the start of the interested year and have not exited before the start of the interested year
        denominator = float(
            len(
                dataframe[
                    (dataframe[self.patient_start_col] <= start_yr)
                    & (dataframe[self.patient_end_col] >= start_yr)
                ]
            )
        )

        denominator = denominator + 1e-8  # adding a small constant to avoid division by zero.
        point_prev = (numerator / denominator) * self.person_years

        lower_ci = self.confidence_method.lower_bound(numerator, denominator)
        upper_ci = self.confidence_method.upper_bound(numerator, denominator)

        return (
            condition_col,
            start_yr.date().strftime(self.dateformat),
            group,
            sub_group,
            point_prev,
            int(numerator),
            int(denominator),
            lower_ci * self.person_years,
            upper_ci * self.person_years,
        )

    def calculate_overall_prevalence(self) -> pd.DataFrame:
        """
        Function definition for overall incidence rate calculation.
        """
        overall_df_list = []
        for condition_col in self.conditions:
            df_list = []
            current_period = self.study_start_date
            while current_period < self.study_end_date:
                delta = relativedelta(months=self.increment_by_months)
                year_tuple = self.point_prevalence(self.data, current_period, condition_col)
                df_list.append(year_tuple)
                current_period += delta
            overall_df_list.append(
                pd.DataFrame(
                    df_list,
                    columns=[
                        "Condition",
                        "Date",
                        "Group",
                        "Subgroup",
                        "Prevalence",
                        "Numerator",
                        "Denominator",
                        "Lower_CI",
                        "Upper_CI",
                    ],
                )
            )

        if len(overall_df_list) > 0:
            self.__analysis_overall = pd.concat(overall_df_list)
        else:
            self.__analysis_overall = pd.DataFrame()
        return self.__analysis_overall

    def calculate_grouped_prevalence(self) -> pd.DataFrame:
        """
        Function definition for subgroup incidence rate calculation.
        """
        overall_df_list = []
        for condition_col in self.conditions:
            for demo in self.demography:
                subgroup_list = []
                for name, group in self.data.groupby(demo, observed=False):
                    current_period = self.study_start_date
                    while current_period < self.study_end_date:
                        delta = relativedelta(months=self.increment_by_months)
                        year_tuple = self.point_prevalence(
                            group, current_period, condition_col, demo, name
                        )
                        subgroup_list.append(year_tuple)
                        current_period += delta
                group_df = pd.DataFrame(
                    subgroup_list,
                    columns=[
                        "Condition",
                        "Date",
                        "Group",
                        "Subgroup",
                        "Prevalence",
                        "Numerator",
                        "Denominator",
                        "Lower_CI",
                        "Upper_CI",
                    ],
                )
                overall_df_list.append(group_df)

        if len(overall_df_list) > 0:
            self.__analysis_subgroup = pd.concat(overall_df_list)
        else:
            self.__analysis_subgroup = pd.DataFrame()

        return self.__analysis_subgroup

    def analyse(self) -> pd.DataFrame:
        overall_df = self.calculate_overall_prevalence()
        subgroup_df = self.calculate_grouped_prevalence()
        return pd.concat([overall_df, subgroup_df])


if __name__ == "__main__":
    df = load_sample_data()
    inc = Prevalence(
        data=df,
        study_start_date="2001-01-01 00:00:00.0",
        study_end_date="2020-12-31 00:00:00.0",
        patient_start_col="START_DATE",
        patient_end_col="END_DATE",
        conditions=["CONDITION"],
        demography=["SEX", "ETHNICITY"],
        date_format="%Y-%m-%d %H:%M:%S.%f",
        increment_by_months=12,
        person_years=1000,
    )

    result = inc.analyse()
    print(result.head(10))

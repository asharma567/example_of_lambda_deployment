import numpy as np
import pandas as pd


def make_all_date_related_features_inplace(df_before_preprocessing, df_after_preprocessing):
    df_before_preprocessing = coerce_columns_to_datetime(df_before_preprocessing,
                                                         ['generated_at_budget', 'start_datetime_trips',
                                                          'end_datetime_trips', 'transaction_date_itemization'])

    df_after_preprocessing['start_datetime_vs_transaction_date_delta_seconds'] = df_before_preprocessing.apply(
        lambda row: calc_delta_from_timestamps_in_seconds(row['start_datetime_trips'],
                                                          row['transaction_date_itemization']),
        axis=1)
    df_after_preprocessing['end_datetime_vs_transaction_date_delta_seconds'] = df_before_preprocessing.apply(
        lambda row: calc_delta_from_timestamps_in_seconds(row['end_datetime_trips'],
                                                          row['transaction_date_itemization']),
        axis=1)
    df_after_preprocessing['generated_at_vs_transaction_date_delta_seconds'] = df_before_preprocessing.apply(
        lambda row: calc_delta_from_timestamps_in_seconds(row['generated_at_budget'],
                                                          row['transaction_date_itemization']),
        axis=1)

    df_after_preprocessing['within_generated_at_or_trip_frame'] = df_after_preprocessing.apply(
        lambda row: (
                        # if the transaction is within either upperbound options(generated_at or start_datetime) the
                        # fields will be negative
                        row['start_datetime_vs_transaction_date_delta_seconds'] < 0
                        or
                        row['generated_at_vs_transaction_date_delta_seconds'] < 0
                        # and this will be positive
                    ) and row['end_datetime_vs_transaction_date_delta_seconds'] > 0,
        axis=1)

    df_after_preprocessing['number_of_days_of_trip'] = \
        df_before_preprocessing.apply(
            lambda row: calc_delta_from_timestamps_in_days(row['end_datetime_trips'], row['start_datetime_trips']),
            axis=1)

    # solving for same-day trips which are common in cars, flights, rail, not hotel. It'll later effects the number
    # of days dependent fields
    df_after_preprocessing['number_of_days_of_trip'] = df_after_preprocessing['number_of_days_of_trip'].apply(
        lambda x: 1.0 if float(x) == 0.0 else x)

    df_after_preprocessing['within_time_frame_budget_generated_end_trip'] = \
        df_before_preprocessing.apply(lambda row: check_if_expense_lineitem_within_time_frame(
            (row['generated_at_budget'], row['end_datetime_trips']),
            row['transaction_date_itemization']), axis=1)

    df_after_preprocessing['within_time_frame_start_end_trip'] = \
        df_before_preprocessing.apply(lambda row: check_if_expense_lineitem_within_time_frame(
            (row['start_datetime_trips'], row['end_datetime_trips']),
            row['transaction_date_itemization']), axis=1)

    df_after_preprocessing['min_date_delta_from_frame_generated_at'] = \
        df_before_preprocessing.apply(lambda row: get_the_min_date_delta(
            (row['generated_at_budget'], row['end_datetime_trips']),
            row['transaction_date_itemization']), axis=1)

    df_after_preprocessing['min_date_delta_from_frame_start_datetime'] = \
        df_before_preprocessing.apply(lambda row: get_the_min_date_delta(
            (row['generated_at_budget'], row['end_datetime_trips']),
            row['transaction_date_itemization']), axis=1)

    return None


def coerce_columns_to_datetime(df, datetime_cols):
    df[datetime_cols] = df[datetime_cols].apply(pd.to_datetime)
    return df


def calc_delta_from_timestamps_in_seconds(time_stamp1, time_stamp2):
    return (time_stamp1 - time_stamp2).total_seconds()


def calc_delta_from_timestamps_in_days(time_stamp1, time_stamp2):
    return (time_stamp1 - time_stamp2).days


def check_if_expense_lineitem_within_time_frame(timestamp_tuple, transaction_time_of_lineitem):
    """
    this checks if the transaction time of the expense falls within bounds of
    i) time subject budget was generated or start_datetime
    ii) trip end date.
    Motivation for this was that most expense lineitems fall within this date range.

    *we have special issue with the datetimes being around 24 hours of distane from one another
    make sure to note this as it may cause some noise. The cause for this is the field is stored
    2016-07-10 so the time is truncated.

    use with a dataframe:

    df.apply(lambda row: check_if_expense_lineitem_within_time_frame(
        (row['generated_at_budget'], row['end_datetime_trips']),
        row['transaction_date_itemization']) ,
        axis=1)
    """
    THRESHOLD_FOR_EXPENSE_DATE = '1 days 00:00:00'

    begining_of_window, end_of_window = timestamp_tuple

    # simple check to see if the lineitem/expense time falls well within the time-frame
    if begining_of_window <= transaction_time_of_lineitem <= end_of_window:
        return True

    '''
    This lower half is to accomodate the 24 hour noise in the datetime field.

    normalize first *need to at the motivation for this but the idea is if you don't then it won't 
    account for all the ones which are technically over 24 hours 
    e.g.('2016-07-10 04:00:00', '2016-07-13 04:00:00'), '2016-07-09')
    '''

    begining_of_window_truncated, end_of_window_truncated = map(drop_hours_minutes_handle, timestamp_tuple)

    if check_within_tolerance_window(THRESHOLD_FOR_EXPENSE_DATE, begining_of_window_truncated,
                                     transaction_time_of_lineitem):
        return True
    if check_within_tolerance_window(THRESHOLD_FOR_EXPENSE_DATE, end_of_window_truncated, transaction_time_of_lineitem):
        return True

    return False


def get_the_min_date_delta(time_stamp_tuple, line_item_time_of_purchase):
    begining_of_window_truncated, end_of_window_truncated = map(drop_hours_minutes_handle, time_stamp_tuple)

    delta_lower_bound = calc_absolute_delta_from_timestamps_in_seconds(begining_of_window_truncated,
                                                                       line_item_time_of_purchase)
    delta_upper_bound = calc_absolute_delta_from_timestamps_in_seconds(end_of_window_truncated,
                                                                       line_item_time_of_purchase)

    return min(delta_lower_bound, delta_upper_bound)


def drop_hours_minutes_handle(time_stamp):
    time_stamp_truncated = pd.to_datetime(str(time_stamp).split()[0])

    return time_stamp_truncated


def check_within_tolerance_window(tolerance_window, time_stamp1, time_stamp2):
    return pd.to_timedelta(tolerance_window).total_seconds() >= calc_absolute_delta_from_timestamps_in_seconds(
        time_stamp1, time_stamp2)


def calc_absolute_delta_from_timestamps_in_seconds(time_stamp1, time_stamp2):
    return np.abs(time_stamp1 - time_stamp2).total_seconds()

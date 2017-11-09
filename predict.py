import joblib
import pandas as pd

from preprocess_dates import make_all_date_related_features_inplace
from preprocess_prices import make_all_price_related_features_inplace
from preprocess_strings import make_all_string_related_features_inplace

model_car = joblib.load('rf_car_27.pkl')
model_flight = joblib.load('rf_flight_27.pkl')
model_hotel = joblib.load('rf_hotel_27.pkl')
model_rail = joblib.load('rf_rail_27.pkl')


def predict_if_budget_matches_itemization(flat_budget_and_itemization_data):
    """
    Wrapper function to the predict method in persisted sklearn model and
    the preprocessing. This is the main function you would pass data to
    for a prediction.

    I: dictionary which represents budget data and itemization data, fields listed below
    O: 0.0-1.0 (float) (percent match)
    """

    df = pd.DataFrame(flat_budget_and_itemization_data, index=[0])

    nparray_vector_model_input = preprocess_budget_and_itemization_data_row_by_row(df)
    del nparray_vector_model_input['budget_type_budget']

    final_score = route_to_correct_model(df['budget_type_budget'].values, nparray_vector_model_input)
    return final_score


def preprocess_budget_and_itemization_data_row_by_row(df_before_preprocessing):
    df_after_preprocessing = pd.DataFrame()

    df_after_preprocessing['budget_type_budget'] = df_before_preprocessing['budget_type_budget']
    df_after_preprocessing['budget_id'] = df_before_preprocessing['budget_id']

    make_all_date_related_features_inplace(df_before_preprocessing, df_after_preprocessing)
    make_all_price_related_features_inplace(df_before_preprocessing, df_after_preprocessing)
    make_all_string_related_features_inplace(df_before_preprocessing, df_after_preprocessing)

    return df_after_preprocessing


def route_to_correct_model(budget_type, vector):
    if budget_type == 'flight':
        return predict_if_match(vector, model_flight)
    if budget_type == 'car':
        return predict_if_match(vector, model_car)
    if budget_type == 'hotel':
        return predict_if_match(vector, model_hotel)
    if budget_type == 'rail':
        return predict_if_match(vector, model_rail)
    return None


def predict_if_match(vectorized_budget_and_itemization_datapoint, model):
    percent_negative, percent_positive = model.predict_proba(vectorized_budget_and_itemization_datapoint)[0]
    return percent_positive

import py_stringmatching as sm
from utils.helpers_string_normalizer import normalize, POST_NORMALIZATION_STOP_WORDS_FOR_VENDOR_NAME, \
    POST_NORMALIZATION_STOP_WORDS_FOR_CAR_VENDOR_NAME, STOP_WORDS_FOR_FLIGHTS_VENDOR_NAME_EXPENSE, \
    POST_NORMALIZATION_STOP_WORDS_FOR_CAR_EXPENSE_TYPE_NAME, STOP_WORDS_FOR_FLIGHTS_EXPENSE_TYPE_NAME, \
    STOP_WORDS_FOR_RAIL_EXPENSE_TYPE_NAME


def make_all_string_related_features_inplace(df_before_preprocessing, df_after_preprocessing):
    df_before_preprocessing['vendor_name_expense_normalized'] = df_before_preprocessing['vendor_name_expense'].apply(
        normalize)
    df_before_preprocessing['purchase_vendor_receipts_normalized'] = df_before_preprocessing[
        'purchase_vendor_receipts'].apply(normalize)
    df_before_preprocessing['travel_vendor_receipts_normalized'] = df_before_preprocessing[
        'travel_vendor_receipts'].apply(normalize)
    df_before_preprocessing['expense_type_name_expense_normalized'] = df_before_preprocessing[
        'expense_type_name_expense'].apply(normalize)
    df_before_preprocessing['expense_type_name_itemization_normalized'] = df_before_preprocessing[
        'expense_type_name_itemization'].apply(normalize)
    df_before_preprocessing['expense_category_itemization_normalized'] = df_before_preprocessing[
        'expense_category_itemization'].apply(normalize)
    df_before_preprocessing['expense_category_expense_normalized'] = df_before_preprocessing[
        'expense_category_expense'].apply(normalize)

    df_after_preprocessing['vendor_name_in_hotel_name_stopwords'] = \
        df_before_preprocessing['vendor_name_expense_normalized'].apply(
            lambda x: check_membership_if_in_stopwords(x, POST_NORMALIZATION_STOP_WORDS_FOR_VENDOR_NAME))
    df_after_preprocessing['vendor_name_in_car_stopwords'] = \
        df_before_preprocessing['vendor_name_expense_normalized'].apply(
            lambda x: check_membership_if_in_stopwords(x, POST_NORMALIZATION_STOP_WORDS_FOR_CAR_VENDOR_NAME))
    df_after_preprocessing['vendor_name_in_flights_name_stopwords'] = \
        df_before_preprocessing['vendor_name_expense_normalized'].apply(
            lambda x: check_membership_if_in_stopwords(x, STOP_WORDS_FOR_FLIGHTS_VENDOR_NAME_EXPENSE))

    df_after_preprocessing['tax_str_in_expense_type_name_expense'] = \
        df_before_preprocessing['expense_type_name_expense_normalized'].apply(lambda x: check_if_tax_in_str(x))
    df_after_preprocessing['tax_str_in_expense_type_name_itemization'] = \
        df_before_preprocessing['expense_type_name_itemization_normalized'].apply(lambda x: check_if_tax_in_str(x))

    df_after_preprocessing['expense_type_name_in_car_stopwords_itemization'] = \
        df_before_preprocessing['expense_type_name_itemization_normalized'].apply(
            lambda x: check_membership_if_in_stopwords(x, POST_NORMALIZATION_STOP_WORDS_FOR_CAR_EXPENSE_TYPE_NAME))
    df_after_preprocessing['expense_type_name_in_car_stopwords_expense'] = \
        df_before_preprocessing['expense_type_name_expense_normalized'].apply(
            lambda x: check_membership_if_in_stopwords(x, POST_NORMALIZATION_STOP_WORDS_FOR_CAR_EXPENSE_TYPE_NAME))

    df_after_preprocessing['car_str_in_expense_type_name_itemization'] = \
        df_before_preprocessing['expense_type_name_itemization_normalized'].apply(check_if_car_in_str)
    df_after_preprocessing['car_str_in_expense_type_name_expense'] = \
        df_before_preprocessing['expense_type_name_expense_normalized'].apply(check_if_car_in_str)

    df_after_preprocessing['hotel_str_in_expense_type_name_itemization'] = \
        df_before_preprocessing['expense_category_itemization_normalized'].apply(check_if_hotel_lodging_in_str)
    df_after_preprocessing['hotel_str_in_expense_type_name_expense'] = \
        df_before_preprocessing['expense_category_expense_normalized'].apply(check_if_hotel_lodging_in_str)

    df_after_preprocessing['expense_type_name_in_flights_stopwords_itemization'] = \
        df_before_preprocessing['expense_type_name_itemization_normalized'].apply(
            lambda x: check_membership_if_in_stopwords(x, STOP_WORDS_FOR_FLIGHTS_EXPENSE_TYPE_NAME))
    df_after_preprocessing['expense_type_name_in_flights_stopwords_expense'] = \
        df_before_preprocessing['expense_type_name_expense_normalized'].apply(
            lambda x: check_membership_if_in_stopwords(x, STOP_WORDS_FOR_FLIGHTS_EXPENSE_TYPE_NAME))

    df_after_preprocessing['expense_type_name_in_rail_stopwords_itemization'] = \
        df_before_preprocessing['expense_type_name_itemization_normalized'].apply(
            lambda x: check_membership_if_in_stopwords(x, STOP_WORDS_FOR_RAIL_EXPENSE_TYPE_NAME))
    df_after_preprocessing['expense_type_name_in_rail_stopwords_expense'] = \
        df_before_preprocessing['expense_type_name_expense_normalized'].apply(
            lambda x: check_membership_if_in_stopwords(x, STOP_WORDS_FOR_RAIL_EXPENSE_TYPE_NAME))

    # from anlaysis19_flights
    budget_check_list = [
        'hotel',
        'flight',
        'car',
        'rail'
    ]

    make_features_which_checks_if_str_equals('expense_type_name_itemization', budget_check_list,
                                             df_before_preprocessing, df_after_preprocessing)

    # from anlaysis19_flights
    expense_check_list = [
        'other',
        'hotel',
        'taxi',
        'flight',
        'car',
        'fees_and_misc',
        'rail',
        'bus',
        'train'
    ]

    make_features_which_checks_if_str_equals('expense_type_name_expense', expense_check_list, df_before_preprocessing,
                                             df_after_preprocessing)
    make_features_which_checks_if_str_equals('expense_type_name_itemization', expense_check_list,
                                             df_before_preprocessing, df_after_preprocessing)

    make_features_which_checks_if_str_equals('expense_category_expense', expense_check_list, df_before_preprocessing,
                                             df_after_preprocessing)
    make_features_which_checks_if_str_equals('expense_category_itemization', expense_check_list,
                                             df_before_preprocessing, df_after_preprocessing)

    df_after_preprocessing['airbnb_in_vendor_name_expense'] = df_before_preprocessing[
        'vendor_name_expense_normalized'].apply(check_if_airbnb_in_str)
    df_after_preprocessing['omega_world_travel_in_vendor_name_expense'] = df_before_preprocessing[
        'vendor_name_expense_normalized'].apply(check_if_omega_world_travel_in_str)

    # matching vendorname
    me = sm.MongeElkan(sim_func=sm.JaroWinkler().get_raw_score)
    df_after_preprocessing['mongeelkan_jaro_wink'] = df_before_preprocessing.apply(lambda row:
                                                                                   max(
                                                                                       me.get_raw_score(row[
                                                                                                            'vendor_name_expense_normalized'].split(),
                                                                                                        row[
                                                                                                            'purchase_vendor_receipts_normalized'].split()), \
                                                                                       me.get_raw_score(row[
                                                                                                            'travel_vendor_receipts_normalized'].split(),
                                                                                                        row[
                                                                                                            'vendor_name_expense_normalized'].split())
                                                                                   )
                                                                                   , axis=1)


def check_membership_if_in_stopwords(normalized_str, stop_words):
    for word in list(stop_words):
        if word in normalized_str:
            return True
    return False


def check_if_tax_in_str(normalized_str):
    if 'taxi' in normalized_str:
        return False

    return 'tax' in normalized_str


def check_if_car_in_str(normalized_str):
    if 'car' in normalized_str:
        return True

    return False


def check_if_omega_world_travel_in_str(normalized_str):
    if 'omega world travel' in normalized_str:
        return True

    return False


def check_if_hotel_lodging_in_str(normalized_str):
    if 'lodg' in normalized_str or 'hotel' in normalized_str:
        return True

    return False


def make_features_which_checks_if_str_equals(field_name, check_list, df_before_preprocessing, df_after_preprocessing):
    check_if_strs_are_equal = lambda in_str, exp_str: 1.0 if in_str == exp_str else 0.0

    for type_name in check_list:
        check_if_strs_are_equal_wrapper = lambda x: check_if_strs_are_equal(x.lower(), type_name)
        df_after_preprocessing[field_name + '_' + type_name] = df_before_preprocessing[field_name].apply(
            check_if_strs_are_equal_wrapper)

    return None


def check_if_airbnb_in_str(normalized_str):
    if 'airbnb' in normalized_str or 'air bnb' in normalized_str:
        return True

    return False

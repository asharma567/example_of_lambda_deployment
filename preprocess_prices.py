def make_all_price_related_features_inplace(df_before_preprocessing, df_after_preprocessing):
    df_after_preprocessing['actual_cost_budget'] = df_before_preprocessing['actual_cost_budget']
    df_after_preprocessing['budget_price_budget'] = df_before_preprocessing['budget_price_budget']
    df_after_preprocessing['actual_cost_budget_per_day'] = df_before_preprocessing['actual_cost_budget'] / \
                                                           df_after_preprocessing['number_of_days_of_trip']
    df_after_preprocessing['budget_price_budget_per_day'] = df_before_preprocessing['budget_price_budget'] / \
                                                            df_after_preprocessing['number_of_days_of_trip']

    df_after_preprocessing['pct_of_budget_price'] = \
        df_before_preprocessing['expensed_amount_itemization'] / df_before_preprocessing['budget_price_budget']

    df_before_preprocessing['actual_cost_budget'] = df_before_preprocessing['actual_cost_budget'].apply(
        lambda x: 0.01 if float(x) == 0.0 else x)

    df_after_preprocessing['pct_of_actual_cost_budget'] = \
        df_before_preprocessing['expensed_amount_itemization'] / df_before_preprocessing['actual_cost_budget']

    df_after_preprocessing['pct_of_budget_price_per_day'] = \
        df_before_preprocessing['expensed_amount_itemization'] / df_after_preprocessing['budget_price_budget_per_day']

    df_after_preprocessing['pct_of_actual_cost_per_day'] = \
        df_before_preprocessing['expensed_amount_itemization'] / df_after_preprocessing['actual_cost_budget_per_day']

    return None

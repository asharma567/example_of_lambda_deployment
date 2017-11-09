from filtered_payload import FilteredPayload


class FlattenedDataPoints(object):
    def __init__(self, json_payload):
        self._filtered_json_payload = FilteredPayload(json_payload).get()

    def all(self):
        flattened_data_points = self._flattened_json_payload()
        return flattened_data_points

    def _flattened_json_payload(self):
        flattened_data_points = []

        for budget in self._filtered_json_payload['budgets']:
            for itemization in self._filtered_json_payload['all_user_expense_lineitems']:
                data_point = {}
                data_point.update(budget)
                data_point.update(itemization)
                flattened_data_points.append(data_point)

        return flattened_data_points

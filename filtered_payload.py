class FilteredPayload(object):
    def __init__(self, json_payload):
        self._json_payload = json_payload

    def get(self):
        self._json_payload['budgets'] = [budget for budget in self._json_payload.get('budgets')
                                         if None not in budget.values()]
        self._json_payload['all_user_expense_lineitems'] = \
            [itemization for itemization in self._json_payload.get('all_user_expense_lineitems')
             if None not in itemization.values()]
        return self._json_payload

import ctypes
import json
import os

from flattened_data_points import FlattenedDataPoints
from predict import predict_if_budget_matches_itemization

for d, _, files in os.walk('lib'):
    for f in files:
        if f.endswith('.a'):
            continue

        ctypes.cdll.LoadLibrary(os.path.join(d, f))
        print("success", str(d), str(f))


def handler(event, context):
    print('Start matching expenses to budgets')
    print('Received the following input:\n{}'.format(json.dumps(event)))

    flattened_data_points = FlattenedDataPoints(event).all()
    scores = score_all_data_points(flattened_data_points)

    print('Scores:\n{}'.format(json.dumps(scores)))
    print('Finished')
    return scores


def score_all_data_points(flattened_data_points):
    final_scores = []

    for data_point in flattened_data_points:
        score = predict_if_budget_matches_itemization(data_point)
        row_value = dict(budget_id=data_point['budget_id'], itemization_id=data_point['itemization_id'], score=score)
        final_scores.append(row_value)

    return final_scores

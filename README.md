# My Matching Model v3.0

A standalone function that returns a percent match for Itemizations to Budgets. It is hosted through
[Amazon Lambda](https://aws.amazon.com/lambda/).

### Deployment

To create the deployment package, run the following command while in the root directory of the project:

```bash
$ ./build
```

This creates a new file called `deploy.zip` in the current directory, which can then be uploaded to Amazon Lambda.

### Executing Locally

While in the root directory of the project with Docker running, run the command:

```bash
$ docker run -v "$PWD":/var/task lambci/lambda:python2.7 main.handler JSON_PAYLOAD
```

Replace `JSON_PAYLOAD` with a JSON formatted payload sent as a string. For example:

```bash
$ docker run -v "$PWD":/var/task lambci/lambda:python2.7 main.handler '{"budgets": [{"budget_price_budget": "140.0", "travel_vendor_receipts": "Southwest Airlines", "purchase_vendor_receipts": "Southwest Airlines", "budget_id": "309366", "start_datetime_trips": "2017-04-18 04:00:00", "generated_at_budget": "2017-04-08 14:55:39", "budget_type_budget": "flight", "actual_cost_budget": "131.98", "end_datetime_trips": "2017-04-19 04:00:00"}], "all_user_expense_lineitems": [{"expensed_amount_itemization": "24.0", "expense_type_name_itemization": "Taxi", "transaction_date_itemization": "2017-04-25 00:00:00", "itemization_id": "4659496", "expense_category_itemization": "taxi", "vendor_name_expense": "taxi", "expense_type_name_expense": "Taxi", "expense_category_expense": "taxi"}]}'
```

Alternatively, you can use a tool like [Postman](https://www.getpostman.com/) to send your JSON payload to the following address:

https://j4e8yp6cdi.execute-api.us-west-2.amazonaws.com/test/matcher/

#### Request Format

Request body:

```json
{
    "item_1": [
        {
            "price": "140.0",
            "travel_vendor": "Southwest Airlines",
            "purchase_vendor": "Southwest Airlines",
            "id": "309366",
            "type": "flight",
            "generated_at": "2017-04-08 14:55:39",
            "start_datetime": "2017-04-18 04:00:00",
            "actual_cost_budget": "131.98",
            "end_datetime": "2017-04-19 04:00:00"
        }
    ],
    "item_2": [
        {
            "expensed_amount_itemization": "24.0",
            "expense_type_name_itemization": "Taxi",
            "transaction_date_itemization": "2017-04-25 00:00:00",
            "itemization_id": "4659496",
            "expense_category_itemization": "taxi",
            "vendor_name_expense": "taxi",
            "expense_type_name_expense": "Taxi",
            "expense_category_expense": "taxi"
        }
    ]
}
```

The response should look like the following:

```json
[
    {
        "score": 0,
        "item_id1": "309366",
        "item_id2": "4659496"
    }
]
```# example_of_lambda_deployment

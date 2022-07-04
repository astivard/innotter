from core.models.database import table


def init_new_user_statistics(body: dict) -> None:
    table.put_item(
        Item={
            "user_id": body["id"],
            "statistics": {
                "pages": 0,
                "posts": 0,
                "likes": 0,
                "subscribers": 0,
            },
        }
    )


def update_user_statistics(body: dict) -> None:
    is_increase = True if body["method"] == "add" else False
    follow_requests_number = body["requests"] if body.get("many") else 1
    value = body['value']

    table.update_item(
        Key={
            "user_id": body["user_id"],
        },
        UpdateExpression=f"SET statistics.{value} = statistics.{value} + :value",
        ExpressionAttributeValues={":value": follow_requests_number if is_increase else -1},
    )


def get_user_statistics(user_id: int) -> dict:
    response = table.get_item(
        Key={
            "user_id": user_id,
        }
    )
    return response["Item"]


methods_dict = {
    "new_user": init_new_user_statistics,
    "add": update_user_statistics,
    "delete": update_user_statistics
}

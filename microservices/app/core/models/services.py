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


def update_pages_number(body: dict) -> None:
    increase = True if body["method"] == "add_page" else False
    _update_some_value(body=body, value="pages", increase=increase)


def update_posts_number(body: dict):
    increase = True if body["method"] == "add_post" else False
    _update_some_value(body=body, value="posts", increase=increase)


def update_likes_number(body: dict):
    increase = True if body["method"] == "add_like" else False
    _update_some_value(body=body, value="likes", increase=increase)


def update_subscribers_number(body: dict):
    increase = True if body["method"] in ("add_subscriber", "add_many_subscribers") else False
    _update_some_value(body=body, value="subscribers", increase=increase)


def _update_some_value(body: dict, value: str, increase: bool) -> None:
    follow_requests_number = body["requests"] if body.get("many") else 1
    table.update_item(
        Key={
            "user_id": body["user_id"],
        },
        UpdateExpression=f"SET statistics.{value} = statistics.{value} + :value",
        ExpressionAttributeValues={":value": follow_requests_number if increase else -1},
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
    "add_page": update_pages_number,
    "delete_page": update_pages_number,
    "add_post": update_posts_number,
    "delete_post": update_posts_number,
    "add_like": update_likes_number,
    "delete_like": update_likes_number,
    "add_subscriber": update_subscribers_number,
    "delete_subscriber": update_subscribers_number,
    "add_many_subscribers": update_subscribers_number,
}

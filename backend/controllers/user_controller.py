import json
from http import HTTPStatus
from backend.services.user_service import UserService

service = UserService()

def create_user_handler(body: bytes):
    data = json.loads(body.decode("utf-8"))
    try:
        user_id = service.create_user(
            username=data["username"],
            email=data["email"],
            password=data["password"]
        )
        return HTTPStatus.CREATED, {"id": user_id}
    except (KeyError, ValueError) as e:
        return HTTPStatus.BAD_REQUEST, {"error": str(e)}

def get_user_handler(user_id: int):
    user = service.get_user(user_id)
    if not user:
        return HTTPStatus.NOT_FOUND, {"error": "User not found"}
    # transform User em dict
    return HTTPStatus.OK, {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at.isoformat(),
        "updated_at": user.updated_at.isoformat()
    }

def update_user_handler(user_id: int, body: bytes):
    data = json.loads(body.decode("utf-8"))
    success = service.update_user(
        user_id,
        username=data.get("username"),
        email=data.get("email"),
        password=data.get("password")
    )
    if not success:
        return HTTPStatus.NOT_FOUND, {"error": "User not found or no changes"}
    return HTTPStatus.OK, {"message": "User updated"}

def delete_user_handler(user_id: int):
    success = service.delete_user(user_id)
    if not success:
        return HTTPStatus.NOT_FOUND, {"error": "User not found"}
    return HTTPStatus.NO_CONTENT, None  # sem corpo

def login_handler(body: bytes):
    data = json.loads(body.decode("utf-8"))
    ok = service.authenticate(
        username=data.get("username", ""),
        password=data.get("password", "")
    )
    if not ok:
        return HTTPStatus.UNAUTHORIZED, {"error": "Invalid credentials"}
    return HTTPStatus.OK, {"message": "Authenticated"}
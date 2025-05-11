import json
from http import HTTPStatus
from backend.services.resource_service import ResourceService

service = ResourceService()

def create_resource_handler(body: bytes):
    data = json.loads(body.decode("utf-8"))
    try:
        res_id = service.create_resource(
            name=data["name"],
            description=data.get("description", ""),
            type=data.get("type", ""),
            details=data.get("details", {})
        )
        return HTTPStatus.CREATED, {"id": res_id}
    except KeyError as e:
        return HTTPStatus.BAD_REQUEST, {"error": f"Missing field {e}"}

def list_resources_handler():
    lst = service.list_resources()
    result = []
    for r in lst:
        result.append({
            "id":          r.id,
            "name":        r.name,
            "description": r.description,
            "type":        r.type,
            "details":     r.details
        })
    return HTTPStatus.OK, result

def get_resource_handler(res_id: int):
    r = service.get_resource(res_id)
    if not r:
        return HTTPStatus.NOT_FOUND, {"error": "Resource not found"}
    return HTTPStatus.OK, {
        "id":          r.id,
        "name":        r.name,
        "description": r.description,
        "type":        r.type,
        "details":     r.details
    }

def delete_resource_handler(res_id: int):
    ok = service.delete_resource(res_id)
    if not ok:
        return HTTPStatus.NOT_FOUND, {"error": "Not found"}
    return HTTPStatus.NO_CONTENT, None

# Opcionalmente, se quiser PUT /resources/:id
def update_resource_handler(res_id: int, body: bytes):
    data = json.loads(body.decode("utf-8"))
    ok = service.update_resource(
        res_id,
        name=data.get("name"),
        description=data.get("description"),
        type=data.get("type"),
        details=data.get("details")
    )
    if not ok:
        return HTTPStatus.NOT_FOUND, {"error": "Not found or no changes"}
    return HTTPStatus.OK, {"message": "Resource updated"}

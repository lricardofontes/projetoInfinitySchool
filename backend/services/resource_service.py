from backend.models.resource import Resource
from backend.repository.resource_repository import ResourceRepository

class ResourceService:
    def __init__(self):
        self.repo = ResourceRepository()

    def create_resource(self, name: str, description: str, type: str, details: dict) -> int:
        r = Resource(name=name, description=description, type=type, details=details)
        return self.repo.create(r)

    def list_resources(self) -> list[Resource]:
        return self.repo.list_all()

    def get_resource(self, res_id: int) -> Resource | None:
        return self.repo.get_by_id(res_id)

    def update_resource(self, res_id: int, **fields) -> bool:
        r = self.repo.get_by_id(res_id)
        if not r:
            return False
        for k, v in fields.items():
            if v is not None and hasattr(r, k):
                setattr(r, k, v)
        return self.repo.update(r)

    def delete_resource(self, res_id: int) -> bool:
        return self.repo.delete(res_id)

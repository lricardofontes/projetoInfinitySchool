import pytest
from backend.services.resource_service import ResourceService
from backend.models.resource import Resource


service = ResourceService()

@pytest.fixture
def setup_resource():
    """Configura um recurso temporário para os testes."""
    res_id = service.create_resource("Recurso Teste", "Descrição do recurso", "Tipo A", {})
    yield res_id
    service.delete_resource(res_id)  # Limpa após o teste

def test_create_resource():
    res_id = service.create_resource("Recurso 1", "Descrição 1", "Tipo A", {})
    assert res_id is not None

def test_list_resources():
    service.create_resource("Recurso 2", "Descrição 2", "Tipo B", {})
    resources = service.list_resources()
    assert len(resources) > 0

def test_get_resource(setup_resource):
    res = service.get_resource(setup_resource)
    assert res is not None
    assert res.name == "Recurso Teste"

def test_update_resource(setup_resource):
    updated = service.update_resource(setup_resource, name="Recurso Atualizado")
    assert updated is True
    res = service.get_resource(setup_resource)
    assert res.name == "Recurso Atualizado"

def test_delete_resource(setup_resource):
    deleted = service.delete_resource(setup_resource)
    assert deleted is True
    res = service.get_resource(setup_resource)
    assert res is None

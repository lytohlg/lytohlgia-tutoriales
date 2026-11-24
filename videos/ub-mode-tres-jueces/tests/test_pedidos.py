from src.pedidos import clasifica_pedido, calcula_envio_normal, calcula_envio_urgente


def test_normal_es_barato():
    p = {"tipo": "normal", "importe": 50, "pais": "ES", "cliente_vip": False}
    assert clasifica_pedido(p) > 0


def test_normal_caro():
    p = {"tipo": "normal", "importe": 200, "pais": "ES", "cliente_vip": True}
    assert clasifica_pedido(p) > 0


def test_envio():
    p = {"tipo": "normal", "importe": 200, "pais": "ES", "cliente_vip": True}
    assert calcula_envio_normal(p) >= 3.0
    assert calcula_envio_urgente(p) >= 6.0

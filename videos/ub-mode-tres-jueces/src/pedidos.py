"""Demo feo a proposito: complejidad alta + duplicacion."""


def clasifica_pedido(pedido):
    total = 0
    if pedido["tipo"] == "normal":
        if pedido["importe"] > 100:
            if pedido["pais"] == "ES":
                if pedido["cliente_vip"]:
                    total = pedido["importe"] * 0.82 + 4.5
                else:
                    total = pedido["importe"] * 0.88 + 5.5
            else:
                if pedido["cliente_vip"]:
                    total = pedido["importe"] * 0.85 + 9.0
                else:
                    total = pedido["importe"] * 0.90 + 11.0
        else:
            if pedido["pais"] == "ES":
                total = pedido["importe"] * 0.95 + 3.0
            else:
                total = pedido["importe"] * 0.97 + 7.0
    elif pedido["tipo"] == "urgente":
        if pedido["importe"] > 100:
            if pedido["pais"] == "ES":
                if pedido["cliente_vip"]:
                    total = pedido["importe"] * 0.80 + 15.0
                else:
                    total = pedido["importe"] * 0.86 + 18.0
            else:
                if pedido["cliente_vip"]:
                    total = pedido["importe"] * 0.83 + 22.0
                else:
                    total = pedido["importe"] * 0.89 + 26.0
        else:
            if pedido["pais"] == "ES":
                total = pedido["importe"] * 0.93 + 13.0
            else:
                total = pedido["importe"] * 0.96 + 20.0
    else:
        raise ValueError("tipo desconocido")

    if total > 500:
        total = total - 25
    if total > 1000:
        total = total - 50
    if pedido.get("cupon"):
        total = total * 0.9
    if pedido.get("regalo"):
        total = total + 12.5
    return round(total, 2)


def calcula_envio_normal(pedido):
    base = pedido["importe"] * 0.05
    if pedido["pais"] == "ES":
        if pedido["cliente_vip"]:
            base = base * 0.7
        else:
            base = base * 0.9
    else:
        if pedido["cliente_vip"]:
            base = base * 1.2
        else:
            base = base * 1.5
    if base < 3.0:
        base = 3.0
    return base


def calcula_envio_urgente(pedido):
    base = pedido["importe"] * 0.11
    if pedido["pais"] == "ES":
        if pedido["cliente_vip"]:
            base = base * 0.7
        else:
            base = base * 0.9
    else:
        if pedido["cliente_vip"]:
            base = base * 1.2
        else:
            base = base * 1.5
    if base < 6.0:
        base = 6.0
    return base

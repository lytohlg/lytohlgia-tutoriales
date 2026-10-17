-- Excepciones: lo que se queda atrás y nadie mira.
-- Pedidos con la fecha de entrega pasada y sin servir + facturas vencidas sin cobrar.
-- La referencia va como TEXTO en las dos partes: en un UNION ALL las dos columnas
-- tienen que ser del mismo tipo (un id de pedido es número y el de factura no, y
-- SQL Explorer resume las columnas numéricas: si se mezclan, la consulta falla).
SELECT CAST(p.id AS TEXT)  AS referencia,
       p.cliente        AS cliente,
       p.fecha_entrega   AS vence,
       p.importe        AS importe,
       'pedido sin servir' AS excepcion
  FROM pedidos p
 WHERE p.estado = 'pendiente'
   AND p.fecha_entrega < date('now')
 UNION ALL
SELECT f.id,
       f.cliente,
       f.vencimiento,
       f.importe,
       'factura vencida sin cobrar'
  FROM facturas f
 WHERE f.cobrada = 0
   AND f.vencimiento < date('now')
 ORDER BY 3

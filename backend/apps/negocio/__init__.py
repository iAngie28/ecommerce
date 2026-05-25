"""
apps/negocio/__init__.py

Punto de entrada al módulo negocio dentro de la carpeta apps/.
Los sub-módulos aquí re-exportan desde la Django app 'app_negocio'.

Sub-módulos:
  catalogo/        → Producto, Categoria, Promocion + servicios de catálogo
  ordenes/         → Carrito, CarritoItem, Pedido + servicios de órdenes
  billing/         → Factura, DetalleFactura, TipoPago + Stripe + factura_service
  notificaciones/  → Notificacion + notification_service + signals
"""

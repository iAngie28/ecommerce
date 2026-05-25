"""
apps/customers/__init__.py

Punto de entrada al módulo customers dentro de la carpeta apps/.
Los sub-módulos aquí son organizacionales y re-exportan desde la
Django app registrada en INSTALLED_APPS como 'customers'.

Sub-módulos:
  tenants/      → Client, Domain, Plan, Suscripcion + servicios de tenant
  users/        → Usuario, Rol, Permiso, DeviceToken + auth + servicios de usuario
  clientes/     → Cliente + servicios de cliente
  audit/        → Bitacora, RespaldoSistema + servicios de auditoría
"""

# Reestructuración de Planes de Suscripción y Permisos

El objetivo de este plan es reestructurar la lógica de negocio de los planes de suscripción para que existan 4 niveles claramente definidos (Gratis, Standard, Gold, Profesional), cada uno con un balance progresivo de funcionalidades (permisos) y limitaciones (usuarios, productos, facturación). Además, bloquearemos la interfaz en el frontend para aquellos usuarios/tiendas que no posean el permiso necesario.

## Open Questions
> [!IMPORTANT]
> **Preguntas para el usuario:**
> 1. Para el límite de facturación mensual: ¿Prefieres que se bloquee la creación de **nuevos pedidos** cuando la tienda supere el monto, o simplemente se muestre un aviso en el frontend? (directamente en el backend le tira una especie de error y el frontend lo muestre asi para validar todo en el backend)
> 2. En el plan gratuito, he limitado la cantidad de usuarios a 1 (solo el dueño), ¿te parece bien o prefieres que sean 2? (1 dueño y 1 usuario mas para manejar la tienda)
> 3. ¿El plan Gold tiene un límite de $50,000 en facturación, o prefieres otro monto? (mucho mas, aunque no se si sea necesario ese limite)

## Proposed Changes

### Backend: Semilla de Datos y Roles

#### [MODIFY] [seed_db.py](file:///c:/Users/ldgd2/OneDrive/Documentos/Proyectos_lider/python/ecommerce/backend/scripts_utiles/seed_db.py)
- **Cambio**: Modificar la creación de los `planes_config` para incluir los 4 niveles:
  - **Gratis**: $0/mes, 1 usuario, 50 productos, límite $1,000/mes. Permisos básicos esenciales (sin roles, sin reportes).
  - **Standard**: $29/mes, 5 usuarios, 500 productos, límite $10,000/mes. Incluye `REP_ESTATICO`, `GESTIONAR_USUARIOS`.
  - **Gold**: $69/mes, 15 usuarios, 5000 productos, límite $50,000/mes. Incluye `EXPORTAR_CLIENTES`, `CONFIGURACION_PAGOS`, `VER_DASHBOARD_AVANZADO`.
  - **Profesional**: $99/mes, ilimitado (0) usuarios, ilimitado (0) productos, límite `None` facturación. Incluye `REP_DINAMICO`, `REP_AUDIO`.

#### [MODIFY] [seed_permisos.py](file:///c:/Users/ldgd2/OneDrive/Documentos/Proyectos_lider/python/ecommerce/backend/apps/gestionDeUsuarioySeguridad/cu5_gestionar_permisos/management/commands/seed_permisos.py)
- **Cambio**: Sincronizar las modificaciones de los permisos (`es_basico=False` para los que solo entran desde Standard en adelante).
- **Cambio**: Actualizar la asignación de permisos a los planes en la base de datos (reparación de planes).

---

### Backend: Validación de Límites en la API

#### [MODIFY] [apps/gestionDeUsuarioySeguridad/cu3_gestion_de_usuario/api/views.py](file:///c:/Users/ldgd2/OneDrive/Documentos/Proyectos_lider/python/ecommerce/backend/apps/gestionDeUsuarioySeguridad/cu3_gestion_de_usuario/api/views.py)
- **Cambio**: Añadir validación en `perform_create` para verificar que la tienda no exceda el `max_usuarios` definido en su plan activo (si no es ilimitado).

#### [MODIFY] [apps/gestionDeVentasYFacturacion/cu13_gestionar_estado_de_pedido/api/views.py](file:///c:/Users/ldgd2/OneDrive/Documentos/Proyectos_lider/python/ecommerce/backend/apps/gestionDeVentasYFacturacion/cu13_gestionar_estado_de_pedido/api/views.py)
- **Cambio**: Al crear un nuevo pedido, calcular el total facturado en el mes actual y verificar si supera el `facturacion_max` del plan. Si lo supera, lanzar un error `ValidationError` indicando que deben mejorar su plan.

---

### Frontend: Bloqueo de Rutas e Interfaz

#### [MODIFY] [frontend/src/core/router/routes.config.jsx](file:///c:/Users/ldgd2/OneDrive/Documentos/Proyectos_lider/python/ecommerce/frontend/src/core/router/routes.config.jsx)
- **Cambio**: Añadir una nueva propiedad `permissions: ['CODIGO_PERMISO']` en la configuración de las rutas.
- **Cambio**: Modificar la función `getSidebarGroups` para que además de chequear roles, oculte las opciones del menú lateral si el usuario no tiene los `permisos_efectivos` requeridos.

#### [MODIFY] [Archivos de Vistas Específicas]
- Ocultaremos o deshabilitaremos botones específicos dentro de las vistas (ej. Botón "Exportar a Excel" en la vista de clientes) mediante un check de permisos (`user.permisos_efectivos.includes('EXPORTAR_CLIENTES')`).

## Verification Plan
### Automated Tests
- Se correrá la semilla de la base de datos `venv\Scripts\python manage.py runscript seed_db` para verificar que los planes se creen correctamente con sus respectivos límites.
### Manual Verification
- Iniciar sesión con un usuario de tienda en plan Gratis y verificar que:
  - No puede crear más de 50 productos.
  - No puede crear más de 1 usuario extra.
  - No ve el botón de "Reportes Dinámicos" en el sidebar.

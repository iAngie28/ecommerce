# 🔄 Diagramas de Flujo: Mixins en Acción

Ver el archivo DIAGRAMAS_MIXINS_FLUJOS.md en la carpeta raíz para los diagramas completos con 8 escenarios detallados.

## 📋 Contenido

Este documento incluye diagramas ASCII para:

1. ✅ Flujo de Creación: POST /api/productos/
2. ✅ Flujo de Actualización: PUT /api/productos/42/
3. ✅ Flujo de Eliminación: DELETE /api/productos/42/
4. ✅ Flujo de Lectura: GET /api/productos/
5. ✅ Manejo de Errores: Validación Fallida
6. ✅ Caso Especial: Usuario Desactivado
7. ✅ Caso Especial: Multi-Tenant Separation (Seguridad)
8. ✅ Comparativa Visual: Mixins vs Sin Mixins

---

## 🎯 Flujo General Simplificado

```
HTTP Request (POST /api/productos/)
          ↓
ProductoViewSet.perform_create()
          ↓
ValidacionesMixin.perform_create()
├─ ¿Usuario activo? → SÍ ✓
├─ ¿Tiene permisos? → SÍ ✓
└─ super()
          ↓
AuditoriaMixin.perform_create()
├─ serializer.save() → INSERT en BD ✓
├─ BitacoraService.registrar_accion() → Auditoría ✓
└─ super()
          ↓
MultiTenantMixin.get_queryset()
├─ ¿Schema es 'public'? → NO
└─ Retorna datos del tenant actual ✓
          ↓
HTTP Response 201 CREATED
├─ Datos guardados ✅
└─ Auditoría registrada ✅
```

---

## 📊 Tabla: Orden de Ejecución

| Paso | Mixin | Acción | Resultado |
|------|-------|--------|-----------|
| 1️⃣ | ValidacionesMixin | Valida usuario | ✅ o ❌ |
| 2️⃣ | AuditoriaMixin | Guarda + Audita | ✅ |
| 3️⃣ | MultiTenantMixin | Garantiza aislamiento | ✅ |
| 4️⃣ | ModelViewSet | Responde | 201/400/403 |

---

## 💡 Clave: Herencia en Python (MRO)

Los Mixins se ejecutan en orden de **Method Resolution Order**:

```python
class CRUDGenericoMixin(
    ValidacionesMixin,      # 1️⃣ Se ejecuta primero
    AuditoriaMixin,         # 2️⃣ Se ejecuta segundo
    MultiTenantMixin        # 3️⃣ Se ejecuta tercero
):
    pass
```

**Ventaja:** Las validaciones se ejecutan ANTES de guardar datos

---

**Para ver todos los diagramas detallados, abre:**
`DIAGRAMAS_MIXINS_FLUJOS.md` en la raíz del proyecto

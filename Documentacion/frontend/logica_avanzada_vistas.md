# Guia de Logica Avanzada en Vistas (Parte 2)

Este documento complementa la guia basica de vistas, enfocandose en como inyectar logica interactiva en sus interfaces. Aqui abordaremos el manejo de estado, interacciones asincronas, confirmacion de acciones destructivas y el aprovechamiento total del ecosistema de componentes.

Continuaremos interactuando con el modulo `InventarioView`.

---

## 1. Separacion de Preocupaciones: UI vs Negocio

Una vista compleja rapidamente puede desordenarse si amontonamos logica de red, marcadores de estado y marcado visual.
La recomendacion es subdividir bloques densos en subcomponentes ubicados dentro del mismo archivo, o abstraerlos si son sumamente grandes.

Por ejemplo, consideremos el escenario donde en la vista de inventario necesitamos anadir logica de creacion/edicion mediante un Modal (Drawer) y confirmaciones de eliminacion.

### Componentes Internos de Soporte

Es preferible definir funciones retornables modulares en el mismo archivo para fragmentos de renderizacion.

```javascript
/* src/modules/inventario/views/InventarioView.jsx */

// Importaciones
import { useState, useEffect, useCallback } from 'react';
import { Plus, Trash2, Pencil } from 'lucide-react';
import AppView from 'shared/widgets/AppView/AppView';
import DataTable from 'shared/widgets/DataTable/DataTable';
import { Button, Input, Alert } from 'shared/components';
import { inventarioApi } from '../services/inventarioApi';
import styles from './InventarioView.module.css';

// -------------------------------------------------------------
// Subcomponente 1: Drawer (Panel de Edicion)
// Aisla todo el formulario en su propia logica local.
// -------------------------------------------------------------
function EditorProductoDrawer({ open, producto, onClose, onSuccess }) {
  const isEditing = !!producto;
  const [form, setForm] = useState({ codigo: '', cantidad: 0 });
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);

  // Re-sincronizar formulario cada vez que se abren los datos
  useEffect(() => {
    if (open) {
      setForm(producto ? { ...producto } : { codigo: '', cantidad: 0 });
      setError(null);
    }
  }, [open, producto]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    
    try {
      if (isEditing) {
        await inventarioApi.actualizar(producto.id, form);
      } else {
        await inventarioApi.crear(form);
      }
      onSuccess(); // Disparar refetch local en la vista principal
      onClose();   // Ocultar modal
    } catch (err) {
      setError("Fallo en red. Intente de nuevo.");
    } finally {
      setSaving(false);
    }
  };

  if (!open) return null;

  return (
    <div className={styles.drawerOverlay}>
      <div className={styles.drawerPanel}>
         <h3>{isEditing ? 'Editar Producto' : 'Nuevo Producto'}</h3>
         {error && <Alert variant="danger">{error}</Alert>}
         <form onSubmit={handleSubmit}>
            <Input 
              label="Codigo SKU" 
              value={form.codigo} 
              onChange={(e) => setForm({...form, codigo: e.target.value})} 
              required 
            />
            <Button type="submit" loading={saving}>Guardar</Button>
         </form>
      </div>
    </div>
  );
}
```

---

## 2. Coordinacion del Estado Raiz (Vista Principal)

El componente exportado por defecto actua como controlador orquestador (Controller). Se enfoca en la carga inicial, variables macro y pasar instrucciones delegadas a los subcomponentes internos que delineamos antes.

```javascript
// -------------------------------------------------------------
// Componente Principal
// -------------------------------------------------------------
export default function InventarioView() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  
  // Estado para la logica de edicion
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [productoSeleccionado, setProductoSeleccionado] = useState(null);
  
  // Estado para alertas y de eliminacion
  const [deleteTarget, setDeleteTarget] = useState(null);
  const [deleting, setDeleting] = useState(false);

  // Abstraccion de la recarga encapsulada (useCallback recomendado)
  const cargar = useCallback(async () => {
    setLoading(true);
    try {
      const res = await inventarioApi.listar();
      setData(res.data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  }, []);

  // Carga inicial
  useEffect(() => { cargar(); }, [cargar]);

  // Manejo de eliminacion con seguridad
  const onConfirmDelete = async (obj) => {
    if (deleteTarget?.id !== obj.id) {
       setDeleteTarget(obj); // Solo muestra la confirmacion
       return;
    }
    setDeleting(true);
    try {
       await inventarioApi.eliminar(obj.id);
       setDeleteTarget(null);
       cargar(); // Recarga la tabla silenciosamente
    } finally {
       setDeleting(false);
    }
  };

  // Definir columnas (usando referencia de las variables de arriba)
  const columns = [
    { key: 'codigo', label: 'Codigo Interno' },
    { 
      key: 'id', 
      label: 'Acciones', 
      align: 'right',
      render: (val, row) => (
        <div style={{ display: 'flex', gap: '8px' }}>
           <Button size="sm" onClick={() => { setProductoSeleccionado(row); setDrawerOpen(true); }}>
              <Pencil size={14}/>
           </Button>
           <Button size="sm" variant="danger" onClick={() => onConfirmDelete(row)}>
              <Trash2 size={14}/>
           </Button>
        </div>
      )
    }
  ];

  return (
    <AppView 
      title="Control de Inventarios"
      actions={
        <Button leftIcon={<Plus size={16}/>} onClick={() => { setProductoSeleccionado(null); setDrawerOpen(true); }}>
          Anadir Producto
        </Button>
      }
    >
      {/* Sistema In-line de proteccion anti-borrado */}
      {deleteTarget && (
         <Alert variant="warning" title="Peticion de Borrado">
           Seguro que desea eliminar {deleteTarget.codigo}? Esta accion es permanente.
           <Button variant="danger" loading={deleting} onClick={() => onConfirmDelete(deleteTarget)}>Confirmar</Button>
           <Button variant="ghost" onClick={() => setDeleteTarget(null)}>Cancelar</Button>
         </Alert>
      )}

      <DataTable 
        columns={columns}
        data={data}
        loading={loading}
        emptyText="No se encontraron registros de inventario actuales."
      />

      {/* Inyeccion del Drawer Desacoplado */}
      <EditorProductoDrawer 
        open={drawerOpen}
        producto={productoSeleccionado}
        onClose={() => setDrawerOpen(false)}
        onSuccess={cargar}
      />
    </AppView>
  );
}
```

---

## 3. Mejores Practicas Implementadas en este Ejercicio

Al transcribir lógicas para crear o refinar una vista dentro de la arquitectura actual, procure ceñirse a estos patrones:

1. **Uso Exclusivo del "Loading state" en Botones**
No bloquee toda la pantalla por solicitudes interactivas (como guardar o procesar). Use en su lugar el parametro `loading={true}` ofrecido de fabrica por nuestro boton generico `shared/components/Button`. Esto mantiene la interfaz interactiva.
2. **Pase la carga al padre**
Como vimos en el flujo `onSuccess={cargar}` del Componente hijo, el cajon de edicion no esta ligado de forma inherente a los datos de la tabla. Al delegarle el refresco a una funcion orquestadora que se encuetra en el padre, se aisla por completo la responsabilidad e inyeccion de dependencias.
3. **El estado "Vacio Base" (Empty State)**
Programe un array de base para sus formularios en base al esquema real: `const [form, setForm] = useState({ campo: '' })`. Cuando los editores laterales cierran o cancelan sus comportamientos, se debe asegurar retornar el estado de estos objetos a sus variables limplias al volver a montar. Evita arrastres residuales en cache en los inputs textuales.
4. **Alerta Selectiva**
No lance PopUps Nativos (`window.alert()` o `alert()`) ante los errores o borrados, implemente la caja de proteccion visual anidada en el `AppView` basandose en el widget encapsulado `shared/components/Alert` para advertencias, fallos y exitos de sistema.

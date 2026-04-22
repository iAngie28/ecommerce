# Guia de Implementacion de Vistas en MiQhatu

Este documento actua como un estandar de desarrollo para la creacion e integracion de nuevas interfaces de usuario en el panel de MiQhatu. La idea detras de este patron es el principio DRY (Don't Repeat Yourself) y la estandarizacion visual.

A continuacion, se explica el flujo paso a paso desde la creacion estructural hasta el despliegue de una nueva funcionalidad.

---

## Fases de Implementacion

### Paso 1: Estructura del Modulo

Antes de escribir codigo reactivo, debemos identificar a que "Modulo de Negocio" pertenece la funcionalidad. Si es una caracteristica autonoma, debemos crear su propio directorio.

Tomemos como ejemplo la implementacion de una vista de **Inventario**:

1. Navega al directorio `/src/modules/`
2. Crea una nueva carpeta representativa, por ejemplo `/inventario`
3. Dentro, inicializa los archivos estructurales base:

```text
src/modules/inventario/
├── views/
│   ├── InventarioView.jsx          # Logica del componente React
│   └── InventarioView.module.css   # Estilos exclusivos de la vista
├── services/
│   └── inventarioApi.js            # Extraccion de llamadas HTTP
└── index.js                        # Barril de exportaciones
```

### Paso 2: Creacion de la Capa de Datos (API Service)

Para mantener los componentes limpios y enfocados en la renderizacion, aislamos el acceso a datos.

#### `services/inventarioApi.js`

```javascript
import api from 'core/services/api';

const BASE_URL = '/inventarios';

export const inventarioApi = {
  listar: (params) => api.get(`${BASE_URL}/`, { params }),
  crear: (data) => api.post(`${BASE_URL}/`, data),
  eliminar: (id) => api.delete(`${BASE_URL}/${id}/`),
};
```

### Paso 3: Diseno Visual de la Vista

El pilar estructural de cualquier vista interna de la plataforma es el componente base `AppView`. Se trata de un *Widget* generico disenado para recibir parametros formales de cabecera y el contenido hijo. 

Tambien apoyaremos la integracion visual utilizando los componentes empaquetados de la carpeta `shared/components/`.

#### `views/InventarioView.jsx`

```javascript
import { useState, useEffect } from 'react';
import { Download } from 'lucide-react'; // Iconografia oficial

// Componentes estandarizados
import AppView from 'shared/widgets/AppView/AppView';
import DataTable from 'shared/widgets/DataTable/DataTable';
import { Button, Badge, Alert } from 'shared/components';

// Logica de red
import { inventarioApi } from '../services/inventarioApi';

// Definicion formal de la tabla
const COLUMNAS = [
  { key: 'codigo', label: 'Codigo Interno' },
  { key: 'cantidad', label: 'Stock', align: 'center' },
  { 
    key: 'estado', 
    label: 'Estado', 
    align: 'center',
    render: (val) => <Badge variant={val ? 'success' : 'danger'}>{val ? 'Activo' : 'Agotado'}</Badge> 
  }
];

export default function InventarioView() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    inventarioApi.listar()
      .then(res => setData(res.data))
      .finally(() => setLoading(false));
  }, []);

  return (
    <AppView 
      title="Control de Inventarios" 
      subtitle="Gestion administrativa en tiempo real"
      actions={
        <Button leftIcon={<Download size={16}/>}>
          Exportar
        </Button>
      }
    >
      <DataTable 
        title="Stock Consolidado"
        columns={COLUMNAS}
        data={data}
        loading={loading}
      />
    </AppView>
  );
}
```

### Paso 4: Exportacion del Modulo (Archivos Barril)

A traves del archivo `index.js`, centralizamos que caracteristicas seran expuestas por el modulo de inventario hacia el resto de la configuracion o proyecto.

#### `index.js`
```javascript
export { default as InventarioView } from './views/InventarioView';
export * from './services/inventarioApi';
```

### Paso 5: Registro del Modulo (Router Integration)

El ecosistema Frontend utiliza un registro estricto en el nucleo para la navegacion. No debes tocar `App.js` ni `AppShell.jsx`. Lo unico requerido es inyectar nuestra vista al registro general de negocio.

Navega hacia `src/core/router/routes.config.jsx` y anade tu objeto de ruta en el array constante `APP_MODULES`.

```javascript
import { InventarioView } from 'modules/inventario';
import { Archive } from 'lucide-react';

export const APP_MODULES = [
  // ...modulos existentes
  {
    id: 'inventario_core',
    path: '/inventario',
    label: 'Inventarios',
    icon: Archive,
    component: InventarioView,
    sidebarGroup: 'negocio',
    protected: true
  }
];
```

## Recursos del Framework Visual

Al extender los archivos `*.module.css`, la arquitectura provee un Design System integrado mediante variables. Los estilos de la aplicacion se unifican y reusar el marco de diseno ahorra horas de mantenimiento visual.

**Lista de variables de consulta (CSS Tokens):**

*   **Superficies:**
    *   `var(--color-bg)`: Fondo base de la aplicacion.
    *   `var(--color-surface)`: Superficie estandar de paneles y cartas.
    *   `var(--color-surface-2)`: Resaltado sutil en paneles o filas.
*   **Acentos y Estados:**
    *   `var(--color-primary)`: Color principal interactivo.
    *   `var(--color-success)`: Aprobaciones o finalizaciones.
    *   `var(--color-danger)`: Fallas, eliminacion o atencion de riesgo.
*   **Tipografia Analitica:**
    *   `var(--text-xs)` al `var(--text-3xl)`.
    *   `var(--color-text)`: Texto central estandar.
    *   `var(--color-text-muted)`: Texto secundario/hints.

Ejemplo util en CSS Modules:
```css
.cardTitle {
    font-size: var(--text-lg);
    font-weight: var(--font-bold);
    color: var(--color-primary-light);
    border-bottom: 1px solid var(--color-border);
    padding-bottom: var(--space-2);
}
```

### Checklist Final para Resguardo de Codigo
- Componentes exportados via `index.js`
- Rutas no absolutas internas del modulo
- Importaciones externas empleando Alias Limpios (`shared/...`, `core/...`)
- Nulos o vacios gestionados antes de render (sin hardcodeo)

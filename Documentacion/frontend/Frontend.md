# 🏗️ Arquitectura Frontend: Plataforma MiQhatu

Este documento detalla la reestructuración arquitectónica del frontend de MiQhatu. La aplicación ha sido rediseñada para ser altamente modular, escalable y mantenible mediante un enfoque asilado de 4 capas y una metodología tipo "Lego".

---

## 🧭 Visión General de la Arquitectura

La aplicación está dividida en 4 capas estrictas, desde la más global (Theme) hasta la más específica (Modules), asegurando la separación de responsabilidades:

| Capa | Responsabilidad | Dependencias permitidas |
|---|---|---|
| 🎨 **Theme** | Fija el Design System global. | *Ninguna* (puramente CSS). |
| ⚙️ **Core** | Infraestructura de la app (Router, Auth, API, Contextos). | *Ninguna* (no puede importar componentes visuales). |
| 🧩 **Shared** | Piezas Lego reutilizables (Botones, Tablas, Layouts). | Solo puede importar de *Theme* y *Core*. |
| 📦 **Modules** | Lógica de negocio y vistas específicas de la aplicación. | Puede importar de *Core* y *Shared*. |

---

## 📁 Estructura de Directorios

La estructura de la carpeta `src/` está diseñada de manera intuitiva y semántica:

```text
src/
├── theme/                 # Design System Central
│   ├── tokens.css         # Variables CSS (colores, espaciados, tipografía)
│   ├── globals.css        # Reseteo CSS y estilos base para html/body
│   ├── typography.css     # Escalas tipográficas
│   └── index.css          # Archivo unificador cargado en el entry-point
│
├── core/                  # Motores e infraestructura
│   ├── router/            # Configuración dinámica de RUTAS y SIDEBAR
│   ├── contexts/          # Estado global (AuthContext, TenantContext)
│   ├── hooks/             # Custom hooks (useAuth, useTenant)
│   ├── services/          # Interceptores de Axios y cliente HTTP
│   └── guards/            # Protección de rutas (PrivateRoute)
│
├── shared/                # Las "Piezas Lego" de UI
│   ├── components/        # Átomos y Moléculas (Button, Input, Badge)
│   ├── widgets/           # Organismos complejos (DataTable, StatCard, AppView)
│   └── layouts/           # Plantillas principales (AppShell, AuthLayout)
│
├── modules/               # Módulos Funcionales (Negocio)
│   ├── auth/              # Login, Recuperación, Registro
│   ├── panel/             # Dashboard Principal
│   ├── productos_catalogo/# CRUD Productos e inventario
│   ├── ventas_facturacion/# Registro de Ventas, Facturación SIN/QR
│   ├── clientes/          # CRM y Segmentación
│   └── reportes/          # Inteligencia de Negocio
│
├── App.js                 # Solo maneja enrutamiento abstracto
└── index.js               # Entry point (Inyecta theme/index.css)
```

---

## 🧩 La Metodología "Lego"

El sistema está diseñado para que crear y añadir nuevas interfaces sea un proceso guiado usando bloques de construcción.

### Componentes y Widgets Base (`shared/`)

Las vistas de negocio deben componerse con widgets reutilizables en lugar de estilos hardcodeados:

| Categoría | Ejemplos | Uso Principal |
|---|---|---|
| **Components** | `<Button>`, `<Input>`, `<Badge>`, `<Spinner>`, `<Alert>` | Para construir formularios y pequeñas interacciones. |
| **Widgets** | `<AppView>`, `<DataTable>`, `<StatCard>` | Bloques estructurales que proveen de consistencia en el "Look & Feel" de todas las pantallas. |
| **Layouts** | `<AppShell>`, `<AuthLayout>` | Define la estructura global de la pantalla (ej. Sidebar + Topbar). |

#### Ejemplo de uso (Construir una vista):
Cualquier nueva página en el sistema debe estar envuelta por el widget `<AppView>`:

```jsx
import AppView from 'shared/widgets/AppView/AppView';
import DataTable from 'shared/widgets/DataTable/DataTable';
import { Button } from 'shared/components';

export default function MiNuevaVista() {
  return (
    <AppView 
      title="Gestión de Facturas" 
      subtitle="Visualiza el historial."
      actions={<Button>Nueva Factura</Button>}
    >
      <DataTable {...configuracion} />
    </AppView>
  );
}
```

---

## 🚀 Guía: Cómo crear y registrar un módulo nuevo

El core cuenta con un **"Lego Registry"** en `core/router/routes.config.jsx`. Agregar una nueva vista y hacer que aparezca mágicamente en el menú lateral y las rutas es extremadamente sencillo.

**Paso 1: Crear la vista en `modules/`**
Crea tu componente en `src/modules/mimodulo/views/MiVista.jsx`. (No olvides tu archivo barril `index.js`).

**Paso 2: Registrar en `routes.config.jsx`**
Abre el archivo de configuración del router y añade tu objeto a `APP_MODULES`:

```javascript
// core/router/routes.config.jsx
import { Mivista } from 'modules/mimodulo';
import { FileText } from 'lucide-react';

export const APP_MODULES = [
  // ... módulos anteriores
  {
    id: 'mis_facturas',
    path: '/facturas',
    label: 'Facturación',
    icon: FileText,           // Icono del Sidebar
    component: Mivista,       // El componente que acabas de crear
    sidebarGroup: 'negocio',  // Donde aparecerá en el menú (opcional)
    protected: true           // Requiere token JWT
  }
];
```
> [!NOTE] 
> **¡Eso es todo!** Automáticamente:
> 1. Webpack y React Router habilitarán la URL `/facturas`.
> 2. `AppShell.jsx` leerá la configuración y dibujará el botón en el menú lateral.
> 3. `PrivateRoute` protegerá el acceso usando los token JWT vigentes.

---

## 🎨 Design System (`theme/`)

El estilo no utiliza IDs hardcodeados ni Bootstrap. Todo depende de variables CSS (Tokens) centralizadas, lo que permite un control en un solo punto y facilita temáticas (ej: Dark Mode).

### Uso en Componentes (CSS Modules)
Todos los componentes usan `CSS Modules` (`Component.module.css`). Esto evita conflictos de clases entre vistas.

Al momento de definir estilos, debes consumir los *CSS Custom Properties*:

| Modificador | Variables CSS | Ejemplo de uso |
|---|---|---|
| **Colores** | `--color-primary`, `--color-surface`, `--color-text` | `background: var(--color-surface-2);` |
| **Espaciados** | `--space-1` hasta `--space-24` | `padding: var(--space-4); gap: var(--space-2);` |
| **Tipografía**| `--text-sm`, `--text-xl`, `--font-bold` | `font-size: var(--text-sm); font-weight: var(--font-semi);` |
| **Bordes**| `--radius-sm`, `--radius-lg` | `border-radius: var(--radius-md);` |
| **Sombras** | `--shadow-sm`, `--shadow-md`, `--shadow-glow` | `box-shadow: var(--shadow-md);` |

---

## 🔗 Aliases Absolutos (Resolución de módulos)
Gracias al `NODE_PATH=src` en `.env` (y a `jsconfig.json`), ya no se usan las tediosas rutas relativas largas como `../../../shared/...`. 

Puedes importar archivos directamente empezando desde el src:

**❌ INCORRECTO:**
```javascript
import { useAuth } from '../../../core/hooks/useAuth';
```
**✅ CORRECTO:**
```javascript
import { useAuth } from 'core/hooks/useAuth';
```

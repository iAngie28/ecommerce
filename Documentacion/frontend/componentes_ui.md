# Guia de Componentes y Widgets (UI Toolkit)

En MiQhatu, el ecosistema de la interfaz de usuario esta construido estrictamente bajo una jerarquia "Lego". Esto asegura un Look & Feel (apariencia) completamente consistente, ademas de centralizar parches y actualizaciones futuras.

Este documento explica las piezas del kit visual, sus variantes y la manera correcta de importarlos dentro de las Vistas de negocio.

---

## 1. Concepto de Invocacion (Archivos Barril)

Todas las "piezas de lego" de interfaz visual estan localizadas de forma central dentro de `src/shared/`.
Para mantener un codigo conciso y limpio en sus vistas, **no debe importar archivos individuales con rutas largas**. En su lugar, utilice el archivo indice (barril) habilitado para destructuracion multiple, aprovechando el alias base configurado en `jsconfig.json`.

**❌ Patrón Incorrecto:**
```javascript
import Button from '../../../shared/components/Button/Button';
import Input from '../../../shared/components/Input/Input';
import AppView from '../../../shared/widgets/AppView/AppView';
```

**✅ Patrón Correcto Exigido:**
```javascript
// Atomos y Moleculas visuales elementales
import { Button, Input, Badge, Spinner, Alert } from 'shared/components';

// Bloques Estructurales avanzados
import { AppView, DataTable, StatCard } from 'shared/widgets';
```

---

## 2. Componentes Base (`shared/components`)

Los componentes basicos son las particulas mas puras y pequenas. 
No manejan estado logico de red; se basan completamente en las `props` introducidas.

### 2.1 Botones (`<Button>`)
Botones enriquecidos para acciones.
*   **Props soportadas:** `variant` (primary | secondary | ghost | danger), `size` (sm | md | lg), `loading` (booleano), `leftIcon`, `rightIcon`.

```javascript
import { Download, RefreshCw } from 'lucide-react';
import { Button } from 'shared/components';

// Secundario con icono a la izquierda
<Button variant="secondary" leftIcon={<RefreshCw size={15}/>}>
  Actualizar
</Button>

// Estado de carga integrado que reescala y deshabilita el boton
<Button variant="primary" loading={isSaving}>
  Guardar Datos
</Button>

// Destructivo (ej: confirmacion de borrado)
<Button variant="danger">Eliminar</Button>
```

### 2.2 Entradas Inteligentes (`<Input>`)
Campos de entrada que encapsulan manejo de etiquetas (labels), ayudas y deteccion de errores integrada en una caja modular.

*   **Props soportadas:** `label`, `error` (mensaje inferior rojo), `hint` (texto guia opcional), `leftIcon`, asi como cualquier soporte nativo standard (type, htmlForm, disabled).

```javascript
import { Search } from 'lucide-react';
import { Input } from 'shared/components';

// Busqueda sencilla con icono inyectado
<Input
  placeholder="Buscar por codigo..."
  leftIcon={<Search size={16} />}
/>

// Formularios robustos con rastreos de error
<Input
  label="Correo Electronico"
  type="email"
  value={form.email}
  error={formError ? "Las credenciales son erroneas" : null}
  hint="Ocuparemos el correo para notificaciones de pagos."
  required
/>
```

### 2.3 Insignias Metricas (`<Badge>`)
Para clasificar entidades y desplegar miniaturas de estatus (roles, estados de pedido, disponibilidades).
*   **Props soportadas:** `variant` (primary | success | warning | danger | default), `dot` (genera un puntito luminocito indicador estatus).

```javascript
import { Badge } from 'shared/components';

<Badge variant="success" dot={true}>Completado</Badge>
<Badge variant="warning">En Progreso</Badge>
<Badge variant="danger" dot={true}>Agotado</Badge>
```

### 2.4 Alertas Contextuales (`<Alert>`)
Cajas interactivas in-line para notificar al usuario sobre eventos sin interrupcion de lectura.
*   **Props soportadas:** `variant` (info | success | warning | danger | default), `title` (titulo principal engrosado).

```javascript
import { Alert } from 'shared/components';

<Alert variant="danger" title="Error en el Servidor">
   No hemos podido conectarnos al motor de inventario, revise su conexion local.
</Alert>

// Tambien permite interaccion (Botones en su interior)
<Alert variant="warning" title="Accion Permanente">
   Esta a punto de purgar 80 clientes. 
   <Button size="sm" variant="danger">Confirmar Purga</Button>
</Alert>
```

---

## 3. Widgets Complejos (`shared/widgets`)

Los Widgets son organismos que consolidan componentes pequenos o realizan orquestacion sofisticada estructural.

### 3.1 AppView (Envoltorio Oficial)
Elemento mandatorio. TODA vista ruteada debe estar encapsulada en un `AppView`. Se cerciora de inyectar coherencia para la estructura principal (Titulo de Pagina, Subtitulo semantico, y Barra de Herramientas derecha).

```javascript
import { AppView } from 'shared/widgets';
import { Button } from 'shared/components';

export default function MisFacturas() {
  return (
    <AppView
      title="Mis Facturas Mensuales"
      subtitle="Examine el historial SIN emitido a sus tenats"
      actions={
         <div style={{ display:'flex', gap: '8px' }}>
            <Button variant="ghost">Reporte</Button>
            <Button>Emitir Manual</Button>
         </div>
      }
    >
      {/* Todo su contenido principal debajo (tablas, graficas, etc) */}
      <div className="mi-cuerpo-de-vista">...</div>
    </AppView>
  );
}
```

### 3.2 Tabla de Datos Asincrona (`<DataTable>`)
El corazon y caballo de carga analitica. Estiliza una tabla y la inyecta de retroalimentacion en su montaje y carga inical.

*   **Props soportadas:** `columns` (Array de definicion), `data` (Array de la API), `loading` (Booleano), `emptyText` (Texto por defecto si no arroja valores).

```javascript
import { DataTable } from 'shared/widgets';
import { Badge, Button } from 'shared/components';

// 1. Configuracion Estructural (Evite meter esto en el render)
const misColumnas = [
  { key: 'codigo', label: 'SKU' },
  { key: 'precio', label: 'Precio', render: (val) => <strong>Bs. {val}</strong> },
  { 
    key: 'id', 
    label: '', // Columna Vacia para acciones
    align: 'right',
    render: (id, rowCompleto) => <Button size="sm">Editar</Button> 
  }
];

// 2. Uso en la renderizacion 
return (
  <DataTable 
    title="Resultados del Ultimo Mes" // Titulo de cabecera visual
    columns={misColumnas}
    data={misRegistrosRecibidosApi}
    loading={estadoLoadingFetch}
    emptyText="No se hallaron coincidencias. Intente un filtro mas flexible."
  />
);
```

### 3.3 Targetas de Estadisticas (`<StatCard>`)
Minicuadros analiticos genericos muy solicitados en Dashboards (Paneles estelares).

*   **Props soportadas:** `title` (Etiqueta textual), `value` (Cifras grandes numericas), `icon` (Render Iconografia Lucide), `trend` (Porcentaje, string comparativo rojo/verde), `trendUp` (booleano).

```javascript
import { StatCard } from 'shared/widgets';
import { ShoppingBag } from 'lucide-react';

<StatCard
  title="Ventas Diarias"
  value="Bs. 4,500.20"
  icon={<ShoppingBag size={24} />}
  trend="+ 12%" // Aumento respecto a ayer
  trendUp={true} // Obliga un pintado verdoso de buena senal
/>
```

---

## 4. Resolucion

Implementar una vista es el arte de importar estas piezas, acomodarlas estructuralmente e inyectar atributos prop como colores booleanos (`loading`), etiquetas (`title`), y manejadores (`onClick`).

Al abstenerse fielmente de estilizar vistas nuevas con CSS particular denso (*Hardcoded styles*) usted asegurara que todo cambio que se pida masivo (como aumentar redondeos, cambiar las fuentes del sistema, variar el rojo oscuro) afecte a miles de nuevas interfaces en tiempo real abaratando el mantenimiento y mitigando el abandono visual.

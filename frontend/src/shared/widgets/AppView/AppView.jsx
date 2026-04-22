import styles from './AppView.module.css';

/**
 * AppView — EL Lego Piece principal para vistas.
 * Envuelve TODA vista de un módulo con encabezado uniforme.
 *
 * Props:
 *   title   : string — título de la página
 *   subtitle: string — descripción corta
 *   actions : ReactNode — botones de acción (ej: "+ Nuevo")
 *   children: ReactNode — contenido de la página
 *
 * Uso básico (crear una nueva vista completa):
 * ─────────────────────────────────────────────
 *   import AppView from 'shared/widgets/AppView/AppView';
 *   import { Button } from 'shared/components';
 *   import { Plus } from 'lucide-react';
 *
 *   export default function MiVista() {
 *     return (
 *       <AppView
 *         title="Mi Módulo"
 *         subtitle="Descripción de lo que hace este módulo"
 *         actions={<Button leftIcon={<Plus size={16}/>}>Nuevo</Button>}
 *       >
 *         {/* tu contenido aquí *\/}
 *       </AppView>
 *     );
 *   }
 * ─────────────────────────────────────────────
 */
const AppView = ({ title, subtitle, actions, children }) => {
  return (
    <div className={styles.view}>
      {(title || actions) && (
        <div className={styles.header}>
          <div className={styles.heading}>
            {title    && <h1 className={styles.title}>{title}</h1>}
            {subtitle && <p  className={styles.subtitle}>{subtitle}</p>}
          </div>
          {actions && <div className={styles.actions}>{actions}</div>}
        </div>
      )}
      <div className={styles.body}>{children}</div>
    </div>
  );
};

export default AppView;

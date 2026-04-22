import { TableProperties } from 'lucide-react';
import Spinner from 'shared/components/Spinner/Spinner';
import styles from './DataTable.module.css';

/**
 * DataTable — Generic table widget
 *
 * Props:
 *   title   : string
 *   columns : Array<{ key, label, render?, align? }>
 *   data    : Array<object>
 *   loading : boolean
 *   emptyText: string
 *   keyField: string — campo a usar como key (default: 'id')
 *   actions : ReactNode — botones en el header de la tabla
 *   footer  : string — texto del footer (ej: "Mostrando 10 de 50")
 *
 * Uso:
 *   const columns = [
 *     { key: 'nombre', label: 'Nombre' },
 *     { key: 'precio', label: 'Precio', render: (val) => `BS. ${val}` },
 *     { key: 'stock',  label: 'Stock',  align: 'center' },
 *   ];
 *
 *   <DataTable
 *     title="Inventario"
 *     columns={columns}
 *     data={products}
 *     loading={loading}
 *   />
 */
const DataTable = ({
  title,
  columns = [],
  data    = [],
  loading = false,
  emptyText = 'No hay datos para mostrar.',
  keyField  = 'id',
  actions,
  footer,
}) => {
  return (
    <div className={styles.wrap}>
      {(title || actions) && (
        <div className={styles.header}>
          {title && <span className={styles.title}>{title}</span>}
          {actions}
        </div>
      )}

      {loading ? (
        <div className={styles.stateBox}>
          <Spinner size="lg" />
          <span className={styles.stateLabel}>Cargando...</span>
        </div>
      ) : data.length === 0 ? (
        <div className={styles.stateBox}>
          <TableProperties size={40} />
          <span className={styles.stateLabel}>{emptyText}</span>
        </div>
      ) : (
        <div className={styles.tableScroll}>
          <table className={styles.table}>
            <thead>
              <tr>
                {columns.map((col) => (
                  <th key={col.key} style={{ textAlign: col.align || 'left' }}>
                    {col.label}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.map((row, rowIdx) => (
                <tr key={row[keyField] ?? rowIdx}>
                  {columns.map((col) => (
                    <td key={col.key} style={{ textAlign: col.align || 'left' }}>
                      {col.render ? col.render(row[col.key], row) : (row[col.key] ?? '—')}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {footer && (
        <div className={styles.footer}>
          <span>{footer}</span>
        </div>
      )}
    </div>
  );
};

export default DataTable;

import styles from './Badge.module.css';

/**
 * Badge — Lego Piece
 * Para etiquetas de estado.
 *
 * variant: 'success' | 'warning' | 'danger' | 'info' | 'primary' | 'default'
 */
const Badge = ({ children, variant = 'default', dot = false }) => {
  const cls = [styles.badge, styles[variant]].filter(Boolean).join(' ');
  return (
    <span className={cls}>
      {dot && <span className={styles.dot} />}
      {children}
    </span>
  );
};

export default Badge;

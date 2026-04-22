import styles from './Spinner.module.css';

/**
 * Spinner — Lego Piece
 * size: 'sm' | 'md' | 'lg'
 * color: 'primary' | 'white' | 'muted'
 */
const Spinner = ({ size = 'md', color = 'primary' }) => {
  const cls = [styles.spinner, styles[size], styles[color]].filter(Boolean).join(' ');
  return <span className={cls} role="status" aria-label="Cargando..." />;
};

export default Spinner;

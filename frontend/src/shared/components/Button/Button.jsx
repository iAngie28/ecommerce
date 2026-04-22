import styles from './Button.module.css';

/**
 * Componente Button — Lego Piece
 *
 * Props:
 *   variant  : 'primary' | 'secondary' | 'ghost' | 'danger'
 *   size     : 'sm' | 'md' | 'lg'
 *   fullWidth: boolean
 *   loading  : boolean
 *   leftIcon : ReactNode
 *   rightIcon: ReactNode
 *   ...rest  : todos los atributos nativos de <button>
 *
 * Uso:
 *   <Button variant="primary" leftIcon={<Plus size={16} />}>Nuevo</Button>
 */
const Button = ({
  children,
  variant  = 'primary',
  size     = 'md',
  fullWidth = false,
  loading  = false,
  leftIcon,
  rightIcon,
  className = '',
  disabled,
  ...rest
}) => {
  const cls = [
    styles.btn,
    styles[variant],
    styles[size],
    fullWidth ? styles.full : '',
    className,
  ].filter(Boolean).join(' ');

  return (
    <button className={cls} disabled={disabled || loading} {...rest}>
      {loading ? (
        <span className={styles.spinner} aria-hidden="true" />
      ) : leftIcon}
      {children}
      {!loading && rightIcon}
    </button>
  );
};

export default Button;

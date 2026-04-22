import styles from './Input.module.css';

/**
 * Componente Input — Lego Piece
 *
 * Props:
 *   label     : string
 *   hint      : string — texto de ayuda debajo
 *   error     : string — mensaje de error
 *   leftIcon  : ReactNode
 *   rightIcon : ReactNode
 *   labelRight: ReactNode — elemento a la derecha del label (ej: "¿Olvidaste tu contraseña?")
 *   ...rest   : todos los atributos nativos de <input>
 *
 * Uso:
 *   <Input
 *     label="Correo"
 *     leftIcon={<Mail size={16} />}
 *     type="email"
 *     placeholder="tu@correo.com"
 *     error={errors.email}
 *   />
 */
const Input = ({
  label,
  hint,
  error,
  leftIcon,
  rightIcon,
  labelRight,
  id,
  className = '',
  ...rest
}) => {
  const wrapCls = [
    styles.inputWrap,
    leftIcon  ? styles.hasLeft  : '',
    rightIcon ? styles.hasRight : '',
  ].filter(Boolean).join(' ');

  const groupCls = [styles.group, error ? styles.error : '', className].filter(Boolean).join(' ');

  return (
    <div className={groupCls}>
      {label && (
        <div className={styles.labelRow}>
          <label htmlFor={id} className={styles.label}>{label}</label>
          {labelRight}
        </div>
      )}
      <div className={wrapCls}>
        {leftIcon  && <span className={styles.iconLeft}>{leftIcon}</span>}
        <input id={id} className={styles.input} {...rest} />
        {rightIcon && <span className={styles.iconRight}>{rightIcon}</span>}
      </div>
      {error && <span className={styles.errorMsg}>{error}</span>}
      {hint && !error && <span className={styles.hint}>{hint}</span>}
    </div>
  );
};

export default Input;

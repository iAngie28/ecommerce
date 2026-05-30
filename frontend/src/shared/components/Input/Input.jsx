import { useState } from 'react';
import { Eye, EyeOff } from 'lucide-react';
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
  type,
  ...rest
}) => {
  const [showPassword, setShowPassword] = useState(false);
  const isPassword = type === 'password';

  // Si es campo de contraseña, el tipo real alterna entre 'password' y 'text'
  const resolvedType = isPassword ? (showPassword ? 'text' : 'password') : type;

  // El ícono de la derecha: si hay rightIcon externo lo respetamos,
  // si es password usamos el toggle de ojo
  const effectiveRightIcon = isPassword ? (
    <button
      type="button"
      onClick={() => setShowPassword(v => !v)}
      className={styles.eyeBtn}
      aria-label={showPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'}
      tabIndex={-1}
    >
      {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
    </button>
  ) : rightIcon;

  const wrapCls = [
    styles.inputWrap,
    leftIcon            ? styles.hasLeft  : '',
    effectiveRightIcon  ? styles.hasRight : '',
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
        {leftIcon && <span className={styles.iconLeft}>{leftIcon}</span>}
        <input id={id} className={styles.input} type={resolvedType} {...rest} />
        {effectiveRightIcon && (
          isPassword
            ? effectiveRightIcon
            : <span className={styles.iconRight}>{effectiveRightIcon}</span>
        )}
      </div>
      {error && <span className={styles.errorMsg}>{error}</span>}
      {hint && !error && <span className={styles.hint}>{hint}</span>}
    </div>
  );
};

export default Input;

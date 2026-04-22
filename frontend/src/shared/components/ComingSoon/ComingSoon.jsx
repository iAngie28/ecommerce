import styles from './ComingSoon.module.css';

/**
 * ComingSoon — Lego Piece para módulos en desarrollo.
 *
 * Props:
 *   icon       : ReactNode
 *   title      : string
 *   description: string
 *   features   : string[] — lista de características futuras
 *   accentColor: string   — color CSS del icono
 */
const ComingSoon = ({ icon, title, description, features = [], accentColor }) => {
  const iconStyle = accentColor
    ? { '--card-bg': `${accentColor}18`, '--card-color': accentColor }
    : undefined;

  return (
    <div className={styles.wrap}>
      <span className={styles.badge}>Próximamente</span>
      <div className={styles.icon} style={iconStyle}>{icon}</div>
      <div>
        <h2 className={styles.title}>{title}</h2>
        <p className={styles.description}>{description}</p>
      </div>
      {features.length > 0 && (
        <div className={styles.features}>
          {features.map((f, i) => (
            <span key={i} className={styles.feature}>✓ {f}</span>
          ))}
        </div>
      )}
    </div>
  );
};

export default ComingSoon;

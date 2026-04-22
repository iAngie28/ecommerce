import styles from './StatCard.module.css';

/**
 * StatCard — KPI card widget
 *
 * Props:
 *   label      : string
 *   value      : string | number
 *   change     : string — ej: "+12% vs mes pasado"
 *   trend      : 'positive' | 'negative' | 'neutral'
 *   icon       : ReactNode
 *   accentColor: string — color CSS var (ej: 'var(--color-success)')
 *
 * StatCard.Group — grilla automática
 *   <StatCard.Group>
 *     <StatCard ... />
 *     <StatCard ... />
 *   </StatCard.Group>
 */
const StatCard = ({ label, value, change, trend = 'neutral', icon, accentColor, style }) => {
  const cardStyle = accentColor
    ? { '--card-accent': accentColor, '--card-accent-ghost': `${accentColor}22`, ...style }
    : style;

  return (
    <div className={styles.card} style={cardStyle}>
      <div className={styles.header}>
        <span className={styles.label}>{label}</span>
        {icon && <div className={styles.icon}>{icon}</div>}
      </div>
      <div className={styles.value}>{value ?? '—'}</div>
      {change && (
        <div className={`${styles.change} ${styles[trend]}`}>
          {change}
        </div>
      )}
    </div>
  );
};

const Group = ({ children }) => (
  <div className={styles.group}>{children}</div>
);

StatCard.Group = Group;

export default StatCard;

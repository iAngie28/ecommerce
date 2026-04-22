import { Link } from 'react-router-dom';
import AppView from 'shared/widgets/AppView/AppView';

export default function ListaTiendasView() {
  return (
    <AppView title="Lista de Tiendas" subtitle="Administración de tiendas registradas">
      <p style={{ color: 'var(--color-text-muted)', textAlign: 'center', padding: 'var(--space-12)' }}>
        Vista en construcción. <Link to="/dashboard">Volver al panel</Link>
      </p>
    </AppView>
  );
}

import { Users } from 'lucide-react';
import AppView    from 'shared/widgets/AppView/AppView';
import ComingSoon from 'shared/components/ComingSoon/ComingSoon';

export default function ClientesView() {
  return (
    <AppView title="Clientes" subtitle="Gestiona tu base de clientes y su historial.">
      <ComingSoon
        icon={<Users size={36} />}
        title="Gestión de Clientes"
        description="CRM completo: perfiles de clientes, historial de compras, segmentación y campañas de fidelización."
        accentColor="var(--color-info)"
        features={[
          'Directorio de clientes',
          'Historial de compras',
          'Segmentación por comportamiento',
          'Programa de fidelización',
          'Comunicaciones automáticas',
          'Análisis de retención',
        ]}
      />
    </AppView>
  );
}

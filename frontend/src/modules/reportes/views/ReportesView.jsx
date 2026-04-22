import { BarChart3 } from 'lucide-react';
import AppView    from 'shared/widgets/AppView/AppView';
import ComingSoon from 'shared/components/ComingSoon/ComingSoon';

export default function ReportesView() {
  return (
    <AppView title="Reportes & Análisis" subtitle="Inteligencia de negocio y predicciones con IA.">
      <ComingSoon
        icon={<BarChart3 size={36} />}
        title="Reportes e Inteligencia de Negocio"
        description="Dashboard interactivo con métricas en tiempo real, predicciones de ventas con Machine Learning y análisis de comportamiento."
        accentColor="var(--color-accent)"
        features={[
          'Predicción de ventas IA',
          'Análisis de rentabilidad',
          'Rotación de inventario',
          'Comportamiento de clientes',
          'Exportación a Excel/PDF',
          'Alertas automáticas',
        ]}
      />
    </AppView>
  );
}

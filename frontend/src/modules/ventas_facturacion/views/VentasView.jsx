import { ShoppingCart } from 'lucide-react';
import AppView    from 'shared/widgets/AppView/AppView';
import ComingSoon from 'shared/components/ComingSoon/ComingSoon';

export default function VentasView() {
  return (
    <AppView title="Ventas & Facturación" subtitle="Gestiona pedidos, facturas y pagos de tu tienda.">
      <ComingSoon
        icon={<ShoppingCart size={36} />}
        title="Ventas y Facturación"
        description="Registro completo de ventas, emisión de facturas SIN/QR, seguimiento de pedidos y gestión de devoluciones."
        accentColor="var(--color-success)"
        features={[
          'Registro de ventas',
          'Facturación electrónica SIN',
          'Pagos con QR',
          'Gestión de pedidos',
          'Historial de transacciones',
          'Devoluciones y créditos',
        ]}
      />
    </AppView>
  );
}

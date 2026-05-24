# apps/negocio/billing/api/urls.py
from django.urls import path
from app_negocio.views.factura_views import FacturaViewSet, TipoPagoViewSet
from app_negocio.views.pago_views import PagoViewSet

urlpatterns = [
    # Facturas
    path('facturas/', FacturaViewSet.as_view({'get': 'list', 'post': 'create'}), name='factura-list'),
    path('facturas/<str:nro>/descargar_pdf/', FacturaViewSet.as_view({'get': 'descargar_pdf'}), name='factura-pdf'),
    path('tipos-pago/', TipoPagoViewSet.as_view({'get': 'list', 'post': 'create'}), name='tipo-pago-list'),
    # Pagos / Stripe
    path('pagos/', PagoViewSet.as_view({'get': 'list', 'post': 'create'}), name='pago-list'),
    path('pagos/create-checkout-session/', PagoViewSet.as_view({'post': 'create_checkout_session'}), name='pago-stripe-session'),
    path('pagos/webhook/', PagoViewSet.as_view({'post': 'stripe_webhook'}), name='pago-stripe-webhook'),
    path('pagos/confirm-success/', PagoViewSet.as_view({'post': 'confirm_success'}), name='pago-confirm-success'),
]

from django.urls import path

from carrito import views
from payments import views as views_payments

urlpatterns = [
    path("carrito/", views.CarritoView.as_view(), name="carrito"),
    path("eliminar/carrito/<int:cita_id>/", views.eliminar_cita, name="eliminar"),
    path("limpiar/", views.limpiar_carrito, name="limpiar"),
    path("carrito/utils/config/", views_payments.stripe_config),
    path("carrito/utils/create-custom-checkout-session/",
         views_payments.create_custom_checkout_session,
         ),
    path("carrito/utils/create-checkout-session/",
         views_payments.create_checkout_session,
         ),
]

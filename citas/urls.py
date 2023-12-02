from django.urls import path
from .views import (
    CitaView,
    get_especialistas_por_servicio,
    get_horas_disponibles,
    get_precio_por_servicio,
    get_precio_id_por_servicio
)
from payments import views as views


urlpatterns = [
    path(
        "especialistas_opciones/",
        get_especialistas_por_servicio,
        name="especialistas_opciones",
    ),
    path("horas_disponibles/", get_horas_disponibles, name="horas_disponibles"),
    path("cita/", CitaView.as_view(), name="cita"),
    path('precio_servicio/', get_precio_por_servicio, name='precio'),
    path('precio_id_servicio/', get_precio_id_por_servicio, name='precioid'),
    path('cita/utils/config/', views.stripe_config),
    path('cita/utils/create-custom-checkout-session/<str:param>/<str:ident>', views.create_custom_checkout_session),
    path('cita/success/', views.SuccessView.as_view(), name='success'),  # new
    path('cita/cancelled/', views.CancelledView.as_view(), name='cancelled'),
    path('cita/webhook/', views.stripe_webhook),
]

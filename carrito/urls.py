from django.urls import path

from carrito import views


urlpatterns = [
    path("carrito/", views.CarritoView.as_view(), name="carrito"),
    path("eliminar/carrito/<int:cita_id>/", views.eliminar_cita, name="eliminar"),
    path("limpiar/", views.limpiar_carrito, name="limpiar"),
]

from django.urls import path

from carrito import views


urlpatterns = [
    path("carrito/", views.CarritoView.as_view(), name="carrito"),
]

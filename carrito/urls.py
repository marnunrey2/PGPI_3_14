from django.urls import path

from carrito import views


urlpatterns = [
    path("carrito/", views.tienda, name="carrito"),
]

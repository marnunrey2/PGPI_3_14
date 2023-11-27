from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('utils/config/', views.stripe_config),
    path('utils/create-checkout-session/', views.create_checkout_session), #Used as an example
    path('utils/create-custom-checkout-session/<str:param>/', views.create_custom_checkout_session),
    path('success/', views.SuccessView.as_view(), name='success'),  # new
    path('cancelled/', views.CancelledView.as_view(), name='cancelled'),
    path('webhook/', views.stripe_webhook),
]

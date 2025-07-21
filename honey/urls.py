from django.urls import path
from honey import views


urlpatterns = [
    path('honeys/', views.HoneysView.as_view(), name='honeys'),
    path('honey_taste/', views.AddHoneyTasteView.as_view(), name='honey_taste'),
    path('honey_type/', views.AddHoneyTypeView.as_view(), name='honey_type'),
    path('honey_variant/', views.AddHoneyVariantView.as_view(), name='honey_variant'),
    path('honey_offer/', views.AddHoneyOfferView.as_view(), name='honey_offer'),
    path('honey_list/', views.HoneyListAndSearchView.as_view(), name='honey_list'),
    path('update_offer/<int:pk>/', views.UpdateHoneyOfferView.as_view(), name='update_offer'),
    path('delete_offer/<int:pk>/', views.DeleteHoneyOfferView.as_view(), name='delete_offer'),
    path('add_product/', views.AddBeeProductView.as_view(), name='add_product' ),
    path('update_product/<int:pk>/', views.UpdateBeeProductView.as_view(), name='update_product'),
    path('delete_product/<int:pk>/', views.DeleteBeeProductView.as_view(), name='delete_product'),
]
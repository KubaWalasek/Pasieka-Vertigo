from django.urls import path
from honey import views


urlpatterns = [
    path('add_honey/', views.AddHoneyView.as_view(), name='add_honey'),
    path('update_honey/<int:pk>', views.UpdateHoneyView.as_view(), name='update_honey'),
    path('delete_honey/<int:pk>', views.DeleteHoneyView.as_view(), name='delete_honey')

]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('explore', views.explore, name='explore'),
    path('explore/filterproduct', views.filterproduct, name='filterproduct'),
    path('crop-recommend', views.crop_recommend, name='crop-recommend'),
    path('crop-recommend/result', views.result, name='result'),
    path('feedback', views.feedback, name='feedback'),
    path('trace', views.trace, name='trace'),
    path('absolute', views.absolute, name='absolute'),
    path('wolverine', views.wolverine, name='wolverine'),
    path('alion', views.alion, name='alion'),
    path('scala', views.scala, name='scala'),
    path('movento', views.movento, name='movento'),
]
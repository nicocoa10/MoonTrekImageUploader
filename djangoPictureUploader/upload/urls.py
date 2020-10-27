from django.urls import path

from . import views

app_name = "upload"
# Upload App url is linked in the main project urls
urlpatterns= [
    path('', views.upload, name="upload"), #here is the upload view path url patterns
    path('upload/verify/', views.verify, name="verify"),
    path('upload/choose_call/', views.chooseCall, name="choose_call"),
    path('upload/vector/<time>/', views.planetVectorAPICall, name="vector"),
    path('upload/nearest_point/<lon>/<lat>/<time>', views.nearestPointAPICall, name="nearest_point")
]
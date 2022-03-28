from django.urls import path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from . import views


router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"posts", views.PostViewSet)

urlpatterns = [path("login/", obtain_auth_token)]
urlpatterns += router.urls

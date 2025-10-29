"""
URL configuration for infinite_grid project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from grid import views

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # Autenticação
    path("", views.login_view, name="login"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    
    # Jogador
    path("player/join/", views.player_join_view, name="player_join"),
    path("player/room/<str:room_code>/", views.player_room_view, name="player_room"),
    
    # Mestre
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("room/create/", views.create_room_view, name="create_room"),
    path("room/<str:room_code>/", views.master_room_view, name="master_room"),
    path("room/<str:room_code>/delete/", views.delete_room_view, name="delete_room"),
    
    # API de Cenas
    path("api/room/<str:room_code>/scenes/", views.list_scenes_api, name="list_scenes"),
    path("api/room/<str:room_code>/scenes/create/", views.create_scene_api, name="create_scene"),
    path("api/room/<str:room_code>/scenes/<int:scene_id>/", views.update_scene_api, name="update_scene"),
    path("api/room/<str:room_code>/scenes/<int:scene_id>/delete/", views.delete_scene_api, name="delete_scene"),
    path("api/room/<str:room_code>/scenes/<int:scene_id>/switch/", views.switch_scene_api, name="switch_scene"),
    
    # API de Upload
    path("api/upload/image/", views.upload_image_api, name="upload_image"),
]

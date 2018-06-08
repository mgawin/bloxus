from django.urls import path


from . import views


urlpatterns = [
    path("init/", views.init),
    path("get/", views.get),
    path("check_move/", views.check_move),
    path("move/", views.move),
    path("get_moves/", views.get_available_moves),
]

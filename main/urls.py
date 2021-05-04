from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/",views.register,name="register"),
    path("login/",views.login_view,name="login"),
    path("student/",views.student,name="student"),
    path("instructor/",views.instructor,name="instructor"),
    path("logout/",views.logout_view,name="logout"),
    path("cruise/",views.cruise,name="cruise"),
    path("water/",views.water,name="water"),
    path("test/",views.test,name="test"),
    path("servomotor/", views.servomotor, name="servomotor")
]
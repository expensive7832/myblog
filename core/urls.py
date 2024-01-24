from django.urls import path
from . import views

urlpatterns = [
    path("", views.Home, name="home"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("update-profile/<int:pk>", views.updateprofile, name="update-profile"),
    path("logout/", views.signout, name="logout"),
    path("delete/", views.delete, name="delete"),
    path("post-article/", views.postArticle, name="post"),
    path("single-post/<int:pk>", views.blogDetails, name="blogdetails"),
    path("del-reply/", views.deleteReply, name="del-reply"),
    path("del-comment/", views.deleteComment, name="del-comment"),
    path("forgetpassword/", views.changePassword, name="forgetpassword"),
    path("search/", views.search, name="search"),
]
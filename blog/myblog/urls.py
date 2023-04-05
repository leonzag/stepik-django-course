from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path("", views.MainView.as_view(), name="index"),
    path("post/<slug:slug>/", views.PostDetailView.as_view(), name="post_detail"),
    path("tag/<slug:slug>/", views.TagView.as_view(), name="tag"),
    path("search/", views.SearchResaultsView.as_view(), name="search"),
    path("contact/", views.FeedBackView.as_view(), name="contact"),
    path("contact/success/", views.SuccessView.as_view(), name="success"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("signin/", views.SignInView.as_view(), name="signin"),
    path(
        "signout/",
        LogoutView.as_view(),
        {"next_page": settings.LOGOUT_REDIRECT_URL},
        name="signout",
    ),
]

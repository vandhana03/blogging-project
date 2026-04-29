from django.urls import include, path
from .import views

urlpatterns = [
    path('register/',views.register.as_view()),
    path('login/',views.login.as_view()),
    path('blog/',views.BlogView.as_view()),
    path('blog/<int:blog_id>',views.BlogView.as_view()),
    path('comment/',views.CommentView.as_view()),
    path('comment/<int:comment_id>',views.CommentView.as_view()),



]
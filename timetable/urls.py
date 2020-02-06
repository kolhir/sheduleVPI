from django.urls import path
from .viewsApi import LessonsForGroupView, LessonsView
app_name = "articles"
# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('lessons_for_group/<int:group_id>', LessonsForGroupView.as_view({'get': 'list', 'post': 'update'})),
    path('lessons/', LessonsView.as_view({'get': 'list'})),
]

from django.urls import path

from .views import (
    ArticleListView,
    ArticleUpdateView,
    ArticleDeleteView,
    ArticleDetailView,
    ArticleCreateView,
    ArticleViewApi,
    # ArticleViewApiGetId,
    ArticleDetail,
    AddCommentView
)

urlpatterns = [
    path('<int:pk>/edit/', ArticleUpdateView.as_view(), name="article_edit"),
    path('<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
    path('new/', ArticleCreateView.as_view(), name='article_new'),
    path('<int:pk>/comment/', AddCommentView.as_view(), name='add_comment'),
    path('', ArticleListView.as_view(), name='article_list'),

    # path('articleGetId/<int:id>/', ArticleViewApiGetId.as_view()),
    path('articleGet/', ArticleViewApi.as_view()),
    path('genericAPIView/<int:pk>/', ArticleDetail.as_view()),



]

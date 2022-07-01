from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (ListView, DetailView)
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from rest_framework import status, mixins, generics
from django.core.mail import send_mail

from .forms import CommentForm
from .models import Article, Comment
from django.urls import reverse_lazy
from rest_framework.views import APIView
from .serializers import ArticleSerializer
from rest_framework.response import Response


# Create your views here.

class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ('title', 'summary', 'body', 'photo')
    template_name = 'article_edit.html'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleCreateView(LoginRequiredMixin,  CreateView):
    model = Article
    template_name = 'article_new.html'
    fields = ('title', 'summary', 'body', 'photo',)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # # user superuser ekanini tekshirish
    # def test_func(self):
    #     return self.request.user.is_superuser


class ArticleViewApi(APIView):
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddCommentView(CreateView):
    model = Comment
    template_name = 'add_comment.html'
    form_class = CommentForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        article = Article.objects.get(id=self.kwargs["pk"])
        obj.articles = article
        obj.save()
        return super().form_valid(form)

    # def massage_email(self, request):
    # username = self.request.data['user']
    #
    # print(username.data)
    # return Response(username)


# ==========================================================>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# def post(self, request, *args, **kwargs):
#     form = CommentForm(request.POST)
#     if form.is_valid():
#         print('bbbbbbb', request.user)
#         print('aaaaaaaaa', form["articles"])
#         article = Article.objects.get(id=form["articles"])
#         # a = form.save(commit=True)
#         # a.author = request.user
#         # a.save()
#         Comment.objects.create(author=request.user, comment=form["comment"], articles=form[article])


# ================================successful===============================================
# class ArticleViewApiGetId(APIView):
#     def get_object(self, id):
#         try:
#             return Article.objects.get(id=id)
#         except Article.DoesNotExist:
#             raise Http404
#
#     def get(self, request, id, format=None):
#         article = self.get_object(id)
#         serializer = ArticleSerializer(article)
#         return Response(serializer.data)


# =====================ishlamadi=========================
# def delete(self, request, id, format=None):
#     article = self.get_object(id)
#     article.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)


# class AddCommentView(CreateView):
#     model = Comment
#     # template_name = 'add_comment.html'
#
#     fields = "__all__"
#     def massage(self, request):
#         username = self.request.data.author
#         print(username.data)
#

# send_mail("Hello from PrettyPrinted", f"shun user siznig postingizga koment yo'zdi{username}", )


class ArticleDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

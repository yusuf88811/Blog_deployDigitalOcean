from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.dispatch import Signal
from django.core.mail import send_mail
from django.db.models.signals import post_save

from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

from .tasks import send_email


# Create your models here.
User = get_user_model()


class Article(models.Model):
    title = models.CharField(max_length=150)
    summary = models.CharField(max_length=200, blank=True)
    body = RichTextField()
    photo = models.ImageField(upload_to='images/', blank=True)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', args=[str(self.id)])


class Comment(models.Model):
    articles = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE, )

    # date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

    def get_absolute_url(self):
        return reverse('article_list')

    @property
    def get_article_author_email(self):
        return self.articles.author.email

    @property
    def get_commenet_author(self):
        return self.author.username



    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        print(self.get_commenet_author, self.get_article_author_email)
        # send_mail('Hello from PrettyPrinted', f'{self.comment}', 'tolaganovyusuf00@gmail.com',
        #           [f'{self.get_article_author_email}'], fail_silently=False)
        send_email.delay(self.get_article_author_email, self.get_commenet_author, self.comment)
        super().save(force_insert, force_update, using, update_fields)

#
# def massage_add(sender, instance, created, **kwargs):
#     print(f"sender: {sender.get_comment_author}\n instance:{instance}\n created{created} ")
#     # coment = Comment.objects.get(comment=instance)
#
#
#     send_mail('Hatolik yuz berdi', f'Masha allohx',
#               'tolaganovyusuf00@gmail.com',
#               [f'{sender.get_comment_author}'], fail_silently=False)
#     # return super().save(commit)


# Signal.connect(post_save, massage_add, sender=Comment)

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from django.views.generic.base import TemplateView


# Create your views here.
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


# class Upper(TemplateView):
#
#     def get(self, request):
#         template_name = 'home.html'
#         custom_user = request.user
#         custom_user.first_name = custom_user.first_name.upper()
#         custom_user.username = custom_user.username.upper()
#
#         return render(request, template_name, {"custom_user": custom_user})

from django.shortcuts import render

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages

class SignUp(generic.edit.FormView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

    def form_valid(self, form):
        form.save()
        return super(SignUp, self).form_valid(form)

    def form_invalid(self, form):
        # import ipdb
        # ipdb.set_trace()
        # messages.error(self.request, "Что-то ")
        return super(SignUp, self).form_invalid(form)
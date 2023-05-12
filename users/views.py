from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from news.models import News


class UserRegistrationView(CreateView):
    template_name = 'users/user/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('user_news_list')
    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'],
                            password=cd['password1'])
        login(self.request, user)
        return result


# class UserEnrollNewsView(LoginRequiredMixin, FormView):
#     news = None
#     form_class = NewsEnrollForm
#     def form_valid(self, form):
#         self.news = form.cleaned_data['news']
#         self.news.users.add(self.request.user)
#         return super().form_valid(form)
#     def get_success_url(self):
#         return reverse_lazy('user_news_detail',
#                             args=[self.news.id])


class UserNewsListView(LoginRequiredMixin, ListView):
    model = News
    template_name = 'users/news/list.html'
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner__in=[self.request.user])


class UserNewsDetailView(DetailView):
    model = News
    template_name = 'users/news/detail.html'
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner__in=[self.request.user])


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get news object
        news = self.get_object()
        if 'module_id' in self.kwargs:
            # get current module
            context['module'] = news.modules.get(
                                    id=self.kwargs['module_id'])
        else:
            # get first module
            context['module'] = news.modules.all()[0]
        return context
    
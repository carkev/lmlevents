"""News view module.
"""
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, \
                                      DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, \
                                       PermissionRequiredMixin
from django.core.cache import cache
from django.urls import reverse_lazy
from django.forms.models import modelform_factory
from django.apps import apps
from django.db.models import Count

from .forms import ModuleFormSet
from .models import News
from .models import Module, Content, Subject


class OwnerMixin:
    """Mixin class to retrieve the owner news.
    """
    def get_queryset(self):
        """Get the owner news.
        """
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)


class OwnerEditMixin:
    """Mixin class to edit.
    """
    def form_valid(self, form):
        """Valid form only if the owner is the editor.
        """
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerNewsMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    """Mixin class to get news.
    """
    model = News
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('news:manage_news_list')


class OwnerNewsEditMixin(OwnerNewsMixin, OwnerEditMixin):
    """Mixin class to get the edit form only if the editor is the
    author.
    """
    template_name = 'news/manage/news/form.html'


class ManageNewsListView(OwnerNewsMixin, ListView):
    """Manage news list view class.
    """
    model = News
    template_name = 'news/manage/news/list.html'
    permission_required = 'news.view_news'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class NewsCreateView(OwnerNewsEditMixin, CreateView):
    """News create view class.
    """
    permission_required = 'news.add_news'


class NewsUpdateView(OwnerNewsEditMixin, UpdateView):
    """News update view.
    """
    permission_required = 'news.change_news'


class NewsDeleteView(OwnerNewsMixin, DeleteView):
    """News delete view.
    """
    template_name = 'news/manage/news/delete.html'
    permission_required = 'news.delete_news'


class NewsModuleUpdateView(TemplateResponseMixin, View):
    """News module update view.
    """
    template_name = 'news/manage/module/formset.html'
    news = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.news,
                             data=data)

    def dispatch(self, request, pk):
        self.news = get_object_or_404(News, id=pk, owner=request.user)
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        """Get HTML request.
        """
        formset = self.get_formset()
        return self.render_to_response({'news': self.news, 'formset': formset})

    def post(self, request, *args, **kwargs):
        """Post HTML request.
        """
        formset = self.get_formset(data=request.POST)

        if formset.is_valid():
            formset.save()
            return redirect('news:manage_news_list')

        return self.render_to_response({'news': self.news, 'formset': formset})


class ContentCreateUpdateView(TemplateResponseMixin, View):
    """Content create update view class.
    """
    module = None
    model = None
    obj = None
    template_name = 'news/manage/content/form.html'

    def get_model(self, model_name):
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='news',
                                  model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        form = modelform_factory(model, exclude=['owner',
                                                 'order',
                                                 'created',
                                                 'updated'])
        return form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(Module,
                                        id=module_id,
                                        news__owner=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model,
                                         id=id,
                                         owner=request.user)
        return super().dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        """Get HTML request.
        """
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form,
                                        'object': self.obj})

    def post(self, request, module_id, model_name, id=None):
        """Post HTML request.
        """
        form = self.get_form(self.model,
                             instance=self.obj,
                             data=request.POST,
                             files=request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()

            if not id:
                # new content
                Content.objects.create(module=self.module, item=obj)

            return redirect('news:module_content_list', self.module.id)

        return self.render_to_response({'form': form, 'object': self.obj})


class ContentDeleteView(View):
    """Content delete view class.
    """
    def post(self, request, order_id):
        """Post HTML request.
        """
        content = get_object_or_404(Content,
                                    id=order_id,
                                    module__news__owner=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('news:module_content_list', module.id)


class ModuleContentListView(TemplateResponseMixin, View):
    """Module content list view class.
    """
    template_name = 'news/manage/module/content_list.html'

    def get(self, request, module_id):
        """Get HTML request.
        """
        module = get_object_or_404(Module,
                                   id=module_id,
                                   news__owner=request.user)
        return self.render_to_response({'module': module})


class ModuleOrderView(View):
    """Module order view class.
    """

    def post(self, request):
        """Post HTML request.
        """
        for order_id, order in self.request_json.items():
            Module.objects.filter(id=order_id,
                                  news__owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})


class ContentOrderView(View):
    """Content order view class.
    """

    def post(self, request):
        """Post HTML request.
        """
        for order_id, order in self.request_json.items():
            Content.objects.filter(
                id=order_id, module__news__owner=request.user) \
                    .update(order=order)

        return self.render_json_response({'saved': 'OK'})


class NewsListView(TemplateResponseMixin, View):
    """News list view class.
    """
    model = News
    template_name = 'news/news/list.html'

    def get(self, request, subject=None):
        """Get HTML request.
        """
        subjects = cache.get('all_subjects')

        if not subjects:
            subjects = Subject.objects.annotate(total_news=Count('news'))
            cache.set('all_subjects', subjects)

        all_news = News.objects.annotate(total_modules=Count('modules'))

        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            key = f'subject_{subject.id}_news'
            news = cache.get(key)

            if not news:
                news = all_news.filter(subject=subject)
                cache.set(key, news)

        else:
            news = cache.get('all_news')

            if not news:
                news = all_news
                cache.set('all_news', news)

        return self.render_to_response({'subjects': subjects,
                                        'subject': subject,
                                        'news': news})


class NewsDetailView(DetailView):
    """News detail view class.
    """
    model = News
    template_name = 'news/news/detail.html'

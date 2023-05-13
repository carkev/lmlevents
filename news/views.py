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


class ManageNewsListView(ListView):
    model = News
    template_name = 'news/manage/news/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin:
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerNewsMixin(OwnerMixin,
                       LoginRequiredMixin,
                       PermissionRequiredMixin):
    model = News
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_news_list')


class OwnerNewsEditMixin(OwnerNewsMixin, OwnerEditMixin):
    template_name = 'news/manage/news/form.html'


class ManageNewsListView(OwnerNewsMixin, ListView):
    model = News
    template_name = 'news/manage/news/list.html'
    permission_required = 'news.view_news'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class NewsCreateView(OwnerNewsEditMixin, CreateView):
    permission_required = 'news.add_news'


class NewsUpdateView(OwnerNewsEditMixin, UpdateView):
    permission_required = 'news.change_news'


class NewsDeleteView(OwnerNewsMixin, DeleteView):
    template_name = 'news/manage/news/delete.html'
    permission_required = 'news.delete_news'


class NewsModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'news/manage/module/formset.html'
    news = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.news,
                             data=data)

    def dispatch(self, request, pk):
        self.news = get_object_or_404(News,
                                        id=pk,
                                        owner=request.user)
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'news': self.news,
                                        'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('news:manage_news_list')
        return self.render_to_response({'news': self.news,
                                        'formset': formset})


class ContentCreateUpdateView(TemplateResponseMixin, View):
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
        Form = modelform_factory(model, exclude=['owner',
                                                 'order',
                                                 'created',
                                                 'updated'])
        return Form(*args, **kwargs)

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
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form,
                                        'object': self.obj})

    def post(self, request, module_id, model_name, id=None):
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
                Content.objects.create(module=self.module,
                                       item=obj)
            return redirect('news:module_content_list', self.module.id)
        return self.render_to_response({'form': form,
                                        'object': self.obj})


class ContentDeleteView(View):
    def post(self, request, id):
        content = get_object_or_404(Content,
                               id=id,
                               module__news__owner=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('news:module_content_list', module.id)


class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'news\manage\module\content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(Module,
                                   id=module_id,
                                   news__owner=request.user)
        return self.render_to_response({'module': module})


class ModuleOrderView(
                      
                      View):

    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(id=id,
                   news__owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})


class ContentOrderView(
                       View):

    def post(self, request):
        for id, order in self.request_json.items():
            Content.objects.filter(id=id,
                       module__news__owner=request.user) \
                       .update(order=order)
        return self.render_json_response({'saved': 'OK'})
    

class NewsListView(TemplateResponseMixin, View):
    model = News
    template_name = 'news/news/list.html'
    def get(self, request, subject=None):
        subjects = cache.get('all_subjects')
        if not subjects:
            subjects = Subject.objects.annotate(
                            total_news=Count('news'))
            cache.set('all_subjects', subjects)
        all_news = News.objects.annotate(
                        total_modules=Count('modules'))
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
    model = News
    template_name = 'news/news/detail.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['enroll_form'] = NewsEnrollForm(
    #                                initial={'news':self.object})
    #     return context
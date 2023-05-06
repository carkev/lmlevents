"""Pages app views.
"""
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    """Home page class view.
    """
    template_name = "pages/index.html"


class AboutPageView(TemplateView):
    """About page class view.
    """
    template_name = "pages/about.html"


class PartnersPageView(TemplateView):
    """Partners page class view.
    """
    template_name = "pages/partners.html"


class CGUPageView(TemplateView):
    """CGU page class view.
    """
    template_name = "pages/cgu.html"


class CGVPageView(TemplateView):
    """CGV page class view.
    """
    template_name = "pages/cgv.html"


class LegalNoticesView(TemplateView):
    """Legal notices page class view.
    """
    template_name = "pages/legal-notices.html"


class GPDRPageView(TemplateView):
    """GPDR page class view.
    """
    template_name = "pages/gpdr.html"

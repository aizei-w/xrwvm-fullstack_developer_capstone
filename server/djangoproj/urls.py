from django.contrib import admin
from django.conf import settings
from django.http import HttpResponse
from django.urls import include, path, re_path
from django.views.generic import TemplateView


def react_app(request):
    if not (settings.FRONTEND_BUILD_DIR / "index.html").exists():
        return HttpResponse("React build not found. Run npm run build.", status=503)
    return TemplateView.as_view(template_name="index.html")(request)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("djangoapp/", include("djangoapp.urls")),
    path("about", TemplateView.as_view(template_name="About.html")),
    path("about/", TemplateView.as_view(template_name="About.html")),
    path("contact", TemplateView.as_view(template_name="Contact.html")),
    path("contact/", TemplateView.as_view(template_name="Contact.html")),
    path("", react_app, name="home"),
    re_path(r"^(?:login|register|dealers|dealer/\d+|postreview/\d+)/?$", react_app),
]

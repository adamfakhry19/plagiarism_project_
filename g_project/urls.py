from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import TemplateView
from pd_app.views import FileUploadView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/upload/', FileUploadView.as_view(), name='file-upload'),
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html'), name='home'),  # This serves the React app
]

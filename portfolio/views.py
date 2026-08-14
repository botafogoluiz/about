from django.shortcuts import render

from .models import Project


def project_list(request):
    projects = Project.objects.filter(is_visible=True)
    return render(request, "portfolio/project_list.html", {"projects": projects})

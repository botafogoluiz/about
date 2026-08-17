from django.shortcuts import render

from .models import Education, Experience, Language, Profile


def timeline_home(request):
    # Latest first, matching the models' default ordering (-start_date).
    profile = Profile.objects.first()
    experiences = Experience.objects.all()
    education = Education.objects.all()
    languages = Language.objects.all()
    return render(
        request,
        "timeline/home.html",
        {
            "profile": profile,
            "experiences": experiences,
            "education": education,
            "languages": languages,
        },
    )

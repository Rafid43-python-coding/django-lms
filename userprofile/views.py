from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm

@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, "userprofile/student_profile.html", {"profile": profile})

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "userprofile/edit_profile.html", {"form": form})


@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(
        request,
        "userprofile/student_profile.html",
        {"profile": profile}
    )


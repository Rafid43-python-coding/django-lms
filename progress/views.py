from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import StudentProgress

@login_required
def progress_dashboard(request):
    progress_list = StudentProgress.objects.filter(student=request.user)

    return render(request, "progress.html", {
        "progress_list": progress_list
    })


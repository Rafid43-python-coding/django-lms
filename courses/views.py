from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from reportlab.pdfgen import canvas

from .models import Course, Enrollment
from reportlab.lib.colors import navy,gold,black,grey
from datetime import date
from reportlab.lib.utils import ImageReader
import os 
from django.conf import settings
from django.contrib.auth.decorators import login_required

from .models import Rating
from django.db.models import Avg
from .models import Course, Rating
from .forms import RatingForm
from django import forms
from .models import Rating
from progress.models import StudentProgress



def home(request):
    return render(request, "home.html")


def course_list(request):
    query = request.GET.get("q")

    if query:
        courses = Course.objects.filter(title__icontains=query)
    else:
        courses = Course.objects.all()

    return render(request, "courses.html", {
        "courses": courses
    })


def course_detail(request, id):
    course = get_object_or_404(Course, id=id)

    return render(request, "course_detail.html", {
        "course": course
    })


@login_required
def enroll_course(request, id):
    course = get_object_or_404(Course, id=id)

    Enrollment.objects.get_or_create(
        
        student=request.user,
        course=course
    )
    StudentProgress.object.get_or_create(
        
        student=request.user,
        course=course
    )

    return redirect("my_courses")


@login_required
def my_courses(request):
    enrollments = Enrollment.objects.filter(
        student=request.user
    )

    return render(request, "my_courses.html", {
        "enrollments": enrollments
    })


@login_required
def dashboard(request):
    enrollments = Enrollment.objects.filter(
        student=request.user
    )

    return render(request, "dashboard.html", {
        "enrollments": enrollments,
        "total_courses": enrollments.count(),
    })


@login_required
def complete_course(request, id):
    enrollment = get_object_or_404(
        Enrollment,
        id=id,
        student=request.user
    )

    enrollment.completed = True
    enrollment.save()

    return redirect("my_courses")


@login_required
def download_certificate(request, id):
    enrollment = get_object_or_404(
        Enrollment,
        id=id,
        student=request.user
    )

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        'attachment; filename="certificate.pdf"'
    )

    pdf = canvas.Canvas(response)

    pdf.setTitle("Certificate")

    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawString(100, 800, "COURSE COMPLETION CERTIFICATE")

    pdf.setFont("Helvetica", 16)
    pdf.drawString(
        100, 740,
        f"Student : {request.user.username}"
    )

    pdf.drawString(
        100, 710,
        f"Course : {enrollment.course.title}"
    )

    pdf.drawString(
        100, 680,
        f"Instructor : {enrollment.course.instructor}"
    )

    pdf.drawString(
        100, 650,
        "Congratulations on successfully completing the course!"
    )

    pdf.showPage()
    pdf.save()

    return response

def certificate(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'

    p = canvas.Canvas(response)

    # Background Image
    bg_path = os.path.join(
        settings.BASE_DIR,
        "static",
        "images",
        "certificate_bg.png"
    )
    print(bg_path)
    print(os.path.exists(bg_path))

    if os.path.exists(bg_path):
      print("Image Found:", bg_path)
      bg = ImageReader(bg_path)
      p.drawImage(bg, 0, 0, width=595, height=842)
    else:
     print("Image NOT Found:", bg_path)

    # Student Name
    p.setFillColor(navy)
    p.setFont("Helvetica-Bold", 26)
    p.drawCentredString(297, 400, enrollment.student.username)

    # Course Name
    p.setFillColor(black)
    p.setFont("Helvetica-Bold", 20)
    p.drawCentredString(297, 315, enrollment.course.title)

    # Completion Date
    p.setFont("Helvetica", 14)
    p.drawString(70, 90, f"Date of Completion : {date.today()}")

    # Instructor
    p.setFont("Helvetica", 16)
    p.drawString(120, 100, str(enrollment.course.instructor))

    # Administrator
    p.drawString(420, 170, "Administrator")

    #Date
    p.drawCentredString(470,100,str(date.today()))

    p.save()

    return response



@login_required
def profile(request):
    enrollments = Enrollment.objects.filter(student=request.user)

    context = {
        "user": request.user,
        "enrollments": enrollments,
        "completed": enrollments.filter(completed=True).count(),
        "total": enrollments.count(),
    }

    return render(request, "profile.html", context)





@login_required
def rate_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == "POST":
        stars = int(request.POST.get("stars"))

        Rating.objects.update_or_create(
            user=request.user,
            course=course,
            defaults={"stars": stars}
        )

        return redirect("my_courses")



def courses(request):
    courses = Course.objects.all()

    for course in courses:
        avg = Rating.objects.filter(course=course).aggregate(
            Avg("stars")
        )["stars__avg"]

        course.avg_rating = round(avg, 1) if avg else 0

    return render(request, "courses.html", {
        "courses": courses
    })





class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating', 'review']

        widgets = {
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 5
            }),
            'review': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your review...'
            }),
        }





@login_required
def add_rating(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    rating, created = Rating.objects.get_or_create(
        course=course,
        user=request.user
    )

    if request.method == "POST":
        form = RatingForm(request.POST, instance=rating)

        if form.is_valid():
            form.save()
            return redirect('course_detail', course_id=course.id)
    else:
        form = RatingForm(instance=rating)

    return render(request, "add_rating.html", {
        "form": form,
        "course": course
    })

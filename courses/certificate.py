from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import Enrollment

def generate_certificate(request, enrollment_id):
    enrollment = Enrollment.objects.get(id=enrollment_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'

    p = canvas.Canvas(response)

    p.setFont("Helvetica-Bold", 24)
    p.drawString(140, 750, "Certificate of Completion")

    p.setFont("Helvetica", 16)
    p.drawString(
        100,
        700,
        f"This certifies that {enrollment.student.username}"
    )

    p.drawString(
        100,
        670,
        f"has successfully completed the course"
    )

    p.setFont("Helvetica-Bold", 18)
    p.drawString(
        100,
        640,
        enrollment.course.title
    )

    p.drawString(100, 590, "Congratulations!")

    p.showPage()
    p.save()

    return response

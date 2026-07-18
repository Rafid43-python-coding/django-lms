from django.db import models
from django.contrib.auth.models import User
from courses.models import Course

class StudentProgress(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    total_lessons = models.PositiveIntegerField(default=10)
    completed_lessons = models.PositiveIntegerField(default=0)

    progress = models.PositiveIntegerField(default=0)
    completed = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.total_lessons > 0:
            self.progress = int(
                (self.completed_lessons / self.total_lessons) * 100
            )

        if self.progress >= 100:
            self.progress = 100
            self.completed = True

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.username} - {self.course.title}"


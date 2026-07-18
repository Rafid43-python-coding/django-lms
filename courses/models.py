from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES = [
    ("Programming", "Programming"),
    ("Web Development", "Web Development"),
    ("AI", "AI"),
    ("Data Science", "Data Science"),
]


class Course(models.Model):
    title = models.CharField(max_length=100)
    instructor = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to="courses/", blank=True, null=True)
    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
        default="Programming"
    )

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.username} - {self.course.title}"




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="course_profile")
    image = models.ImageField(upload_to="profile/", default="profile/default.png")

    def __str__(self):
        return self.user.username


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    stars = models.IntegerField(default=5)

    def __str__(self):
        return f"{self.user.username} - {self.course.title} - {self.stars}"
    



class Rating(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="ratings"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    rating = models.IntegerField(default=5)
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('course', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"


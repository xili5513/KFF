from django.db import models
from django.contrib.auth.models import AbstractUser


RATING_CHOICES = (
    ('Best', 'Best'),
    ('Good', 'Good'),
    ('Avoid', 'Avoid'),
)
GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)
AGE_CHOICES = (
    ('Under 18', 'Under 18'),
    ('18-29', '18-29'),
    ('30-39', '30-39'),
    ('40-49', '40-49'),
    ('50-59', '50-59'),
    ('60+', '60+'),
)


class CustomUser(AbstractUser):
    gender = models.CharField(max_length=20, choices=GENDER, default='Under 18')
    age = models.CharField(max_length=20, choices=AGE_CHOICES, default='Male')

    def __str__(self):
        return self.username


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    rating = models.CharField(max_length=20, choices=RATING_CHOICES, default='Best', blank=True, null=True)
    product_name = models.CharField(max_length=400, blank=True, default='')
    product_category = models.CharField(max_length=400, blank=True, default='')
    accreditation = models.CharField(max_length=400, blank=True, default='')
    availability = models.CharField(max_length=1000, blank=True, default='')
    location = models.CharField(max_length=400, blank=True, default='')
    address = models.CharField(max_length=400, blank=True, default='')
    owner = models.ForeignKey('snippets.CustomUser', related_name='snippets', on_delete=models.CASCADE)

    class Meta:
        ordering = ('created',)



# class Member(models.Model):
#     created = models.DateTimeField(auto_now_add=True)
#     username = models.CharField(max_length=20, primary_key=True, null=False)
#     password = models.CharField(max_length=20)
#     gender = models.CharField(max_length=20, choices=GENDER)
#     age = models.CharField(max_length=20, choices=AGE_CHOICES)
#     user_email = models.EmailField(max_length=255, blank=True, unique=True)
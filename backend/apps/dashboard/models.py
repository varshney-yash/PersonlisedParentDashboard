from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    PARENT_TYPE_CHOICES = [
        (1, 'First-time'),
        (2, 'Experienced'),
    ]

    parent_type = models.IntegerField(choices=PARENT_TYPE_CHOICES)


class Child(models.Model):
    GENDER_CHOICES = [
        (1, 'Male'),
        (2, 'Female'),
        (3, 'Other'),
    ]

    AGE_GROUPS = [
        (1, 'Infant'),
        (2, 'Toddler'),
        (3, 'Preschool'),
        (4, 'School-age'),
        (5, 'Teen'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='children')
    name = models.CharField(max_length=50)
    gender = models.IntegerField(choices=GENDER_CHOICES)
    birth_date = models.DateField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True, editable=False)
    age_group = models.IntegerField(choices=AGE_GROUPS, blank=True, editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if isinstance(self.birth_date, str):
            self.birth_date = datetime.strptime(self.birth_date, '%Y-%m-%d').date()
        self.age = self.calculate_age()
        self.age_group = self.calculate_age_group()
        super().save(*args, **kwargs)

    def calculate_age(self):
        if self.birth_date:
            today = timezone.now().date()
            return (today - self.birth_date).days // 365
        return None

    def calculate_age_group(self):
        if self.age is not None:
            if self.age <= 1:
                return 1
            elif self.age <= 3:
                return 2
            elif self.age <= 5:
                return 3
            elif self.age <= 12:
                return 4
            else:
                return 5
        return None


class Keyword(models.Model):
    ENTITY_TYPE_CHOICES = [
        ("age_group", "Age Group"),
        ("interests", "Interests"),
        ("gender", "Gender"),
        ("experience_level", "Experience Level"),
    ]

    entity_type = models.CharField(max_length=20, choices=ENTITY_TYPE_CHOICES)
    entity_id = models.IntegerField()
    keyword_name = models.CharField(max_length=50)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.keyword_name


class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    keywords = models.ManyToManyField(Keyword, through='BlogKeywordMapping', related_name='blogs')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='created_blogs', null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='updated_blogs', null=True, blank=True)

    def __str__(self):
        return self.title


class Vlog(models.Model):
    title = models.CharField(max_length=200)
    video_url = models.URLField()
    keywords = models.ManyToManyField(Keyword, through='VlogKeywordMapping', related_name='vlogs')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='created_vlogs', null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='updated_vlogs', null=True, blank=True)

    def __str__(self):
        return self.title


class BlogKeywordMapping(models.Model):
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.keyword.keyword_name} mapping for {self.blog.title}"


class VlogKeywordMapping(models.Model):
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
    vlog = models.ForeignKey(Vlog, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.keyword.keyword_name} mapping for {self.vlog.title}"

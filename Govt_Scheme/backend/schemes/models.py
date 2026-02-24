# Create your models here.
from django.db import models

class Scheme(models.Model):
    SCHEME_TYPE = [
        ("Central", "Central"),
        ("State", "State"),
    ]

    CATEGORY = [
        ("Education", "Education"),
        ("Health", "Health"),
        ("Women", "Women"),
        ("Employment", "Employment"),
        ("Agriculture", "Agriculture"),
        ("Housing", "Housing"),
    ]

    name = models.CharField(max_length=200)
    scheme_type = models.CharField(max_length=10, choices=SCHEME_TYPE)
    category = models.CharField(max_length=20, choices=CATEGORY)

    min_age = models.IntegerField()
    max_age = models.IntegerField()
    income_limit = models.IntegerField()

    gender = models.CharField(max_length=10, default="Any")
    caste = models.CharField(max_length=20, default="Any")
    state = models.CharField(max_length=50)

    benefit_amount = models.IntegerField()
    priority_score = models.FloatField()

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

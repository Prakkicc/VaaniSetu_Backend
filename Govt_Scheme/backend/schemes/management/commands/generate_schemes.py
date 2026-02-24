from django.core.management.base import BaseCommand
from schemes.models import Scheme
import random

class Command(BaseCommand):
    help = "Generate realistic government schemes"

    def handle(self, *args, **kwargs):
        scheme_types = [
            "Education", "Health", "Agriculture", "Employment",
            "Women Welfare", "Housing", "Senior Citizen", "Startup"
        ]

        states = [
            "All India", "Odisha", "Bihar", "UP", "MP",
            "Rajasthan", "West Bengal", "Maharashtra"
        ]

        for i in range(200):
            Scheme.objects.create(
                name=f"Government Scheme {i+1}",
                scheme_type=random.choice(scheme_types),
                benefit_amount=random.randint(5000, 500000),
                priority_score=round(random.uniform(0.3, 1.0), 2),
                state=random.choice(states),
                min_age=random.randint(18, 30),
                max_age=random.randint(40, 65),
                income_limit=random.randint(100000, 800000)
            )

        self.stdout.write(self.style.SUCCESS("✅ 200 schemes generated successfully"))

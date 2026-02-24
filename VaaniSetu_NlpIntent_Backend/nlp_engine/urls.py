from django.urls import path
from .views import ProcessTextView

urlpatterns = [
    # The full URL will be: http://<your-domain>/api/nlp/process-intent/
    path('process-intent/', ProcessTextView.as_view(), name='process_intent'),
]
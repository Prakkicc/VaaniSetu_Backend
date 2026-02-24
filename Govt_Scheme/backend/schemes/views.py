from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Scheme
from .serializers import SchemeSerializer, UserProfileSerializer

@api_view(['GET'])
def scheme_list(request):
    schemes = Scheme.objects.all()
    serializer = SchemeSerializer(schemes, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def recommend_schemes(request):
    serializer = UserProfileSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.validated_data

    age = user['age']
    income = user['income']
    gender = user['gender']
    caste = user['caste']
    state = user['state']
    scheme_type = user.get('scheme_type')

    # Rule-based filtering
    schemes = Scheme.objects.filter(
        min_age__lte=age,
        max_age__gte=age,
        income_limit__gte=income
    )

    if scheme_type:
        schemes = schemes.filter(scheme_type=scheme_type)

    ranked = []

    for scheme in schemes:
        score = 0

        if scheme.state == state:
            score += 2

        if scheme.scheme_type == scheme_type:
            score += 2

        # Higher benefit → higher score
        score += scheme.benefit_amount / 100000  

        # Age closer to center
        mid_age = (scheme.min_age + scheme.max_age) / 2
        if abs(age - mid_age) < 5:
            score += 1

        scheme.priority_score = round(score, 2)
        scheme.save()

        ranked.append(scheme)

    ranked = sorted(ranked, key=lambda x: x.priority_score, reverse=True)

    return Response(SchemeSerializer(ranked, many=True).data)

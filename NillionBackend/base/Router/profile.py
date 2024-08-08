from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Profile
from base.profiles.serializers import ProfileSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

@api_view(['POST'])
def create_profile(request):
    serializer = ProfileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_all_profiles(request):
    profiles = Profile.objects.all()
    serializer = ProfileSerializer(profiles, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_profile_by_address(request, address):
    try:
        profile = Profile.objects.get(address=address)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_matching_profiles(request, address):
    try:
        user_profile = Profile.objects.get(address=address)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Retrieve all other profiles
    all_profiles = Profile.objects.exclude(address=address)

    # Filter profiles based on the "looking for" gender
    matching_profiles = all_profiles.filter(gender=user_profile.looking_for)

    # Weights for each matching criterion
    weights = {
        'location': 0.2,
        'age': 0.1,
        'interest': 0.3,
        'work': 0.1,
        'edu': 0.1,
        'zodiac': 0.2
    }

    # Calculate matching percentage
    def calculate_match_percentage(user, profile):
        match_percentage = 0

        # Location match
        if user.location == profile.location:
            match_percentage += weights['location'] * 100

        # Age match (within 5 years)
        age_difference = abs(user.age - profile.age)
        if age_difference <= 5:
            match_percentage += weights['age'] * (100 - (age_difference * 10))

        # Interest match
        shared_interests = set(user.interest).intersection(set(profile.interest))
        total_interests = set(user.interest).union(set(profile.interest))
        interest_match_percentage = (len(shared_interests) / len(total_interests)) * 100 if total_interests else 0
        match_percentage += weights['interest'] * interest_match_percentage

        # Work match
        if user.work == profile.work:
            match_percentage += weights['work'] * 100

        # Education match
        if user.edu == profile.edu:
            match_percentage += weights['edu'] * 100

        # Zodiac match
        if user.zodiac == profile.zodiac:
            match_percentage += weights['zodiac'] * 100

        return match_percentage

    # Prepare the matching list with percentages
    matches = []
    for profile in matching_profiles:
        match_percentage = calculate_match_percentage(user_profile, profile)
        matches.append({
            'profile': ProfileSerializer(profile).data,
            'match_percentage': match_percentage
        })

    # Sort matches by percentage in descending order
    matches = sorted(matches, key=lambda x: x['match_percentage'], reverse=True)

    return Response(matches, status=status.HTTP_200_OK)
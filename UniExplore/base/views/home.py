from ..models import Category, Challenges, Responses
from django.shortcuts import render
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages
from django.forms import ValidationError
import json
from random import choice
"""
    Authors: Michael Hills
    Description: View for the main homepage
"""
def home(request):
    categories = Category.objects.all()

    unexpired_challenges = Challenges.objects.all()

    if (len(
            unexpired_challenges
            .exclude(Q(is_weekly_challenge=False))
            .filter(Q(expires_on__gt=timezone.now()))
            ) == 0):
        print("No weekly challenges! Generating...")
        generate_weekly_challenges(request)

    # Get the filter from the ?q= in the URL
    q = request.GET.get('q') if request.GET.get('q') is not None else ''

    # Get all challenges, not done by the current user
    if request.user.is_authenticated:
        responses = Responses.objects.filter(user=request.user).values_list('challenge_id')

        challenges = Challenges.objects.exclude(id__in=responses).filter(
            Q(category__name__icontains=q),
            Q(expires_on__gt=timezone.now()) # This makes sure expired aren'trendered
            ).order_by('-created')

        
    else:
        challenges = Challenges.objects.filter(
            Q(category__name__icontains=q), 
            Q(expires_on__gt=timezone.now()) # This makes sure expired aren'trendered
            ).order_by('-created')
        # add locations to map

        # Variables to pass to the database
        

    context = {'categories': categories, 'challenges': challenges}

    return render(request, 'base/home.html', context)

def generate_weekly_challenges(request):
    challenge_json = json.load(open('base/resources/default_challenges.json'))
    location_json = json.load(open('base/resources/sample_locations.json'))

    weekly_category = Category.objects.filter(Q(name="Weekly")).first()

    expiry_date = timezone.now() + timezone.timedelta(days=7)

    if(weekly_category == None):
        messages.warning(request, 'ERROR: No weekly challenge category! Contact admin to create one.')
        raise ValidationError("No weekly challenge category! Contact admin to create one.")

    for i in range(5):
        selected_challenge = choice(challenge_json)
        selected_location = choice(location_json)

        new_challenge = Challenges(
            name = selected_location['name'],
            category = weekly_category,
            points = selected_challenge['points'],
            description = (selected_challenge['name'] + " "  +selected_challenge['description']),
            expires_on = expiry_date,
            is_weekly_challenge = True,
            lat = selected_location['lat'],
            long = selected_location['long']
        )

        new_challenge.save()
    
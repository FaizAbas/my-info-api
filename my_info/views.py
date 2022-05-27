import json
import urllib.parse as urlparse

from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework import status

from my_info.client import MyInfoClient
from my_info.security import get_decoded_access_token, get_decrypted_person_data


def my_info_start_view(request):
    """
    View for establishing connection with My Info API and redirect user to My Info Website
    """
    # Initialize connection with My Info
    client = MyInfoClient()
    my_info_url = client.get_authorise_url(state="blahblah")
    print(my_info_url)
    return HttpResponseRedirect(my_info_url)


def my_info_view(request):
    """
    View for displaying My Info API response
    """

    query_string = urlparse.parse_qs(request.GET.urlencode())
    codes = query_string['code']

    # Initialize connection with My Info
    client = MyInfoClient()

    my_info_responses = []

    template = loader.get_template('my_info/my_info_view.html')

    try:
        for code in codes:
            # Getting access token with code
            resp = client.get_access_token(code)
            access_token = resp["access_token"]

            # Decoding access token
            decoded_access_token = get_decoded_access_token(access_token)
            uinfin = decoded_access_token["sub"]

            # Getting person data
            resp = client.get_person(uinfin=uinfin, access_token=access_token)
            my_info_responses.append(clean_response(get_decrypted_person_data(resp)))
    except Exception as e:
        return HttpResponse(template.render({'error_code': e}, request))

    context = {
        'customers': my_info_responses,
    }

    return HttpResponse(template.render(context, request))

def clean_response(response) -> dict:
    """
    Clean the response from My Info to be used for template rendering
    """

    for noa in response['noahistory']['noas']:
        noa['yearofassessment']['value'] = noa['yearofassessment']['value'][0:5].replace(',','')

    return response

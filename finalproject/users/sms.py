import requests
from django.http import JsonResponse


def send_otp(phone):
    user_phone = phone
    url = "http://2factor.in/API/V1/8702453c-dbe0-11eb-8089-0200cd936042/SMS/" + \
        user_phone + "/AUTOGEN/OTPSEND"
    response = requests.request("GET", url)
    data = response.json()
    # otp_session_data is stored in session.
    print("OTP sent successfully")
    return data['Details']


def otp_verification(request, otp):
    user_otp = otp
    url = "http://2factor.in/API/V1/8702453c-dbe0-11eb-8089-0200cd936042/SMS/VERIFY/" + \
        request.session['otp_session_data'] + "/" + user_otp + ""
    # otp_session_data is fetched from session.
    response = requests.request("GET", url)
    data = response.json()
    if data['Status'] == "Success":
        response_data = {'Message': 'Success'}
    else:
        response_data = {'Message': 'Failed'}
    return response_data

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import sys
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException


class SendSMS(APIView):
    def post(self, request):
        receiver = request.data['receiver']
        message = request.data['message']

        api_key = "NCSGLMHSQ2FTVZUA"
        api_secret = "2ZNM5ZPZR07QHSLHVIFAH3XZR1GAGM2F"

        params = dict()
        params['type'] = 'sms'  # Message type ( sms, lms, mms, ata )
        params['to'] = receiver  # Recipients Number '01000000000,01000000001'
        params['from'] = '01029953874'  # Sender number
        params['text'] = message  # Message

        cool = Message(api_key, api_secret)
        cool.send(params)
        return Response(status=status.HTTP_200_OK)

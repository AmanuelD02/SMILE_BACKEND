from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
# Create your views here.


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(request.data)
        serializer.is_valid()
        serializer.save()
        

        return Response(serializer.data)


class SendOTPView(APIView):
    def post(self, request):
        account_sid = ""
        auth_token = ""
        client = Client(account_sid, auth_token)
        send_to = request.data['number']

        otp  = generateOTP()


        body = f"Your PINCODE is {str(otp)}" 
        message = client.messages.create(from_="", body=body, to = send_to)
        if message.sid:
            return Response('ok')
        return Response("Error")




def generateOTP():
    import random
    return random.randrange(10000,99999)
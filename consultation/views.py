from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'consultation/index.html')


def consultation_chat(request, consultation_chat_id):
    return render(request, 'consultation/room.html', {
        'chat_name': consultation_chat_id
    })

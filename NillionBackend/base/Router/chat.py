from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Profile, Chat, Message
from base.profiles.serializers import ProfileSerializer, ChatSerializer, MessageSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

@api_view(['GET'])
def create_chat(request):
    participants_addresses = request.query_params.getlist('participants')
    participants = Profile.objects.filter(address__in=participants_addresses)

    if participants.count() != len(participants_addresses):
        return Response({'error': 'One or more participants not found.'}, status=status.HTTP_400_BAD_REQUEST)

    chat = Chat(participant_addresses=participants_addresses)
    chat.save()

    return Response(ChatSerializer(chat).data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def send_message(request):
    chat_id = request.query_params.get('chat_id')
    sender_address = request.query_params.get('sender_address')
    content = request.query_params.get('content')

    try:
        chat = Chat.objects.get(id=chat_id)
        sender = Profile.objects.get(address=sender_address)
    except Chat.DoesNotExist:
        return Response({'error': 'Chat not found.'}, status=status.HTTP_400_BAD_REQUEST)
    except Profile.DoesNotExist:
        return Response({'error': 'Sender not found.'}, status=status.HTTP_400_BAD_REQUEST)

    message = Message(chat_id=chat.id, sender_address=sender_address, content=content)
    message.save()

    return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)

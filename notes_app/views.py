from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework import status, permissions
from django.contrib.auth import authenticate
from .models import Note, sharedNote, noteHistory
from .serializers import UserSeriaizer, NoteSerializer, SharedNoteSerializer, NoteHistorySerializer
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request): # Allows new users to sign up by providing their details
    '''
    The view validates the user data using the UserSerializer and,
    if valid, creates a new User instance along with an authentication token.
    '''
    serializer = UserSeriaizer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        # if valid in return we will be provided with a token and a success message
        return Response({'token': token.key, 'message': "Registration Succesful"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request): # Authenticates users by their username and password.
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        # If authentication is successful, it retrieves or creates an authentication token for the user and returned in a Json response
        return Response({'token': token.key, 'message': 'Login successful'}, status=status.HTTP_200_OK)
    return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_note(request): # Allows authenticated users to create a new note.
    serializer = NoteSerializer(data=request.data, context={'request': request})
    # A JSON response with the created note data if successful, otherwise, returns error details.
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_note(request, id): # Retrieves a specific note by its ID, ensuring that the requesting user is the owner of the note.
    # A JSON response with the requested note's data if found; otherwise, returns a message indicating the note is not found.
    try:
        note = Note.objects.get(pk=id, owner=request.user)
        serializer = NoteSerializer(note)
        return Response(serializer.data)
    except Note.DoesNotExist:
        return Response({'message': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)
    


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def share_note(request):
    note_id = request.data.get('note_id')
    usernames = request.data.get('users', [])  # Default to an empty list if 'users' is not provided

    try:
        note = Note.objects.get(pk=note_id, owner=request.user)
        # Ensure there is a sharedNote instance for this note
        shared_note, created = sharedNote.objects.get_or_create(note=note)

        # Retrieve all user instances based on the provided usernames
        users_to_share_with = User.objects.filter(username__in=usernames)

        # Use add() to associate these users with the sharedNote instance
        shared_note.shared_with.add(*users_to_share_with)

        return Response({'message': 'Note shared successfully'}, status=status.HTTP_200_OK)
    except Note.DoesNotExist:
        return Response({'message': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        return Response({'message': 'One or more specified users do not exist'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_note(request, id): # Allows users to update a note they own.
    try:
        note = Note.objects.get(pk=id, owner=request.user)
        previous_content = note.content
        serializer = NoteSerializer(note, data=request.data, partial=True)
        # return he updated note data if successful otherwise eroor and status code
        if serializer.is_valid():
            serializer.save()

            noteHistory.objects.create(note=note, content=previous_content)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Note.DoesNotExist:
        return Response({'message': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_note_version_history(request, id): # Retrieves the version history of a specific note owned by the requesting user.
    try:
        note = Note.objects.get(pk=id, owner=request.user)
        history = noteHistory.objects.filter(note=note).order_by('-updated_time')
        serializer = NoteHistorySerializer(history, many=True)
        # A list of the note's version histories if found; otherwise, returns a message indicating the note is not found.
        return Response(serializer.data)
    except Note.DoesNotExist:
        return Response({'message': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)
    
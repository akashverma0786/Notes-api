from rest_framework import serializers
from .models import Note, sharedNote, noteHistory
from django.contrib.auth.models import User

class UserSeriaizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'
        read_only_fields = ['owner', 'created_time', 'updated_time']


class SharedNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = sharedNote
        fields = '__all__'


class NoteHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = noteHistory
        fields = '__all__'
        
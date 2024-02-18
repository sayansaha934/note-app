# serializers.py
from rest_framework import serializers
from .models import Note, NoteVersion

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'description', 'created_at', 'updated_at', 'created_by', 'updated_by')


class UpdateNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('description','updated_at','updated_by')

class ShareNoteSerializer(serializers.Serializer):
    note_id = serializers.UUIDField()
    user_ids = serializers.ListField(child=serializers.UUIDField())

class NoteVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteVersion
        fields = '__all__'
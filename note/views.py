# views.py
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from .models import Note, NoteUserMap, NoteVersion
from .serializers import (
    NoteSerializer,
    UpdateNoteSerializer,
    ShareNoteSerializer,
    NoteVersionSerializer,
)


class CreateNoteView(generics.CreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Get the authenticated user from the request
        user = request.user

        # Attach the user ID to the data before creating the note
        request.data["created_by"] = user.id
        request.data["updated_by"] = user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        NoteVersion.objects.create(
            note_id=serializer.data["id"],
            user_id=user.id,
            description=request.data["description"],
        )
        NoteUserMap.objects.create(note_id=serializer.data["id"], user_id=user.id)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class UpdateNoteView(generics.UpdateAPIView):
    queryset = Note.objects.all()
    serializer_class = UpdateNoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        # Ensure request.user is available and has an ID
        if not request.user or not request.user.id:
            return Response(
                {"error": "Invalid user"}, status=status.HTTP_400_BAD_REQUEST
            )

        instance = self.get_object()

        # Check if the user updating the note is the same user who created it
        if not NoteUserMap.objects.filter(
            note_id=instance.id, user_id=request.user.id
        ).exists():
            return Response(
                {"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
            )

        # Update the updated_by field
        request.data["updated_by"] = request.user.id

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        NoteVersion.objects.create(
            note_id=instance.id,
            user_id=request.user.id,
            description=request.data["description"],
        )
        self.perform_update(serializer)

        return Response(serializer.data)


class GetNoteView(generics.RetrieveAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        # Ensure request.user is available and has an ID
        if not request.user or not request.user.id:
            return Response(
                {"error": "Invalid user"}, status=status.HTTP_400_BAD_REQUEST
            )

        instance = self.get_object()

        # Check if the user has permission to view the note
        if request.user.id != instance.created_by:
            # Check if there's a mapping for the given note and user
            if not NoteUserMap.objects.filter(
                note_id=instance.id, user_id=request.user.id
            ).exists():
                return Response(
                    {"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
                )

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ShareNoteView(APIView):
    serializer_class = ShareNoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ShareNoteSerializer(data=request.data)
        if serializer.is_valid():
            note_id = serializer.validated_data["note_id"]
            user_ids = serializer.validated_data["user_ids"]
            # Check if the note is created by the logged-in user
            if not Note.objects.filter(id=note_id, created_by=request.user.id).exists():
                return Response(
                    {"detail": "You are not allowed to share this note."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Create NoteUserMap instances for each user
            for user_id in user_ids:
                NoteUserMap.objects.create(note_id=note_id, user_id=user_id)

            return Response(
                {"detail": "Notes shared successfully"}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetNoteVersionView(generics.ListAPIView):
    serializer_class = NoteVersionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Retrieve the note_id from the URL parameters
        note_id = self.kwargs.get("note_id")

        # Ensure request.user is available and has an ID
        if not self.request.user or not self.request.user.id:
            raise PermissionDenied(detail="Invalid user")

        if not NoteUserMap.objects.filter(
            note_id=note_id, user_id=self.request.user.id
        ).exists():
            raise PermissionDenied(detail="Permission denied")

        # Add any additional filtering based on your requirements
        queryset = NoteVersion.objects.filter(
            note_id=note_id
        )

        return queryset

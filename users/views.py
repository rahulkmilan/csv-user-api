import csv
import io

from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from .serializers import CSVUploadSerializer, UserSerializer
from .models import User


class UploadCSVView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = CSVUploadSerializer

    def post(self, request, *args, **kwargs):

        upload_serializer = CSVUploadSerializer(data=request.data)

        if not upload_serializer.is_valid():
            return Response(
                upload_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        file = upload_serializer.validated_data["file"]

        if not file.name.endswith(".csv"):
            return Response(
                {"error": "Only .csv files are allowed."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            decoded_file = file.read().decode("utf-8")
        except UnicodeDecodeError:
            return Response(
                {"error": "Invalid file encoding. Use UTF-8."},
                status=status.HTTP_400_BAD_REQUEST
            )

        io_string = io.StringIO(decoded_file)
        reader = csv.DictReader(io_string)

        saved_count = 0
        rejected_count = 0
        errors = []

        valid_users = []

        existing_emails = set(
            User.objects.values_list("email", flat=True)
        )

        for index, row in enumerate(reader, start=1):

            user_serializer = UserSerializer(data=row)

            if user_serializer.is_valid():
                email = user_serializer.validated_data["email"]

                if email in existing_emails:
                    rejected_count += 1
                    errors.append({
                        "row": index,
                        "error": "Duplicate email skipped."
                    })
                    continue

                valid_users.append(
                    User(**user_serializer.validated_data)
                )

                existing_emails.add(email)
                saved_count += 1

            else:
                rejected_count += 1
                errors.append({
                    "row": index,
                    "error": user_serializer.errors
                })

        if valid_users:
            with transaction.atomic():
                User.objects.bulk_create(valid_users)

        return Response({
            "total_saved": saved_count,
            "total_rejected": rejected_count,
            "errors": errors
        }, status=status.HTTP_200_OK)

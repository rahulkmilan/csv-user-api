import os
from django.conf import settings
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import User


class CSVUploadTest(APITestCase):

    def test_valid_csv_upload(self):

        file_path = os.path.join(settings.BASE_DIR, "sample_input.csv")

        with open(file_path, "rb") as f:
            file = SimpleUploadedFile(
                name="sample_input.csv",
                content=f.read(),
                content_type="text/csv"
            )

        response = self.client.post(
            reverse("upload-csv"),
            {"file": file},
            format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(User.objects.count(), 0)

    def test_invalid_extension(self):

        file_path = os.path.join(settings.BASE_DIR, "sample_input.csv")

        with open(file_path, "rb") as f:
            file = SimpleUploadedFile(
                name="sample_input.txt",
                content=f.read(),
                content_type="text/plain"
            )

        response = self.client.post(
            reverse("upload-csv"),
            {"file": file},
            format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_email(self):
        file_path = os.path.join(settings.BASE_DIR, "sample_input.csv")

        with open(file_path, "rb") as f:
            file = SimpleUploadedFile(
                name="sample_input.csv",
                content=f.read(),
                content_type="text/csv"
            )

        self.client.post(reverse("upload-csv"), {"file": file}, format="multipart")

        with open(file_path, "rb") as f:
            file = SimpleUploadedFile(
                name="sample_input.csv",
                content=f.read(),
                content_type="text/csv"
            )

        response = self.client.post(reverse("upload-csv"), {"file": file}, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("total_rejected", response.data)

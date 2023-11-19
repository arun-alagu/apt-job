from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import EducationDetail

from job_seeker.serializers import EducationDetailSerializer

EDUCATION_DETAIL_URL = reverse('my:educationdetail-list')

class PublicEducationDetailApiTests(TestCase):
    """Test the publicly available education details API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test the login required to access endpoint"""

        res = self.client.get(EDUCATION_DETAIL_URL)

        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)

class PrivateEducationDetailApiTests(TestCase):
    """Test the private education detail API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@example.com",
            "testpassword",
        )
        self.client.force_authenticate(self.user)

    def test_reterive_education_detail_list(self):
        """Test retrieving a list of education details"""

        EducationDetail.objects.create(
            user = self.user,
            certified_degree_name = "B.sc",
            major = "Computer Science",
            institute_university_name = "Abc College of Technology",
            start_year = 2007,
            complete_year = 2010,
            percentage = 86.9,
            cgpa = 8.69,
        )

        EducationDetail.objects.create(
            user = self.user,
            certified_degree_name = "MCA",
            major = "Computer Applications",
            institute_university_name = "Abc College of Technology",
            start_year = 2010,
            complete_year = 2012,
            percentage = 86.9,
            cgpa = 8.69,
        )

        res = self.client.get(EDUCATION_DETAIL_URL)

        education_details = EducationDetail.objects.all().order_by('id')
        serializer = EducationDetailSerializer(education_details, many = True)

        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_eduaction_details_limited_to_user(self):
        """Test that education details for authenticated user reterived"""

        user2 = get_user_model().objects.create_user(
            "other@example.com",
            "otherPassword"
        )

        EducationDetail.objects.create(
            user = user2,
            certified_degree_name = "B.Sc",
            major = "Computer Applications",
            institute_university_name = "Abc College of Technology",
            start_year = 2010,
            complete_year = 2013,
            percentage = 86.9,
            cgpa = 8.69,
        )

        education_detail = EducationDetail.objects.create(
            user = self.user,
            certified_degree_name = "MCA",
            major = "Computer Applications",
            institute_university_name = "Abc College of Technology",
            start_year = 2010,
            complete_year = 2012,
            percentage = 86.9,
            cgpa = 8.69,
        )

        res = self.client.get(EDUCATION_DETAIL_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data),1)
        self.assertEqual(
            res.data[0]['certified_degree_name'],
            education_detail.certified_degree_name
            )

    def test_create_education_details_successful(self):
        """Test create a new education  details"""

        payload ={
            "certified_degree_name": "B.sc",
            "major": "Computer Applications",
            "institute_university_name":"Abc College of Technology",
            "start_year": 2010,
            "complete_year": 2012,
            "percentage": 86.90,
            "cgpa": 8.69
        }

        res = self.client.post(EDUCATION_DETAIL_URL, payload)

        exists = EducationDetail.objects.filter(
            user = self.user,
            certified_degree_name = payload['certified_degree_name'],
        ).exists()
        # print(self.user, self.user.certified_degree_name)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exists)

    def test_create_education_detail_invalid(self):
        """Test creating invalid education detail"""

        payload ={
            "certified_degree_name": "",
            "major": "",
            "institute_university_name":"",
            "start_year": None,
            "complete_year": None,
            "percentage": None,
            "cgpa": None,
        }

        res = self.client.post(EDUCATION_DETAIL_URL, payload=payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)





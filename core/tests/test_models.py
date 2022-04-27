from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models, signals

def sample_user(email='test@londonappdev.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)

class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""

        email = "test@example.com"
        password = "Testpassword"
        user = get_user_model().objects.create_user(
            email=email,
             password=password
            )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""

        email = "test@LONDONAPPDEV.COM"
        user = get_user_model().objects.create_user(email, "test123")

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "test123")
    
    def test_create_new_superuser(self):
        """Test creating a new super user raises error"""

        user = get_user_model().objects.create_superuser(
            "test@gmail.com",
            "test123",
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='full-time'
        )

        self.assertEqual(str(tag), tag.name)

    def test_seeker_profile_str(self):
        """Test whether seeker profile is created"""

        seeker_profile = models.SeekerProfile.objects.create(
            user = sample_user(),
            first_name = "test",
            last_name = "test",
            date_of_birth = "1995-10-05",
            gender = "M",
            address = "123, test address",
            city = "test city",
            pincode = "t123",
            phone_number = "1234567890",
            disabled = False
        )

        self.assertEqual(
            str(seeker_profile),
            seeker_profile.first_name+" "+seeker_profile.last_name
            )

    def test_gender_choices(self):
        """Test gender is selected and is in specified format"""

        with self.assertRaises(ValueError):
            seeker_profile = models.SeekerProfile.objects.create(
                user = sample_user(),
                first_name = "test",
                last_name = "test",
                date_of_birth = "1995-10-05",
                gender = 'm',
                address = "123, test address",
                city = "test city",
                pincode = "t123",
                phone_number = "1234567890",
                disabled = False
            )


    # def test_phone_number_is_unique(self):
    #     """Test phone number is unique"""

    #     seeker_profile1 = models.SeekerProfile.objects.create(
    #         user = get_user_model().objects.create_user("test1@email.com", "testpassword"),
    #         first_name = "test",
    #         last_name = "test",
    #         date_of_birth = "1995-10-05",
    #         gender = "male",
    #         address = "123, test address",
    #         city = "test city",
    #         pincode = "t123",
    #         phone_number = "1234567890",
    #         disabled = False
    #     )

    #     seeker_profile2 = models.SeekerProfile.objects.create(
    #         user = get_user_model().objects.create_user("test2@email.com", "testpassword"),
    #         first_name = "test",
    #         last_name = "test",
    #         date_of_birth = "1995-10-05",
    #         gender = "male",
    #         address = "123, test address",
    #         city = "test city",
    #         pincode = "t123",
    #         phone_number = "1254367890",
    #         disabled = False
    #     )

    #     self.assertNotEqual(
    #         seeker_profile2.phone_number,
    #         seeker_profile1.phone_number
    #         )
        

    def test_education_detail_str(self):
        """Test whether education details is created"""

        education_detail = models.EducationDetail.objects.create(
            certified_degree_name = "B.sc",
            major = "Comjid",
            institute_university_name = "dnudn",
            start_year = 1987,
            complete_year = 2667,
            percentage = 86.9,
            cgpa = 10.0,
            user = sample_user()
        )

        self.assertEqual(
            str(education_detail),
            education_detail.certified_degree_name
            )

    def test_start_year_is_less_than_complete_year(self):
        """Test whether start year is greater than complete year"""

        with self.assertRaises(ValueError):
            education_detail = models.EducationDetail.objects.create(
                certified_degree_name = "B.sc",
                major = "Comjid",
                institute_university_name = "dnudn",
                start_year = 1987,
                complete_year = 1984,
                percentage = 86.9,
                cgpa = 10.0,
                user = sample_user()
            )
                     



    # def test_job_location_str(self):
    #     """Test the job location string representation"""

    #     job_location = models.JobLocation.objects.create(
    #     user = sample_user(),
    #     street_address = '123, abc colony',
    #     city = 'xyz',
    #     state = 'asd',
    #     country = 'qwerty',
    #     zip = 123456
    #     )

    # def test_job_post_activity_str(self):
    #     """Test job post activity"""

    #     job_post_activity = models.JobPostActivity.objects.create(
    #         user = sample_user(),

    #     )
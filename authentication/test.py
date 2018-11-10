import unittest
from django.conf import settings
from django.contrib.auth.models import User
from profile.models import Student
from profile.models import Teacher
from .forms import userLoginForm, signupForm, StudentSignupForm




class RegistrationFormTests(unittest.TestCase):
    '''
    This class test the signup form by raising error text when invalidate data is inputed 
    '''  

    def test_phone_is_not_10_digit(self):
        form_data = {"gender":"MA","dob":"2018-01-01","phone":"09876543211","other_phone":"1234567890","facebook":"testing1111","postcode":4000,"street_name":"aefaerwawger","street_number":12,"suburb":"brisbnae","city":"city","state":"QLD"}
        form_data2 = {"gender":"MA","dob":"2018-01-01","phone":"098765432","other_phone":"1234567890","facebook":"testing1111","postcode":4000,"street_name":"aefaerwawger","street_number":12,"suburb":"brisbnae","city":"city","state":"QLD"}

        form = StudentSignupForm(data=form_data)
        form2 = StudentSignupForm(data=form_data2)

        self.assertFalse(form.is_valid() or form2.is_valid())

    def test_other_phone_is_not_10_digit(self):
        form_data = {"gender":"MA","dob":"2018-01-01","other_phone":"09876543211","phone":"1234567890","facebook":"testing1111","postcode":4000,"street_name":"aefaerwawger","street_number":12,"suburb":"brisbnae","city":"city","state":"QLD"}
        form_data2 = {"gender":"MA","dob":"2018-01-01","other_phone":"098765432","phone":"1234567890","facebook":"testing1111","postcode":4000,"street_name":"aefaerwawger","street_number":12,"suburb":"brisbnae","city":"city","state":"QLD"}
        form = StudentSignupForm(data=form_data)
        form2 = StudentSignupForm(data=form_data2)

        self.assertFalse(form.is_valid() or form2.is_valid())

    def test_postcode_not_only_contains_digit(self):
        form_data = {"gender":"MA","dob":"2018-01-01","phone":"0987654321","other_phone":"1234567890","facebook":"testing1111","postcode":"4000e-","street_name":"aefaerwawger","street_number":12,"suburb":"brisbnae","city":"city","state":"QLD"}
        form = StudentSignupForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_street_name_not_only_contains_character(self):
        form_data = {"gender":"MA","dob":"2018-01-01","phone":"0987654321","other_phone":"1234567890","facebook":"testing1111","postcode":4000,"street_name":"aefaerwawger2","street_number":12,"suburb":"brisbnae","city":"city","state":"QLD"}
        form = StudentSignupForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_street_number_not_only_contains_digit(self):
        form_data = {"gender":"MA","dob":"2018-01-01","phone":"0987654321","other_phone":"1234567890","facebook":"testing1111","postcode":4000,"street_name":"aefaerwawger","street_number":"12-n","suburb":"brisbnae","city":"city","state":"QLD"}
        form = StudentSignupForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_suburb_not_only_contains_character(self):
        form_data = {"gender":"MA","dob":"2018-01-01","phone":"0987654321","other_phone":"1234567890","facebook":"testing1111","postcode":4000,"street_name":"aefaerwawger","street_number":12,"suburb":"brisbnae","city":"city9-","state":"QLD"}
        form = StudentSignupForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_city_not_only_contains_character(self):
        form_data = {"gender":"MA","dob":"2018-01-01","phone":"0987654321","other_phone":"1234567890","facebook":"testing1111","postcode":4000,"street_name":"aefaerwawger","street_number":12,"suburb":"brisbnae","city":"city","state":"QLD7-"}
        form = StudentSignupForm(data=form_data)
        self.assertFalse(form.is_valid())

        
    def test_validate_accept(self):

        form_data = {"username":"testing1111", "password":"abcd1234", "password2":"abcd1234", "first_name":"abcd" ,"last_name":"abcd", "email":"abcd12343@gag.com","email2":"abcd12343@gag.com"}
        form = signupForm(data=form_data)
        self.assertTrue(form.is_valid())
       
    def test_username_is_Existed(self):
        User.objects.create(username = "abcd1234111",password = "abcd1234111",first_name = "abcd",last_name = "1234",email = "abcd123422@gag.com")
        form_data = {"username":"abcd1234111", "password":"abcd1234", "password2":"abcd1234", "first_name":"abcd" ,"last_name":"abcd", "email":"abcd1234@gag.com","email2":"abcd1234@gag.com"}
        form = signupForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_password_double_validation_not_match(self):

        form_data = {"username":"testing1112", "password":"abcd12345", "password2":"abcd1234", "first_name":"abcd" ,"last_name":"abcd", "email":"abcd1234@gag.com","email2":"abcd1234@gag.com"}
        form = signupForm(data=form_data)
        #print(form)
        self.assertFalse(form.is_valid())      

    def test_firstname_contains_not_only_character(self):

        form_data = {"username":"testing1112", "password":"abcd1234", "password2":"abcd1234", "first_name":"abcd1-" ,"last_name":"abcd", "email":"abcd1234@gag.com","email2":"abcd1234@gag.com"}
        form = signupForm(data=form_data)
        #print(form)
        self.assertFalse(form.is_valid())      

    def test_lastname_contains_not_only_character(self):

        form_data = {"username":"testing1112", "password":"abcd1234", "password2":"abcd1234", "first_name":"abcd" ,"last_name":"abcd21-", "email":"abcd1234@gag.com","email2":"abcd1234@gag.com"}
        form = signupForm(data=form_data)
        #print(form)
        self.assertFalse(form.is_valid())      
    
    def test_email_double_validation_not_match(self):

        form_data = {"username":"testing1112", "password":"abcd1234", "password2":"abcd1234", "first_name":"abcd" ,"last_name":"abcd", "email":"abcd12345@gag.com","email2":"abcd1234@gag.com"}
        form = signupForm(data=form_data)
        #print(form)
        self.assertFalse(form.is_valid())      
  
    def test_email_is_Existed(self):
        User.objects.create(username = "abcd12",password = "abcd1234111",first_name = "abcd",last_name = "1234",email = "abcd1234@gag.com")
        form_data = {"username":"testing1112", "password":"abcd1234", "password2":"abcd1234", "first_name":"abcd" ,"last_name":"abcd", "email":"abcd1234@gag.com","email2":"abcd1234@gag.com"}
        form = signupForm(data=form_data)
        #print(form)
        self.assertFalse(form.is_valid())      

    



if __name__ == '__main__':
    unittest.main()


""" 
def test_unvalidate_username_reject(self):
    self.assertEqual(User.objects.count(), 1)

    form_data = {"username":"abcd1234", "password":"abcd1234", "password2":"abcd1234", "first_name":"abcd" ,"last_name":"abcd", "email":"abcd1234@gag.com","email2":"abcd1234@gag.com"}
    form = signupForm(form_data)
    self.assertFalse(form.is_valid())
 """

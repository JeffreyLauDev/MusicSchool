from django import forms
from django.contrib.auth import authenticate, get_user_model, login, logout
from profile.models import Student



User = get_user_model()

class userLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'yourusername1234'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '*************'}))

    def clean(self, *args, **kwargs):

        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        ##user_qs = User.object.filter(username=username)
        ###if user_qs.count() == 1:
        ###   user = user_qs.first()
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Username or password is not correct")
            if not user.is_active:
                raise forms.ValidationError("This user is not longer active.")
        return super(userLoginForm, self).clean(*args, **kwargs )




class signupForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'e.g. abcd1234'}))
    email2 = forms.EmailField(label='Confirm Email', widget=forms.EmailInput(attrs={'placeholder': 'e.g. Type email again'}))
    email = forms.EmailField(label='Email address' , widget=forms.EmailInput(attrs={'placeholder': 'e.g. jeffreyla1129@gmail.com'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'e.g. Lau'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'e.g. Jeffrey'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'placeholder': 'Same password again'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'e.g. ••••••• '}))
    class Meta:  
        model = User
        fields = [
            'username',
            'password',
            'password2',
            'first_name', 
            'last_name', 
            'email',
            'email2'
        ]



    def clean_username(self):
        username = self.cleaned_data.get('username')
        user_qs = User.objects.filter(username=username)
        if user_qs.exists():
            raise forms.ValidationError("This email has already been registered")

        return username  
            

    def clean_password(self):
        password = self.cleaned_data.get('password')
        #password2 = self.cleaned_data.get('password2')

        if self.data['password'] != self.data['password2']:
            raise forms.ValidationError("password must match")

        return password

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')

        if self.data['first_name'].isalpha() != True:
            raise forms.ValidationError("Letters only")
        return first_name


    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        
        if self.data['last_name'].isalpha() != True:
            raise forms.ValidationError("Letters only")
        return last_name  
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        #email2 = self.cleaned_data.get('email2')

        if self.data['email'] != self.data['email2']:
            raise forms.ValidationError("Emails must match")
        
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("This email has already been registered")

        return email  


GENDERCHOICE = (
    ('MA', 'Male'),
    ('FE', 'Female'),
    ('OT', 'Other'),
)

STATECHOICES = (
    ('QLD', 'Queensland'),
    ('NSW', 'New South Wales'),
    ('TAS', 'Tasmania'),
    ('VIC', 'Victoria'),
    ('WAT', 'Western Australia'),
    ('SAH', 'South Australia'),
    ('NTH', 'Nothern Territory'),
)

class StudentSignupForm(forms.ModelForm):
    gender = forms.CharField(widget=forms.Select(choices=GENDERCHOICE))
    dob = forms.DateField(widget=forms.SelectDateWidget(years=range(1970, 2018)))
    phone = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'e.g 1234567890  (has to be 10 digit)'}))
    other_phone = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'placeholder': 'e.g 0987654321  (has to be 10 digit)'}))
    facebook = forms.CharField(required=False,widget=forms.TextInput(attrs={'placeholder': 'e.g. Jeffrey Lau (Your facebook name)'}))
    postcode = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'e.g 4000'}))
    street_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'e.g. Mary St'}))
    street_number = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'e.g 73'}))
    suburb = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'e.g. Brisbane'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'e.g. Brisbane City'}))
    state = forms.CharField(max_length=6, widget=forms.Select(choices=STATECHOICES))

    class Meta:
        model = Student
        fields = [
            'gender',
            'dob',
            'phone',
            'other_phone',
            'facebook',
            'street_number',
            'street_name',
            'suburb',
            'city',
            'state',
            'postcode',
        ]

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        
        if str(self.data['phone']).isdigit() != True:
            raise forms.ValidationError("Digits only")

        if len(str(self.data['phone'])) != 10:
            raise forms.ValidationError("Has to be 10 Digits")

        return phone
        
    def clean_other_phone(self):
        other_phone = self.cleaned_data.get('other_phone')
        othphone = str(self.data['other_phone'])
        
        if othphone != '':
            if othphone.isdigit() != True:
                raise forms.ValidationError("Digits only")

            if len(othphone) != 10:
                raise forms.ValidationError("Has to be 10 Digits")

        return other_phone
        
        
    def clean_street_number(self):
        street_number = self.cleaned_data.get('street_number')
        
        if str(self.data['street_number']).isdigit() != True:
            raise forms.ValidationError("Digits only")

        return street_number
        
    def clean_street_name(self):
        street_name = self.cleaned_data.get('street_name')
        sname = self.data['street_name']
        
        if not all(c.isalpha() or c.isspace() for c in sname):
            raise forms.ValidationError("letters only")

        return street_name

    def clean_suburb(self):
        suburb = self.cleaned_data.get('suburb')
        sub = self.data['suburb']
        
        if not all(c.isalpha() or c.isspace() for c in sub):
            raise forms.ValidationError("letters only")

        return suburb

    def clean_city(self):
        city = self.cleaned_data.get('city')
        cit = self.data['city']
        
        if not all(c.isalpha() or c.isspace() for c in cit):
            raise forms.ValidationError("letters only")

        return city           

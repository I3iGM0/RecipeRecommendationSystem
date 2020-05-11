from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import datetime
from .models import Profile

CURRENT_YEAR = datetime.date.today().year
YEARS = list(range(CURRENT_YEAR - 100, CURRENT_YEAR+1))

# Design the forms 
class DateInput(forms.DateInput):
    input_type = 'date'

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    dob = forms.DateField(
        initial=datetime.date.today(),
        widget=DateInput,
        required=True,
        label="Date of birth"
    )
    class Meta:
        model = Profile
        fields = ['dob']

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name','username','email']


class ProfileUpdateForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        initial=datetime.date.today(),
        widget=DateInput,
        required=True,
        label=" Change Date of Birth"
    )
    class Meta:
        model = Profile
        fields = ['image','date_of_birth']

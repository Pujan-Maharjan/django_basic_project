from django import forms


class ProfileForm(forms.Form):
    full_name = forms.CharField(label='Full name', max_length=100)
    age = forms.IntegerField(label = 'age')
    address = forms.CharField(label='Adderss', max_length=100)
    image = forms.ImageField(label = 'Profile Photo')

class UploadFile(forms.Form):
    file = forms.FileField(label = 'Your File')


class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=25)
    password = forms.CharField(label='password', max_length = 25, widget = forms.PasswordInput)
    

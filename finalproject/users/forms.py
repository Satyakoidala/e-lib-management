from django import forms

# django forms

class loginform(forms.Form):
    userid = forms.CharField(max_length=10, label='Your User ID', required=True, widget=forms.TextInput(attrs={
        'placeholder':'Username',
        'autofocus':'True'
    }))
    psw = forms.CharField(max_length=15, label='Your Password', required=True, widget=forms.PasswordInput(attrs={
        'placeholder':'Password'
    }))


class sendotpform(forms.Form):
    userid = forms.CharField(max_length=10, label='Your User ID', required=True, widget=forms.TextInput(attrs={
        'placeholder':'User ID',
        'autofocus':'True'
    }))

class verifyotpform(forms.Form):
    otp = forms.CharField(max_length=6, label='Your OTP', required=True, widget=forms.TextInput(attrs={
        'placeholder':'Enter OTP',
        'autofocus':'True'
    }))

class setpasswordform(forms.Form):
    psw1 = forms.CharField(max_length=15, label='Enter New Password', required=True, widget=forms.PasswordInput(attrs={
        'placeholder':'Enter New Password',
        'autofocus':'True'
    }))
    psw2 = forms.CharField(max_length=15, label='Retype New Password', required=True, widget=forms.PasswordInput(attrs={
        'placeholder':'Retype New Password'
    }))

class searchboxform(forms.Form):
    searchbox = forms.CharField(max_length=100, label='Search Here', widget=forms.TextInput(attrs={
        'placeholder':'Search Book',
    }))
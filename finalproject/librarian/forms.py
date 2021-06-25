from django import forms


class studentsearchform(forms.Form):
    searchprofile = forms.CharField(max_length=10, label='Search Here', widget=forms.TextInput(attrs={
        'placeholder':'Search Profile',
    }))

class bookactionform(forms.Form):
    rollno = forms.CharField(max_length=10, label='Enter Roll No', widget=forms.TextInput(attrs={
        'placeholder':'Enter Roll No',
    }))
    bookid = forms.CharField(max_length=5, label='Enter Book ID', widget=forms.TextInput(attrs={
        'placeholder':'Enter Book ID',
    }))
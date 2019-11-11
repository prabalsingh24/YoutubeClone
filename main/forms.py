from django import forms

class LoginForm(forms.Form):
    name=forms.CharField(max_length=50)
    password=forms.CharField(max_length=50)


class RegisterForm(forms.Form):
    name=forms.CharField(label='YourName',max_length=50)
    password=forms.CharField(max_length=50)
    youremail=forms.CharField(label='Your Email',max_length=50)

class AddVideoForm(forms.Form):
    title=forms.CharField(label='Title',max_length=50)
    description=forms.CharField(label='Description',max_length=500)
    file=forms.FileField()

class CommentForm(forms.Form):
    text=forms.CharField(label='Your Comment',max_length=100)
    video=forms.IntegerField(widget=forms.HiddenInput())


from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


from .models import Profile


class UserForm(UserCreationForm):
    email = forms.EmailField(label='이메일')

    class Meta:
        model = User
        fields = ("username", "email")

# 프로필 편집을 위한 새로운 폼
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'birth_date', 'profile_image']
        widgets = {
            'birth_date' : forms.DateInput(attrs={'type':'date'}),
            'bio' : forms.Textarea(attrs={'rows':4, 'cols':50}),
        }

# User 정보 수정을 위한 폼 (비밀번호 필드 제외)
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
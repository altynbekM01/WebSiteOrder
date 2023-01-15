from django import forms

from webSite.models import User, Profile


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'last_name', 'email', )

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ( 'photo', 'personal_info', 'birthday', )
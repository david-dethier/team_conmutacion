from django.contrib import admin
from django import forms
from api.v1.logins.models import UserLoginModel
from django.contrib.auth.hashers import make_password, check_password


class LoginFrom(forms.ModelForm):
    class Meta:

        model = UserLoginModel
        fields = "__all__"

    # password = forms.CharField(widget=forms.PasswordInput)

class LoginAdmin(admin.ModelAdmin):

    form = LoginFrom
    list_display = ("site_name", "modified_on")


admin.site.register(UserLoginModel, LoginAdmin)

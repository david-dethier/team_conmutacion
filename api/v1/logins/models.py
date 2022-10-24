from django.db import models
from django.core import signing
from django.contrib.auth.models import User
from django.conf import settings

class UserLoginModel(models.Model):
    site_name = models.CharField(max_length=150, default="")
    site_url = models.URLField(default="")
    login_url = models.URLField(default="")
    username = models.CharField(max_length=150, null=False, unique=True)
    password = models.CharField(max_length=255, null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "login_userlogin"
        verbose_name = "User Login"
        verbose_name_plural = "User Logins"

    def __str__(self) -> str:
        return f"{self.site_name}"

    def clean(self):
        try:
            self.password = signing.loads(self.password)
            self.password = signing.dumps(self.password)
        except signing.BadSignature:
            self.password = signing.dumps(self.password)

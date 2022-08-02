from django.forms import ModelForm
from home.models import User

class UserLoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
from django import forms
from .models import Lead,Agent
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import get_user_model


User = get_user_model()



class LeadModelForms(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'first_name',
            'last_name',
            'age',
            'agent',
            'description',
            'phone_number',
            'email',

        )


class LeadForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    age = forms.IntegerField(min_value=0)


class CustomCreation(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}



class ForgotPasswordForm(forms.Form):
    email = forms.CharField()
    


class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        
        password = cleaned_data.get('new_password')
        confirm = cleaned_data.get('confirm_password')

        if confirm!=password:
            raise forms.ValidationError("Password do not match")
        
        return cleaned_data




class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none())

    def __init__(self,*args,**kwargs):
        request = kwargs.pop("request")
        agents = Agent.objects.filter(organization = request.user.userprofile)
        super().__init__(*args, **kwargs)
        self.fields["agent"].queryset = agents



class LeadCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'category',
        )
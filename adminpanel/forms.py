from django import forms
from inventory.models import Device
from django.contrib.auth import get_user_model

User = get_user_model()

class EmployeeCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = [
            "serial_number",
            "device_type",
            "brand",
            "model",
            "configuration",
            "location",
            "status",
        ]

        widgets = {
            "serial_number": forms.TextInput(attrs={"class": "form-control"}),
            "device_type": forms.TextInput(attrs={"class": "form-control"}),
            "brand": forms.TextInput(attrs={"class": "form-control"}),
            "model": forms.TextInput(attrs={"class": "form-control"}),
            "configuration": forms.TextInput(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
        }
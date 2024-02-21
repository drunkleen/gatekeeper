from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from core.models import UserAccount, Subscription


class UserPasswordChangeForm(UserCreationForm):
    class Meta:
        model = UserAccount
        fields = ("password1", "password2")


class UserCreationForm(UserCreationForm):
    class Meta:
        model = UserAccount
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control form-control-lg form-control-solid',
            'placeholder': 'Name',
            'autocomplete': "off",
        })

        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control form-control-lg form-control-solid',
            'placeholder': 'Name',
            'autocomplete': "off",
        })

        self.fields['username'].widget.attrs.update({
            'class': 'form-control form-control-lg form-control-solid',
            'placeholder': 'Username',
            'autocomplete': "off",
        })

        self.fields['email'].widget.attrs.update({
            'class': 'form-control form-control-lg form-control-solid',
            'placeholder': 'E-mail Address',
            'autocomplete': "off",
        })

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control form-control-lg form-control-solid',
            'placeholder': 'Password',
            'autocomplete': "off",
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control form-control-lg form-control-solid',
            'placeholder': 'Repeat Password',
            'autocomplete': "off",
        })


class AdminUserCreationForm(UserCreationForm):
    class Meta:
        model = UserAccount
        fields = ("first_name", "last_name", "username", "email", "account_type")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control form-control-solid mb-3 mb-lg-0',
            'placeholder': 'Name',
            'autocomplete': "off",
        })

        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control form-control-solid mb-3 mb-lg-0',
            'placeholder': 'Name',
            'autocomplete': "off",
        })

        self.fields['username'].widget.attrs.update({
            'class': 'form-control form-control-solid mb-3 mb-lg-0',
            'placeholder': 'Username',
            'autocomplete': "off",
        })

        self.fields['email'].widget.attrs.update({
            'class': 'form-control form-control-solid mb-3 mb-lg-0',
            'placeholder': 'E-mail Address',
            'autocomplete': "off",
        })

        self.fields['account_type'].widget.attrs.update({
            'class': 'form-check form-check-custom form-check-solid',
            'autocomplete': "off",
        })

        # Set password fields as not required
        self.fields['last_name'].required = False
        self.fields['password1'].required = False
        self.fields['password2'].required = False

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password('Gatekeeper2024@')  # Set a fixed password
        if commit:
            user.save()
        return user


class AdminUserEditForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = ("first_name", "last_name", "username", "email", "account_type", "is_active")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control form-control-solid mb-3 mb-lg-0',
            'placeholder': 'Name',
            'autocomplete': "off",
        })

        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control form-control-solid mb-3 mb-lg-0',
            'placeholder': 'Name',
            'autocomplete': "off",
        })

        self.fields['username'].widget.attrs.update({
            'class': 'form-control form-control-solid mb-3 mb-lg-0',
            'placeholder': 'Username',
            'autocomplete': "off",
        })

        self.fields['email'].widget.attrs.update({
            'class': 'form-control form-control-solid mb-3 mb-lg-0',
            'placeholder': 'E-mail Address',
            'autocomplete': "off",
        })

        self.fields['account_type'].widget.attrs.update({
            'class': 'form-check form-check-custom form-check-solid',
            'autocomplete': "off",
        })

        self.fields['is_active'].widget.attrs.update({
            'class': 'form-check-input w-45px h-30px',
            'autocomplete': "off",
        })

        # Set password fields as not required
        self.fields['last_name'].required = False


class UserEditForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = ("first_name", "last_name", "username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control form-control-solid mb-3 mb-lg-0',
            'placeholder': 'Name',
            'autocomplete': "off",
        })

        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control form-control-solid mb-3 mb-lg-0',
            'placeholder': 'Name',
            'autocomplete': "off",
        })

        self.fields['username'].widget.attrs.update({
            'class': 'form-control form-control-solid mb-3 mb-lg-0',
            'placeholder': 'Username',
            'autocomplete': "off",
        })

        self.fields['email'].widget.attrs.update({
            'class': 'form-control form-control-solid mb-3 mb-lg-0',
            'placeholder': 'E-mail Address',
            'autocomplete': "off",
        })

        # Set password fields as not required
        self.fields['last_name'].required = False

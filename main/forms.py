from django import forms

from .models import Score

from django.core.validators import MaxValueValidator

class ScoreForm(forms.ModelForm) :
    class Meta:
        model = Score
        fields = ['I_score','II_score','III_score','IV_score','IV_a_score','I_clear','II_clear','III_clear','IV_clear','IV_a_clear','I_fc','II_fc','III_fc','IV_fc','IV_a_fc','I_ap','II_ap','III_ap','IV_ap','IV_a_ap']
        
    I_score = forms.IntegerField(
        required=False,  
        validators=[MaxValueValidator(1010000)],
        widget=forms.NumberInput(attrs={
            "min": 0,
            "max": 1010000,
        }),
    )

    II_score = forms.IntegerField(
        required=False,  
        validators=[MaxValueValidator(1010000)],
        widget=forms.NumberInput(attrs={
            "min": 0,
            "max": 1010000,
        }),
    )

    III_score = forms.IntegerField(
        required=False,  
        validators=[MaxValueValidator(1010000)],
        widget=forms.NumberInput(attrs={
            "min": 0,
            "max": 1010000,
        }),
    )

    IV_score = forms.IntegerField(
        required=False,  
        validators=[MaxValueValidator(1010000)],
        widget=forms.NumberInput(attrs={
            "min": 0,
            "max": 1010000,
        }),
    )

    IV_a_score = forms.IntegerField(
        required=False,  
        validators=[MaxValueValidator(1010000)],
        widget=forms.NumberInput(attrs={
            "min": 0,
            "max": 1010000,
        }),
    )


from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ['username']
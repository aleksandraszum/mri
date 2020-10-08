from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from course.models import Quiz


class SignUpForm(UserCreationForm):
    username = forms.CharField(label="Podaj nazwę użytkownika:")
    password1 = forms.CharField(widget=forms.PasswordInput(), label="Podaj hasło:")
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Powtórz hasło:")

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class LoginForm(forms.Form):
    username = forms.CharField(label='Podaj nazwę użytkownika', max_length=64)
    password = forms.CharField(label="Podaj hasło", widget=forms.PasswordInput())


class AlgorithmForm(forms.Form):
    COILS_CHOICES = (('1', '1'), ('4', '4'), ('8', '8'), ('16', '16'), ('32', '32'), ('64', '64'),)
    coils = forms.ChoiceField(label='Wybierz liczbę kanałów odbiorczych', choices=COILS_CHOICES)
    CORRELATION_CHOICES = (('0', '0'), ('0.1', '0.1'), ('0.2', '0.2'), ('0.3', '0.3'), ('0.4', '0.4'), ('0.5', '0.5'),
                           ('0.6', '0.6'), ('0.7', '0.7'), ('0.8', '0.8'), ('0.9', '0.9'), ('1', '1'),)
    correlation = forms.ChoiceField(label='Wybierz stopień korelacji między kanałami', choices=CORRELATION_CHOICES)
    sigma = forms.IntegerField(label='Podaj stopień zaszumienia (zniekształcenia) obrazu', min_value=0)
    RECONSTRUCTION_CHOICES = (('0', 'SoS'), ('1', 'SENSE'))
    reconstruction = forms.ChoiceField(label='Wybierz metodę rekonstrukcji', choices=RECONSTRUCTION_CHOICES,
                                       required=False)


class QuizForm(forms.Form):
    # answer_1 = forms.MultipleChoiceField()
    # answer_2 = forms.CharField(max_length=200)
    # answer_3 = forms.CharField(max_length=200)
    # answer_4 = forms.CharField(max_length=200)

    # class Meta:
    #     model = Quiz
    #     fields = ('answer_1', 'answer_2', 'answer_3', 'answer_4')

    def __init__(self, Quiz_object):
        super(QuizForm, self).__init__()
        answer_1 = forms.MultipleChoiceField(
            required=False,
            widget=forms.CheckboxSelectMultiple,
            choices=Quiz_object,
        )

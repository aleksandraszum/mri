from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# from course.models import  Answer, Question
from course.models import Question, Answer


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
    answer_1 = forms.ChoiceField(required=True, widget=forms.RadioSelect(), label=None)
    answer_2 = forms.ChoiceField(required=True, widget=forms.RadioSelect(), label=None)
    answer_3 = forms.ChoiceField(required=True, widget=forms.RadioSelect(), label=None)
    answer_4 = forms.ChoiceField(required=True, widget=forms.RadioSelect(), label=None)
    answer_5 = forms.ChoiceField(required=True, widget=forms.RadioSelect(), label=None)
    answer_6 = forms.ChoiceField(required=True, widget=forms.RadioSelect(), label=None)
    answer_7 = forms.ChoiceField(required=True, widget=forms.RadioSelect(), label=None)
    answer_8 = forms.ChoiceField(required=True, widget=forms.RadioSelect(), label=None)

    def __init__(self, question=None, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        self.fields['answer_1'].choices = [(a.pk, a.answer) for a in
                                           Answer.objects.filter(question_id=question[0])]
        if self.fields['answer_1'].label is None:
            self.fields['answer_1'].label = Question.objects.get(pk=question[0]).question
        self.fields['answer_2'].choices = [(a.pk, a.answer) for a in
                                           Answer.objects.filter(question_id=question[1])]
        if self.fields['answer_2'].label is None:
            self.fields['answer_2'].label = Question.objects.get(pk=question[1]).question
        self.fields['answer_3'].choices = [(a.pk, a.answer) for a in
                                           Answer.objects.filter(question_id=question[2])]
        if self.fields['answer_3'].label is None:
            self.fields['answer_3'].label = Question.objects.get(pk=question[2]).question
        self.fields['answer_4'].choices = [(a.pk, a.answer) for a in
                                           Answer.objects.filter(question_id=question[3])]
        if self.fields['answer_4'].label is None:
            self.fields['answer_4'].label = Question.objects.get(pk=question[3]).question
        self.fields['answer_5'].choices = [(a.pk, a.answer) for a in
                                           Answer.objects.filter(question_id=question[4])]
        if self.fields['answer_5'].label is None:
            self.fields['answer_5'].label = Question.objects.get(pk=question[4]).question
        self.fields['answer_6'].choices = [(a.pk, a.answer) for a in
                                           Answer.objects.filter(question_id=question[5])]
        if self.fields['answer_6'].label is None:
            self.fields['answer_6'].label = Question.objects.get(pk=question[5]).question
        self.fields['answer_7'].choices = [(a.pk, a.answer) for a in
                                           Answer.objects.filter(question_id=question[6])]
        if self.fields['answer_7'].label is None:
            self.fields['answer_7'].label = Question.objects.get(pk=question[6]).question
        self.fields['answer_8'].choices = [(a.pk, a.answer) for a in
                                           Answer.objects.filter(question_id=question[7])]
        if self.fields['answer_8'].label is None:
            self.fields['answer_8'].label = Question.objects.get(pk=question[7]).question

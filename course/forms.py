from django import forms


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

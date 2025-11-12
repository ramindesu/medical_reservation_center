from django import forms


from django import forms


class Form(forms.Form):
    date = forms.DateField(widget=forms.SelectDateWidget())
    service = forms.CharField(
        max_length=100, required=False)
    description = forms.CharField(
        widget=forms.Textarea, required=False)
    history_of_illness = forms.CharField(widget=forms.Textarea, required=False)
    taking_medicine = forms.CharField(widget=forms.Textarea, required=False)
    allergies = forms.CharField(widget=forms.Textarea, required=False)

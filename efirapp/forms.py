from django import forms
from .models import *

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = {'status', 'comments'}
class AdForm(forms.ModelForm):
    class Meta:
        model = Aadhar
        fields = {'aadhaar_id','otp','txn_id', }

class TrackForm(forms.Form):
    aadhaar_id = forms.IntegerField()
    otp = forms.IntegerField()
    txn_id = forms.IntegerField()


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ('fir_id', 'state', 'city', 'complain','recording')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()

        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['city'].queryset = City.objects.filter(state_id=state_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.state.city_set.order_by('name')



from django import forms
from .models import Proof, Claim, Payment, AnnualInspection

CHOICES =(
    ("Monthly Returns", "Monthly Return"),
)

CHOICES2 =(
    ("Good", "Good"),
    ("Bad", "Bad"),
)

CHOICES3 =(
    ("Forfeit", "Forfeit"),
    ("No Forfeit", "No Forfeit"),
)



CHOICES4 =(
    ("Monthly Payments Overdue", "Monthly Payments Overdue"),
    ('Failure To Pay Tax', 'Failure To Pay Tax'),
    ('Underutilised Land', 'Underutilised Land'),
    ('Environmental Impact Degradation', 'Environmental Impact Degradation')

)

CHOICES5 =(
    ("1000 - 3000 [Labour Returns - $100]", "1000 - 3000 [Labour Returns - $100]"),
    ("3 000 - 6 000 [Labour Returns - $300]", "3 000 - 6 000 [Labour Returns - $300]"),
    ("6 000 - 10 000 [Labour Returns - $500]", "6 000 - 10 000 [Labour Returns - $500]"),
)


class ProofForm(forms.ModelForm):

    class Meta:
        model = Proof
        fields = ('image',)


class ClaimForm(forms.ModelForm):
    location = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Harare, Zimbabwe',
        }
    ))

    address = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': '21 Hillcrest Rd',
        }
    ))

    size_approximation = forms.ChoiceField(choices=CHOICES5, widget=forms.Select(
        attrs={
            'class': 'form-control',
        }
    ))



    class Meta:
        model = Claim
        fields = ('location', 'address', 'size_approximation')



class PaymentForm(forms.ModelForm):
    amount = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': '230',
        }
    ))

    claim = forms.ModelChoiceField(queryset=Claim.objects.all(), widget=forms.Select(
        attrs={
            'class': 'form-control',
        }
    ))

    reason = forms.ChoiceField(choices=CHOICES, widget=forms.Select(
        attrs={
            'class': 'form-control',
            'placeholder': 'Monthly Payment',
        }
    ))

    def __init__(self, user, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.fields['claim'].queryset = Claim.objects.filter(applicant=user)

    class Meta:
        model = Payment
        fields = ('amount', 'claim', 'reason')

class MonthlyReturnForm(forms.Form):
    monthly_return = forms.CharField(max_length=120, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }
    ))

    def get_info(self):
        """
        Method that returns formatted information
        :return: subject, msg
        """
        # Cleaned data
        cl_data = super().clean()
        monthly_return = cl_data.get('monthly_return')

        return monthly_return


class PaymentClaimForm(forms.Form):
    claim = forms.ModelChoiceField(queryset=Claim.objects.all(), widget=forms.Select(
        attrs={
            'class': 'form-control',
        }
    ))

    def __init__(self, user, *args, **kwargs):
        super(PaymentClaimForm, self).__init__(*args, **kwargs)
        self.fields['claim'].queryset = Claim.objects.filter(applicant=user)

    def get_info(self):
        # Cleaned data
        cl_data = super().clean()

        claim = cl_data.get('claim')

        return claim


class AnnualInspectionForm(forms.ModelForm):
    claim = forms.ModelChoiceField(queryset=Claim.objects.all(), widget=forms.Select(
        attrs={
            'class': 'form-control',
        }
    ))

    condition = forms.ChoiceField(choices=CHOICES2, widget=forms.Select(
        attrs={
            'class': 'form-control',
        }
    ))

    desicion = forms.ChoiceField(choices=CHOICES3, widget=forms.Select(
        attrs={
            'class': 'form-control',
        }
    ))



    class Meta:
        model = AnnualInspection
        fields = ('claim', 'condition', 'desicion')


class ReasonForm(forms.Form):
    reason = forms.ChoiceField(choices=CHOICES4, widget=forms.Select(
        attrs={
            'class': 'form-control',
        }
    ))

    notes = forms.CharField(max_length=120, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }
    ))

    def get_info(self):
        # Cleaned data
        cl_data = super().clean()

        reason = cl_data.get('reason')
        notes = cl_data.get('notes')

        data = {
            'reason': reason,
            'notes': notes
        }
        return data
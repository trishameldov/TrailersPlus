import re

from django import forms
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe


def validate_card_exp(value):
    try:
        month, year = value.split('/')
    except ValueError:
        raise ValidationError(f"{value} is not valid card expiry date. Please use MM/YY format.")
    try:
        if not 0 < int(month) <= 12:
            raise ValidationError(f"{month} is not a valid month. Month must be between 1 and 12.")
        if len(month) != 2:
            raise ValidationError(f"{value} is not valid card expiry date. Please use MM/YY format.")
    except ValueError:
        raise ValidationError(f"{month} is not a valid month. Please use numbers")
    try:
        year = int(year)
    except ValueError:
        raise ValidationError(f"{year} is not a valid year. Please use numbers")


class CustomRadioSelect(forms.RadioSelect):
    def render(self, name, value, attrs=None, renderer=None):
        html = []
        for choice in self.choices:
            if choice[0] == 'full':
                rendered_string = ("<div class=\"col-sm-12\" id=\"max_amount_radio\">"
                                   "<input type=\"radio\" class=\"radio\" name=\"payment_type\""
                                   f"value=\"{choice[0]}\" checked=\"checked\" onclick=\"maximumAmountClick();\">"
                                   f" <label>{choice[1]}<span class=\"text-muted\" id=\"maxAmount\"></span>"
                                   "</label></div>")
            else:
                rendered_string = ("<div class=\"col-sm-12\" id=\"partial_amount_radio\">"
                                   "<input type=\"radio\" class=\"radio\" name=\"payment_type\""
                                   f"value=\"{choice[0]}\" onclick=\"partialAmountClick();\">"
                                   f" <label>{choice[1]}</label></div>")
            html.append(rendered_string)
        return mark_safe('\n'.join(html))


class InvoiceForm(forms.Form):
    payment_type_choices = [
        ('full', 'Maximum amount'),
        ('partial', 'Partial')
    ]
    policy = forms.BooleanField(
        required=True,
        label=""
    )
    payment_type = forms.ChoiceField(
        choices=payment_type_choices, widget=CustomRadioSelect, required=False
    )
    partial_value = forms.FloatField(
        label="Amount",
        required=False,
        widget=forms.NumberInput(attrs={"class": "form-control",
                                        "aria-describedby": "amountHelp",
                                        "aria-label": "amountHelp"
                                        })
    )
    data_descriptor = forms.CharField(
        label="dataDescriptor",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control d-none",
                "aria-describedby": "dataDescriptor",
                "aria-label": "dataDescriptor",
                "id": "dataDescriptor"
            }
        )
    )
    data_value = forms.CharField(
        label="dataValue",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control d-none",
                "aria-describedby": "dataValue",
                "aria-label": "dataValue",
                "id": "dataValue"
            }
        )
    )
    def clean(self):
        cleaned_data = super(InvoiceForm, self).clean()
        if cleaned_data['payment_type'] == 'partial' \
                and 'partial_value' not in cleaned_data:
            raise ValidationError('Partial value is required for partial payment type')
        return cleaned_data

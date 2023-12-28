from django import forms

from .models import Listing


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'image_url', 'category']
        input_fields_classes = "form-control mb-2 border-0"
        widgets = {
            'title': forms.TextInput(attrs={'class': input_fields_classes}),
            'description': forms.Textarea(attrs={'class': input_fields_classes}),
            'starting_bid': forms.NumberInput(attrs={'class': input_fields_classes, 'min': 0.01, 'step': 0.01}),
            'image_url': forms.URLInput(attrs={'class': input_fields_classes}),
            'category': forms.TextInput(attrs={'class': input_fields_classes})
        }
from django import forms
from .models import Listing, Comment

class CreateForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'price', 'url', 'category']
        widgets = {
            'price': forms.NumberInput(attrs={'step': '0.01'})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 1, 'cols': 60}),
        }
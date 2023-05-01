
"""
    homepage app Forms
"""
from django import forms

class ContactForm(forms.Form):
    source = forms.CharField(max_length=50, label="Name")
    subject = forms.CharField(max_length= 60)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    message = forms.CharField(widget=forms.Textarea(attrs={"rows":3, "cols":37}))
    
    

# class UserInfoForm(forms.Form):
#     name= forms.CharField(max_length=50)
#     email= forms.EmailField() 
#     phone = forms.CharField(max_length=15)
    
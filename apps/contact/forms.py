from django import forms
from .models import ContactMessage
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage; fields = ("full_name", "email", "phone", "subject", "message")
        widgets = {"subject": forms.Select(choices=[("", "Select a subject"), ("Product Order", "Product Order"), ("Wholesale Inquiry", "Wholesale Inquiry"), ("Partnership", "Partnership"), ("Delivery Support", "Delivery Support"), ("General Question", "General Question")]), "message": forms.Textarea(attrs={"rows": 6, "placeholder": "Type your message here..."})}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values(): field.widget.attrs["class"] = "form-control"

from django import forms
from .models import ContactMessage
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage; fields = ("full_name", "email", "phone", "subject", "message")
        widgets = {"subject": forms.TextInput(attrs={"placeholder": "How can we help?"}), "message": forms.Textarea(attrs={"rows": 6, "placeholder": "Tell us more..."})}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-select" if field.widget.__class__ is forms.Select else "form-control"
        self.fields["full_name"].widget.attrs.update({"placeholder": "Jane Smith", "autocomplete": "name"})
        self.fields["email"].widget.attrs.update({"placeholder": "jane@example.com", "autocomplete": "email"})
        self.fields["phone"].widget.attrs.update({"placeholder": "0788 XXX XXX", "autocomplete": "tel", "inputmode": "tel"})

from django import forms
from .models import Order
class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("full_name", "email", "phone", "delivery_location", "payment_method", "order_notes")
        widgets = {"order_notes": forms.Textarea(attrs={"rows": 4, "placeholder": "Optional delivery or order notes"})}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs["class"] = "form-select" if name == "payment_method" else "form-control"

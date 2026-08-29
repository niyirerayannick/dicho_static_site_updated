from django.contrib import messages
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from .models import NewsletterSubscriber
@require_POST
def subscribe(request):
    email = request.POST.get("email", "").strip().lower()
    if not email: messages.error(request, "Please enter a valid email address.")
    else:
        subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email, defaults={"is_active": True})
        if not created and subscriber.is_active: messages.info(request, "That email is already subscribed.")
        else:
            subscriber.is_active = True; subscriber.save(); messages.success(request, "Thanks for subscribing to DICHO updates!")
    return redirect(request.POST.get("next") or "home")

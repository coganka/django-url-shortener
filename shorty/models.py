import string, random
from django.conf import settings
from django.db import models
from django.utils import timezone


def generate_alias(length=6):
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))


class Link(models.Model):
    original_url = models.URLField(max_length=2048)
    alias = models.SlugField(max_length=64, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    clicks_count = models.PositiveIntegerField(default=0)
    max_clicks = models.PositiveIntegerField(null=True, blank=True, default=None)
    active = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.alias} -> {self.original_url}" 
    
    @property
    def is_expired(self):
        return self.expires_at and timezone.now() > self.expires_at
    
    @property
    def short_url(self):
        # for local testing
        return f"http://127.0.0.1:8000/{self.alias}/"
    
    @property
    def qr_url(self):
        return f"http://127.0.0.1:8000/q/{self.alias}.png"
    
    def save(self, *args, **kwargs):
        if not self.alias:
            new_alias = generate_alias()
            while Link.objects.filter(alias=new_alias).exists():
                new_alias = generate_alias()
            self.alias = new_alias
        super().save(*args, **kwargs)
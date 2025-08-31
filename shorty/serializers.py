from rest_framework import serializers
from .models import Link


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ["id", "original_url", "alias", "short_url", "qr_url", "created_at", "expires_at", "clicks_count", "max_clicks", "active", "is_expired"]
        read_only_fields = [
            "id", "created_at", "clicks_count", "is_expired", "short_url", "qr_url"
        ]

    def validate_max_clicks(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError("max_clicks must be greater than 0 or null.")
        return value
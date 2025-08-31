import qrcode
from io import BytesIO
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Link
from .serializers import LinkSerializer
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from .models import Link


class LinkViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all().order_by("-created_at")
    serializer_class = LinkSerializer

    @action(detail=True, methods=["get"])
    def stats(self, request, pk=None):
        link = self.get_object()
        serializer = self.get_serializer(link)  
        return Response(serializer.data)


def perform_destroy(self, instance):
    instance.active = False
    instance.save(update_fields=["active"])


def redirect_view(request, alias):
    link = get_object_or_404(Link, alias=alias)

    if not link.active:
        return JsonResponse({"detail": "Link disabled"}, status=410)
    
    # check expiry
    if link.is_expired:
        return JsonResponse({"detail": "Link expired"}, status=410)
    
    # check click limit
    if link.max_clicks is not None and link.clicks_count >= link.max_clicks:
        return JsonResponse({"detail": "Click limit reached"}, status=410)
    
    link.clicks_count += 1
    link.save(update_fields=["clicks_count"])

    return HttpResponseRedirect(link.original_url)


def preview_view(request, alias):
    link = get_object_or_404(Link, alias=alias)

    data = {
        "alias": link.alias,
        "original_url": link.original_url,
        "clicks_count": link.clicks_count,
        "expires_at": link.expires_at,
        "is_expired": link.is_expired,
        "active": link.active,
        "created_at": link.created_at,
        "max_clicks": link.max_clicks
    }

    return JsonResponse(data)

def qr_view(request, alias):
    link = get_object_or_404(Link, alias=alias, active=True)
    url = request.build_absolute_uri("/{link.alias}/")
    img = qrcode.make(url)

    buf = BytesIO()
    img.save(buf, format="PNG")
    return HttpResponse(buf.getvalue(), content_type="image/png")

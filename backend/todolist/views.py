from django.conf import settings
from django.http import HttpResponse, StreamingHttpResponse
from django.template import engines
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
import requests


@csrf_exempt
def catchall_dev(request, upstream='http://localhost:3000'):
    upstream_url = upstream + request.path
    method = request.META['REQUEST_METHOD'].lower()
    r = getattr(requests, method)(upstream_url, stream=True)
    content_type = r.headers.get('Content-Type')

    if request.META.get('HTTP_UPGRADE', '').lower() == 'websocket':
        return HttpResponse(
            content='WebSocket connections not supported',
            status=501,
            reason='Not implemented',
        )
    elif content_type == 'text/html; charset=UTF-8':
        return HttpResponse(
            content=engines['django'].from_string(r.text).render(),
            status=r.status_code,
            reason=r.reason,
        )
    else:
        return StreamingHttpResponse(
            streaming_content=r.iter_content(4096),
            content_type=content_type,
            status=r.status_code,
            reason=r.reason,
        )


catchall_prod = TemplateView.as_view(template_name='index.html')

catchall = catchall_dev if settings.DEBUG else catchall_prod

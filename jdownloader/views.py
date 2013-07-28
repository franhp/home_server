from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required, user_passes_test
from jdownloader.models import jdownloaderClient
from django.conf import settings


@login_required
@user_passes_test(lambda u: u.has_perm('jdownloader.can_jdownloader'), login_url='/denied')
def list(request):
    t = jdownloaderClient(settings.JDOWNLOADER_HOSTNAME, settings.JDOWNLOADER_PORT)

    download = ''
    if 'add' in request.POST:
        download = t.addLink(request.POST['add'])
    elif 'start' in request.POST:
        download = t.startDL()

    queue = []
    packages = t.getQueue()
    try:
        for package in packages['jdownloader']['package']:
            queue.append((package['@package_linksinprogress'], package['file']['@file_name'], package['file']['@file_percent']))
    except TypeError:
        pass

    return render_to_response('jdownloader.html', RequestContext(request, {'queue': queue, 'download': download}))

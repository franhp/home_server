from __future__ import absolute_import
from celery import task, current_task
from djcelery.models import TaskMeta
from datetime import datetime, timedelta

@task
def download(url=None, name=None, provider=None):
    from smart_downloader.models import File
    f, _ = File.objects.get_or_create(file_url=url, provider=provider)
    current_taskmeta = TaskMeta.objects.get(task_id=current_task.request.id)
    f.task = current_taskmeta
    f.save()

    f.title = name if name else f.find_title()
    f.save()

    return f.download()


@task
def find_more_links(provider_id=None):
    from smart_downloader.models import Provider
    f = Provider.objects.get(pk=provider_id)
    return 'Added %s files' % f.find_more_links()


@task
def update_transmission():
    from smart_downloader.plugins.transmission import TransmissionProvider
    tc = TransmissionProvider()
    return tc.update_fields()


@task
def cleanup_transmission_tasks():
    TaskMeta.objects.filter(file_task__isnull=True).delete()


@task
def cleanup_old_downloads():
    from smart_downloader.models import File
    last_week = datetime.now() - timedelta(days=7)
    File.objects.filter(created_on__lt=last_week).delete()

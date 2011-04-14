from django.core.management.base import BaseCommand

from addons.models import Addon
from amo.utils import chunked
from amo.tasks import dedupe_approvals


class Command(BaseCommand):
    help = 'Dedupes activity for addon approvals log'

    def handle(self, *args, **options):
        pks = Addon.objects.values_list('pk', flat=True).order_by('id')
        for chunk in chunked(pks, 100):
            dedupe_approvals.delay(chunk)

import os
import json
from pjtest import settings
from django.core.management.base import BaseCommand
from users.serializers import UserSerializer, StatisticSerializer


class Command(BaseCommand):
    help = 'Fill User and Statistic models.'

    def handle(self, *args, **options):

        with open(os.path.join(settings.BASE_DIR, 'users.json')) as user_list:
            for obj in json.load(user_list):
                inst = UserSerializer(data=obj)
                if inst.is_valid():
                    inst.is_valid()
                    inst.save()
                else:
                    raise ValueError()

        with open(os.path.join(settings.BASE_DIR, 'users_statistic.json')) as statistic_list:
            for obj in json.load(statistic_list):
                inst = StatisticSerializer(data=obj)
                if inst.is_valid():
                    inst.is_valid()
                    inst.save()
                else:
                    raise ValueError()

        self.stdout.write(self.style.SUCCESS('DB filled'))

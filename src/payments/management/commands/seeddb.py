from django.core.management.base import BaseCommand

from django_seed import Seed

from payments.models import Invoice, Requisite


class Command(BaseCommand):
    help = "Команда добавления в базу данных 5000" + \
        "платежных заявок(Invoice) и 100 реквизитов(Requisite)"

    requires_migrations_checks = True

    def handle(self, *args, **options):
        seeder = Seed.seeder()
        seeder.add_entity(Requisite, 100)
        seeder.add_entity(Invoice, 5000)
        seeder.execute()

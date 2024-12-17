
from django.core.management.base import BaseCommand, CommandError



class Command(BaseCommand):
    help = "This is an example"

    def add_arguments(self, parser):
        parser.add_argument("test", nargs="+", type=int)

    def handle(self, *args, **options):
        print("This is my_command.py !")
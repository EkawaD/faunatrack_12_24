
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail


class Command(BaseCommand):
    help = "This is an example"

    def add_arguments(self, parser):
        parser.add_argument("test", nargs="+", type=int)

    def handle(self, *args, **options):
        print("This is my_command.py !")
        send_mail(
            "Un projet a été marqué comme critique",
            "Un projet a été marqué comme critique.",
            "from@example.com",
            ["to@example.com"],
            fail_silently=False,
        ) 
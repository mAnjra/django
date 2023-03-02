from django.core.management.base import BaseCommand
from datetime import datetime
from todo.models import Todo

class Command(BaseCommand):
    help = 'swicthes all feilds to true everyday'

    def handle(self, *args, **options):
        """
        queryset = Todo.objects.filter(my_boolean_field=False)
        for obj in queryset:
            obj.my_boolean_field = True
            obj.save()
        """
        Todo.objects.all().update(my_boolean_field=True)
        new_todo = Todo.objects.create(title='New todo', datetime_field=datetime.now())


        

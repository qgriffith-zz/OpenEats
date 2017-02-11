from django.core.management.base import NoArgsCommand, CommandError
from openeats.recipe.models import Recipe
from django.template import Context, loader

class Command(NoArgsCommand):
    help = 'Outputs OpenEat recipes in the meal master format'

    def handle(self, *args, **options):
        #get a list of all the recipes
        try:
            recipes = Recipe.objects.all()
        except IndexError:
            raise CommandError("Could not get a list of recipes check your database")
        
        template = loader.get_template('recipe/mealmaster_export.txt')
        context = Context({'queryset':recipes})
        print template.render(context)
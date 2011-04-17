from django.core.management.base import NoArgsCommand, CommandError
from openeats.recipe.models import Recipe
from templatetags.meal_master_convert import convert_unit

class Command(NoArgsCommand):
    help = 'Outputs OpenEat recipes in the meal master format'

    def handle(self, *args, **options):

        #get a list of all the recipes
        try:
            recipes = Recipe.objects.all()
        except IndexError:
            raise CommandError("Could not get a list of recipes check your database")
        for recipe in recipes:
            print recipe.title
            
from imagekit import ImageSpec, register
from imagekit.processors import SmartResize

"""image kit module spec"""


class RecipeDetail(ImageSpec):
    processors = [SmartResize(230, 230)]
    format = 'PNG'


class RecipeList(ImageSpec):
    processors = [SmartResize(120, 160)]
    format = 'PNG'

register.generator('recipe:detail', RecipeDetail)
register.generator('recipe:list', RecipeList)
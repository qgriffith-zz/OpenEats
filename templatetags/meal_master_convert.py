from django import template
register = template.Library()

@register.filter(name='convertUnit')
def convert_unit(value):
    """converts ingredient measurment to meal master unit"""

    convert = {'gram':'g',
              'fluid ounce':'fl',
              'pint':'pint',
              'quart':'qt',
              'gallon':'ga',
              'ounce':'oz',
              'pound':'lb',
              'pound':'lb',
              'drop':'lb',
              'dash':'ds',
              'pinch':'pn',
              'teaspoon':'ts',
              'tablespoon': 'tb',
              'cup':'c',
              'small': 'sm',
              'medium': 'md',
              'large': 'lg',
              'can':'cn',
              'package':'pk',
              'carton':'ct',
              'bunch':'bn',
              'each':'ea',
              'whole': 'ea',
    }

    #check to see if the value is already an allowed unit type for meal master
    if value in convert.values():
        return value

    if value.endswith('s'):  #remove the s if anything is plural
       value = value[:-1]
    if value in convert:
        return convert[value]
    else:
        return ''

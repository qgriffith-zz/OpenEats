from django.conf import settings

def oelogo(context):
    '''return the oelogo for templates allowing users to set their own logo in the settings file'''
    return {'OELOGO': settings.MEDIA_URL + settings.OELOGO}

def oetitle(context):
    return {'OETITLE': settings.OETITLE}

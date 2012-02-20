from imagekit.specs import ImageSpec
from imagekit import processors

'''image kit module spec'''

class ResizeThumb(processors.Resize):
    ''' Thumbnail resize proccessor'''
    height = 260
    width = 180
    crop = False

class ResizeIndexThumb(processors.Resize):
    ''' Thumbnail resize proccessor'''
    height = 230
    width = 230
    crop = True

class ResizeAdminThumb(processors.Resize):
    '''Admin Thumbnail resize proccessor'''
    height = 75
    width = 75
    crop = True

class ResizeListThumb(processors.Resize):
    '''Recipe list view thumbnail resize proccessor'''
    height = 100
    width = 100
    crop = True

class ResizeDisplay(processors.Resize):
    '''Recipe show view thumbnail proccessor'''
    height = 400

class Thumbnail(ImageSpec):
    '''Thumbnail spec'''
    access_as = 'thumbnail_image'
    pre_cache = True
    processors = [ResizeThumb]

class Display(ImageSpec):
    '''Display thumbnail spec'''
    processors = [ResizeDisplay]

class AdminThumbnail(ImageSpec):
    '''Admin thumbnail spec'''
    access_as ='admin_thumbnail'
    pre_cache = True
    processors = [ResizeAdminThumb]

class IndexThumbnail(ImageSpec):
    '''List Thumbnail spec'''
    access_as = 'index_thumbnail'
    pre_cache = True
    processors = [ResizeIndexThumb]

class ListThumbnail(ImageSpec):
    '''List Thumbnail spec'''
    access_as = 'list_thumbnail'
    pre_cache = True
    processors = [ResizeListThumb]
from imagekit.specs import ImageSpec
from imagekit import processors

'''image kit module spec'''

# thumbnail resize processor
class ResizeThumb(processors.Resize):
    height = 250
    width = 200
    crop = False

class ResizeAdminThumb(processors.Resize):
    height = 75
    width = 75
    crop = True

# display resize proccessor
class ResizeDisplay(processors.Resize):
    height = 400

# now we can define our thumbnail spec
class Thumbnail(ImageSpec):
    access_as = 'thumbnail_image'
    pre_cache = True
    processors = [ResizeThumb]

class Display(ImageSpec):
    processors = [ResizeDisplay]

class AdminThumbnail(ImageSpec):
    access_as ='admin_thumbnail'
    pre_cache = True
    processors = [ResizeAdminThumb]

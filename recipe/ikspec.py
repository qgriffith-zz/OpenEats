from imagekit.specs import ImageSpec
from imagekit import processors

'''image kit module spec'''

# thumbnail resize processor
class ResizeThumb(processors.Resize):
    height = 250
    width = 200
    crop = False

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

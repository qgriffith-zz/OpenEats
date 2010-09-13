__test__ = {"addCourse": """
Create a Course and test the slug over ride works in the save method
then try to set slug to none to make sure the save method does not try to auto set slug again
Add a test user
>>> from django.contrib.auth.models import User
>>> user = User.objects.create(username="testCourse", password="password")
>>> from models import Course
>>> course = Course.objects.create(title="Lunch", author=user)
>>> course.slug
u'lunch'
>>> course.slug = None
>>> course.save()
Traceback (most recent call last):
    ...
IntegrityError: ...
""",
"addCuisine":"""
Create a Cuisine  the slug over ride works in the save method
then try to set slug to none to make sure the save method does not try to auto set slug again
Add A test user
>>> from django.contrib.auth.models import User
>>> user = User.objects.create(username="testCuisine", password="password")
>>> from models import Cuisine
>>> cuisine = Cuisine.objects.create(title="Spanish", author=user)
>>> cuisine.slug
u'spanish'
>>> cuisine.slug = None
>>> cuisine.save()
Traceback (most recent call last):
    ...
IntegrityError: ...

"""
}
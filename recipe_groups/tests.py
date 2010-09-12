__test__ = {"addCourse": """
Create a Course
Add a test user
>>> from django.contrib.auth.models import User
>>> user = User.objects.create(username="testCourse", password="password")
>>> from models import Course
>>> course = Course.objects.create(title="Lunch", slug='lunch', author=user)
>>> course.title
'Lunch'
""",
"addCuisine":"""
Create a Cuisine
Add A test user
>>> from django.contrib.auth.models import User
>>> user = User.objects.create(username="testCuisine", password="password")
>>> from models import Cuisine
>>> cuisine = Cuisine.objects.create(title="Spanish", slug="spanish", author=user)
>>> cuisine.title
'Spanish'

"""
}
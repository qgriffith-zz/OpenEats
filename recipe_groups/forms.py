from django.forms import ModelForm
from models import Course

class CoursePopForm(ModelForm):
    class Meta:
        model = Course
        exclude = ('slug')
from django.test import TestCase
from django.db import IntegrityError
from models import Course, Cuisine
from django.contrib.auth.models import User

class CourseTest(TestCase):
    '''Test that course save overide works and course routing works'''
    fixtures = ['data_user.json','course_data.json'] #load a user up and course data

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.assertEquals(self.user.username, 'testUser') #make sure the user works
        
    def testSlugAutoset(self):
        '''Verify the slug is auto set when a slug is not provided'''
        course = Course.objects.create(title='New Course', author=self.user)
        self.assertEqual(course.slug, 'new-course')

    def testSlugSet(self):
        '''Pass a slug when creating the object and make sure the slug is set to that and not over ride'''
        course = Course.objects.create(title="Slug Test", slug="my-slug", author=self.user)
        self.assertEqual(course.slug, 'my-slug')

    def testSlugReset(self):
        '''Test that the slug is only auto set during intial creation and not after the object has beens saved'''
        course = Course.objects.create(title='failed course', author=self.user)
        course.slug = None
        self.assertRaises(IntegrityError, course.save)

    def testCoursePage(self):
        '''Test the course web page'''
        from django.core.urlresolvers import reverse
        response = self.client.get(reverse('course_list'))
        self.assertEqual(response.status_code, 200) #got the the page
        self.assertTemplateUsed(response, 'recipe_groups/course_list.html') #check the right template was used
        courses = response.context['course_list']
        self.assertEqual(len(courses), 5, 'There should be 5 courses on the page but we found %s' % len(courses))

    def tearDown(self):
        Course.objects.all().delete()
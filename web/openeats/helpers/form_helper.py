from django.utils.html import escape
from django.shortcuts import render
from django.http import HttpResponse
import django.forms as forms
from django.template import RequestContext


def handlePopAdd(request, addForm, field):
    """'This form helper is a pop up on the recipe form that allows users to add courses and cuisnes to the database, it returns
        the created object as the selected object on the recipe form"""

    if request.method == "POST":
        form = addForm(request.POST)
        if form.is_valid():
            try:
                newObject = form.save()
            except forms.ValidationError, error:
                newObject = None
            if newObject:
                return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % \
                (escape(newObject._get_pk_val()), escape(newObject)))
    else:
        form = addForm()

    pageContext = {'form': form, 'field': field}
    return render(request, "recipe_groups/popadd.html", pageContext)
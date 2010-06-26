from django.utils.html import escape
from django.shortcuts import render_to_response
from django.http import HttpResponse
import django.forms as forms

def handlePopAdd(request, addForm, field):
    ''''Used to submit the object to the database from the popup form'''
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
    return render_to_response("form/popadd.html", pageContext)
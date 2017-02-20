from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.forms.models import inlineformset_factory
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.views.generic import DetailView
from django.utils.translation import ugettext as _
from djangoratings.views import AddRatingView
from django.conf import settings
from django.db.models import F

from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import *
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

from openeats.ingredient.models import Ingredient
from openeats.recipe.models import Recipe, StoredRecipe, NoteRecipe, ReportedRecipe
from openeats.recipe.forms import RecipeForm,IngItemFormSet, RecipeSendMail

def index(request):
    recipe_list = Recipe.objects.filter(shared=Recipe.SHARE_SHARED).exclude(photo='').order_by('-pub_date')[0:6]
    return render(request, 'recipe/index.html', {'new_recipes': recipe_list})


def recipeShow(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)

    # setting the four previously viewed recipes in the user session so they can be easily accessed on the sidebar
    if 'recipe_history' in request.session:
        sessionlist = request.session['recipe_history']
        if [recipe.title, recipe.get_absolute_url()] not in sessionlist:
            sessionlist.append(([recipe.title, recipe.get_absolute_url()]))
            if len(sessionlist) > 4:
                sessionlist.pop(0)
            request.session['recipe_history'] = sessionlist
    else:
        request.session['recipe_history'] = [[recipe.title, recipe.get_absolute_url()]]

    if request.user.is_authenticated():
        note = request.user.noterecipe_set.filter(recipe=recipe, author=request.user)
    else:
        note = None
    
    if recipe.shared == Recipe.PRIVATE_SHARED and recipe.author != request.user:  # check if the recipe is a private recipe if so through a 404 error
        output = _("Recipe %s is marked Private") % recipe.slug
        raise Http404(output)
    else:
        return render(request, 'recipe/recipe_detail.html', {'recipe': recipe, 'note': note})


def recipePrint(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)

    if request.user.is_authenticated():
        note = request.user.noterecipe_set.filter(recipe=recipe, author=request.user)
    else:
        note = None

    if recipe.shared == Recipe.PRIVATE_SHARED and recipe.author != request.user:  # check if the recipe is a private recipe if so through a 404 error
        output = _("Recipe %s is marked Private") % recipe.slug
        raise Http404(output)
    else:
        return render(request, 'recipe/recipe_print.html', {'recipe': recipe, 'note': note})


@login_required
def recipe(request, user=None, slug=None):
    """used to create or edit a recipe"""
    IngFormSet = inlineformset_factory(Recipe, Ingredient, fields='__all__', extra=2, formset=IngItemFormSet)  # create the ingredient form with 15 empty fields

    if user and slug:  # must be editing a recipe
        recipe_inst = get_object_or_404(Recipe, author__username=request.user.username, slug=slug)
    else:
        recipe_inst = Recipe()

    if request.method == 'POST':
        form = RecipeForm(data=request.POST, files=request.FILES, instance=recipe_inst)
        formset = IngFormSet(request.POST, instance=recipe_inst)
        if form.is_valid() and formset.is_valid():
            new_recipe = form.save()
            instances = formset.save(commit=False)  # save the ingredients seperatly
            for instance in instances:
                instance.recipe_id = new_recipe.id   # set the recipe id foregin key to the this recipe id
                instance.save()
            form.save(commit=False)
            return redirect(new_recipe.get_absolute_url())
    else:
        form = RecipeForm(instance=recipe_inst)
        if not recipe_inst.related:  # if the related field has not been set on a recipe or it is a new recipe populate the drop down otherwise use the value that is already set
            form.fields['related'].queryset = Recipe.objects.filter(author__username=request.user.username).exclude(related=F('id')).filter(related__isnull=True).order_by('-pub_date')

        if recipe_inst.id:   # if we are editing an existing recipe disable the title field so it can't be changed
            form.fields['title'].widget.attrs['readonly'] = True

        formset = IngFormSet(instance=recipe_inst)
    return render(request, 'recipe/recipe_form.html', {'form': form, 'formset': formset, })


def recipeUser(request, shared, user):
    """Returns a list of recipes for a giving user if shared is set to share then it will show the shared recipes if it is set to private
       then only the private recipes will be shown this is mostly used for the users profile to display the users recipes
    """
    if shared == 'share':
        recipe_list = Recipe.objects.filter(author__username=user, shared=Recipe.SHARE_SHARED).order_by('-pub_date')
    else:
        recipe_list = Recipe.objects.filter(author__username=user, shared=Recipe.PRIVATE_SHARED).order_by('-pub_date')
       
    return render(request, 'recipe/recipe_userlist.html', {'recipe_list': recipe_list, 'user': user, 'shared': shared})


@login_required
def recipeRate(request, object_id, score):
    """ Used for users to rate recipes """
    recipe_type = ContentType.objects.get(app_label="recipe", model="recipe")
    params = {
        'content_type_id': recipe_type.id,  # this is the content type id of the recipe models per django.contrib.contentetype
        'object_id': object_id,
        'field_name': 'rating',  # this should match the field name defined in your model
        'score': score,
    }
    results = {}
    response = AddRatingView()(request, **params)
    results['message'] = response.content
    r = Recipe.objects.get(pk=object_id)  # get recipe object so we can return the average rating
    avg = r.rating.score / r.rating.votes
    results['avg'] = avg
    results['votes'] = r.rating.votes

    return JsonResponse(results, safe=False)

@login_required
def recipeStore(request, object_id):
    """Take the recipe id and the user id passed via the url check that the recipe is not
       already stored for that user then store it if it is
    """
    stored = StoredRecipe.objects.filter(recipe=object_id, user=request.user.id)
    if stored:
        output = _("Recipe already in your favorites!")
        return HttpResponse(output)
    else:  # save the recipe
        r = get_object_or_404(Recipe, pk=object_id)
        new_store = StoredRecipe(recipe=r, user=request.user)
        new_store.save()
        output = _("Recipe added to your favorites!")
        return HttpResponse(output)
        

@login_required
def recipeUnStore(request):
    """Take the recipe id via the url check that the recipe is not already
       stored for that user then remove it if it is
    """
    if request.method == 'POST':
        if request.POST['recipe_id']:
            try:
                stored_recipe = StoredRecipe.objects.get(recipe=request.POST['recipe_id'], user=request.user.id)
            except StoredRecipe.DoesNotExist:
                raise Http404
            stored_recipe.delete()
            return redirect('/recipe/ajax-favrecipe/')
    

@login_required
def recipeUserFavs(request):
    """returns a list of a users favorite recipes"""
    stored_list = StoredRecipe.objects.filter(user=request.user.id)
    recipe_list = []
    for stored in stored_list:
        recipe_list.append(stored.recipe)
    return render(request, 'recipe/recipe_userfav.html', {'recipe_list': recipe_list})


@login_required
def recipeNote(request):
    """This is called by the jquery inline edit on the recipe detail template to allow users to add notes to recipes"""

    user = request.user
    
    if request.POST['recipe']:
        try:
            recipe = Recipe.objects.get(pk=request.POST['recipe'])
        except Recipe.DoesNotExist:
            raise Http404
        note = request.POST['note']

    cur_note = NoteRecipe.objects.filter(author=user, recipe=recipe)

    if cur_note:  # check to see if the user already has a note if so re-save it with the new text
        if len(note) == 0 or note.isspace():  # they must want to delete the note so they sent nothing in the text field
            cur_note[0].delete()
        else:
            cur_note[0].text = note
            cur_note[0].save()
    else:
        if len(note) > 0 and not note.isspace():
            new_note = NoteRecipe(recipe=recipe, author=user, text=note)
            new_note.save()
    return HttpResponse(note)


def exportPDF(request, slug):
    """Exports recipes to a pdf"""

    pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
    pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
    pdfmetrics.registerFont(TTFont('VeraIt', 'VeraIt.ttf'))
    pdfmetrics.registerFont(TTFont('VeraBI', 'VeraBI.ttf'))
    registerFontFamily('Vera', normal='Vera', bold='VeraBd', italic='VeraIt', boldItalic='VeraBI')

    recipe = get_object_or_404(Recipe, slug=slug)

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + recipe.slug + '.pdf'

    # Our container for 'Flowable' objects
    elements = []

    # set up our styles
    styles = getSampleStyleSheet()
    styleH1 = styles['Heading1']
    styleH1.textColor = colors.green
    styleH1.fontName = 'VeraBd'
    styleH2 = styles['Heading2']
    styleH2.textColor = colors.goldenrod
    styleH2.fontName = 'Vera'
    styleNormal = styles['Normal']
    styleNormal.fontName='Vera'
    styleBullet = styles['Bullet']
    styleBullet.fontName = 'VeraIt'

    # create the pdf doc
    doc = SimpleDocTemplate(response)

    # set the openeats logo
    logo = settings.STATIC_ROOT + "/" + settings.OELOGO
    I = Image(logo)
    I.hAlign = 'LEFT'
    elements.append(I)
    elements.append(Spacer(0, 1 * cm))

    # add the recipe photo if the recipe has one
    if recipe.photo:
        photo = settings.BASE_PATH + recipe.photo.url
        I = Image(photo)
        I.height = "CENTER"
        elements.append(I)
        elements.append(Spacer(0, 0.5 * cm))

    # add the meat of the pdf
    elements.append(Paragraph(recipe.title, styleH1))
    elements.append(Paragraph('info', styleH2))
    elements.append(Paragraph(recipe.info, styleNormal))
    elements.append(Paragraph('ingredients', styleH2))

    for ing in recipe.ingredients.all():
        ing = "%s %s %s %s" % (ing.quantity, ing.measurement, ing.title, ing.preparation)
        elements.append(Paragraph(ing, styleBullet))

    elements.append(Paragraph('directions', styleH2))
    elements.append(Paragraph(recipe.directions, styleNormal))

    # build the pdf and return it
    doc.build(elements)
    return response


@login_required
def recipeReport(request, slug):
    """Take the recipe id and the user id passed via the url check that the recipe is not
       already reported if it isn't it will be reported
    """
    recipe = get_object_or_404(Recipe, slug=slug)
    reported = ReportedRecipe.objects.filter(recipe=recipe.pk)
    if reported:
        output = _("Recipe has already been reported!")
        return HttpResponse(output)
    else:  # report the recipe
        new_reported = ReportedRecipe(recipe=recipe, reported_by=request.user)
        new_reported.save()
        output = _("Recipe reported to the moderators!")
        return HttpResponse(output)


@login_required
def recipeMail(request, id):
    """this view creates a form used to send a recipe to someone via email"""
    if request.method == 'POST':
        form = RecipeSendMail(data=request.POST, request=request)  # passing the request object so that in the form I can get the request post dict to save the form
        if form.is_valid():
            form.save(fail_silently=False)
            return HttpResponse("recipe sent to " + request.POST['to_email'])
    else:
        form = RecipeSendMail(request=request)
    return render(request, 'recipe/recipe_email.html', {'form': form, 'id': id})


class CookList(DetailView):
    model = Recipe
    template_name = "recipe/recipe_cook.html"

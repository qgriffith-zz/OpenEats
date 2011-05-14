/* javascript file for OpenEats2*/

/* this function is for the django-dynamic-formset which allows a new ingredient row to be added on the recipe form*/
$(function() {
    $('tbody tr').formset({
        prefix: '{{ formset.prefix }}',
        added: function(row){
            var txt = row.find('#ing-field input');
            txt.unbind();
            makeAutoComplete(); /* call the makeAutoComplete function to assign the jquery ui autocomplete to the new row added*/
        },
        extraClasses: ['row1', 'row2']

    });
})


function makeAutoComplete() {
    $(function() {
        $("#ing-field input").autocomplete({
            source: '/ingredient/auto/',
            minLength: 2
        });
    })
    };
makeAutoComplete()





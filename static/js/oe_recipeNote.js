/**
 * * User: qgriffith
 * Date: 3/18/12
 * Time: 1:57 PM
 * Allows a user to edit a note on a recipe
 */

$(document).ready(function() {
    $('#recipe-note p').editable('/recipe/ajaxnote/', {
        indicator : 'Saving...',
        tooltip   : 'Click to edit...',
        type      : 'textarea',
        cancel    : 'Cancel',
        submit    : 'OK',
        submitdata : {recipe: "{{ recipe.id }}"},
        name       :  'note',
        cssclass : 'editable',
        event    : 'dblclick'
    })
});
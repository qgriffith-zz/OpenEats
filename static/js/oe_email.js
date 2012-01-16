//recipe mail function
$(document).ready(dialogForms);

function dialogForms() {
    $('#email-link').click(function () {
        var a = $(this);
        $.get(a.attr('href'), function (resp) {
            var dialog = $('<div>').attr('id', 'formDialog').html(resp);
            $('body').append(dialog);
            dialog.find(':submit').hide();
            dialog.dialog({
                title:a.attr('title') ? a.attr('title') : '',
                modal:true,
                hide:'explode',
                buttons:{
                    'send':function () {
                        submitFormWithAjax($(this).find('form'));
                    },
                    'cancel':function () {
                        $(this).dialog('close');
                    }
                },
                close:function () {
                    $(this).remove();
                },
                width:'auto'
            });
        }, 'html');
        return false;
    });
}

function submitFormWithAjax(form) {
    form = $(form);
    $.ajax({
        url:form.attr('action'),
        data:form.serialize(),
        type:(form.attr('method')),
        dataType:'html',
        success:function (html) {
            $('#formDialog').html(html);
            var validationCheck = $('#formDialog').has("form") //check to see if the form was valid and saved if the html contains a form then we know something went wrong
            if (validationCheck.length == 0) //form must of passed so change the buttons and close after 10 seconds
            {
                // $('#formDialog').delay(50000).dialog('close');
                setTimeout(function () {
                    $('#formDialog').dialog('close');
                }, 1800);

            }
        }
    });
    //return false;
}

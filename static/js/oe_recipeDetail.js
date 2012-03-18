/**
  * User: qgriffith
 * Date: 3/18/12
 * Time: 2:00 PM
 * Adds the fancy box for the picture and cook view and the report and favorite button change
 */

$(document).ready(function() {
    $("a#recipe-photo").fancybox({
        'openEffect': 'elastic',
        'closeEffect': 'fade'
    });
    $("a#cook-view").fancybox({
        'autoSize':true,
        'fitToView':true,
        'closeBtn': true,
        'closeClick': true,
        'height': 1000,
        'width': 1000,
        'scrolling':'auto'
    });

});



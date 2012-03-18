/**
  * User: qgriffith
 * Date: 3/18/12
 * Time: 2:00 PM
 * Adds the fancy box for the picture and cook view and the report and favorite button change
 */

$(document).ready(function() {
    $("a#recipe-photo").fancybox();
    $("a#cook-view").fancybox({
        'autoDimensions': false,
        'autoScale': false,
        'width': 1000,
        'height': 1000
    });

});



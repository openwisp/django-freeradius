/*jslint browser:true */
django.jQuery(function ($) {
    'use strict';
    var textarea_selector = "textarea";
    function adaptiveheight(a) {
        django.jQuery(a).height(0);

        var scrollval = django.jQuery(a)[0].scrollHeight;
        django.jQuery(a).height(scrollval);
        if (parseInt(a.style.height, 10) > django.jQuery(window).height()) {
            var i = a.selectionEnd;
            if (i >= 0) {
                django.jQuery(document).scrollTop(parseInt(a.style.height, 10));
            } else {
                django.jQuery(document).scrollTop(0);
            }
        }
    }
    django.jQuery(textarea_selector).click(function (e) {
        adaptiveheight(this);
    });
    django.jQuery(textarea_selector).keyup(function (e) {
        adaptiveheight(this);
    });
    // init
    django.jQuery(textarea_selector).each(function () {
        adaptiveheight(this);
    });
});

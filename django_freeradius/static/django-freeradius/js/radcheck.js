django.jQuery(function ($) {
    'use strict';
    // stop here if in add mode
    if (!('.deletelink').length) { return; }
    if (!gettext) { gettext = function (text) { return text; }; }
    var newValueRow = $('.field-new_value'),
        rawValueRow = $('.field-value'),
        newValueInput = newValueRow.find('input'),
        changeId = 'change-radcheck-value',
        changeHtml = '<button class="button" id="' + changeId + '">' + gettext('change') + '</button>',
        cancelId = 'cancel-change-radcheck-value',
        cancelHtml = '<button class="button" id="' + cancelId + '">' + gettext('cancel') + '</button>';
    newValueRow.hide();
    rawValueRow.find('.readonly').append(changeHtml);
    newValueInput.after(cancelHtml);
    // change value operation
    $('#' + changeId).click(function (e) {
        e.preventDefault();
        rawValueRow.hide();
        newValueRow.show();
    });
    // cancel change value operation
    $('#' + cancelId).click(function (e) {
        e.preventDefault();
        newValueInput.val('');
        newValueRow.hide();
        rawValueRow.show();
    });
});

$(function () {
    var
        $win = $(window),
        $filter = $('.scroll-navbar'),
        $filterSpacer = $('<div />', {
            "class": "filter-drop-spacer",
            "height": 0
        });
    $win.scroll(function () {
        $filter.before($filterSpacer);
        $filter.addClass("fix");

    });
});





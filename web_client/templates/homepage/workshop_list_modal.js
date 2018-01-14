var selected_list_item;

$('.list-group-item').click(function () {
    $(selected_list_item).removeClass('active');
    selected_list_item = this;
    $(this).addClass('active');
});
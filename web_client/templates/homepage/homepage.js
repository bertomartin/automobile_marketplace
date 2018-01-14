var selected_list_item;

$('.list-group-item').click(function () {
    console.log(this.id);
    $(selected_list_item).removeClass('active');
    selected_list_item = this;
    $(this).addClass('active');
});

$('.share').on('shown.bs.modal', function () {
    console.log('Generating url...');
    $('#post-url').focus();
});
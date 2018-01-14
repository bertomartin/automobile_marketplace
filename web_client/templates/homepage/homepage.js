var selected_list_item;
var selected_post_id;

$('.workshops').on('shown.bs.modal', function() {
    selected_post_id = $(this).find('#post-id').val();
    console.log(selected_post_id);
});

$('.workshops').on('hidden.bs.modal', function () {
    if (selected_list_item){
        $(selected_list_item).removeClass('active');
    }
    selected_post_id = null;
    selected_list_item = null;
});

//Selects/deselects item in 'workshop list' modal.
$('.list-group-item').click(function () {
    // console.log(this.id);
    $(selected_list_item).removeClass('active');
    selected_list_item = this;
    $(this).addClass('active');
});

//Submits post to selected workshop
$('.submit-workshop-button').click(function () {
    if (selected_list_item == null){
        console.log('nothing selected!')
    } else {
        console.log('Submitting post with id: '+ selected_post_id + ', to workshop with id: ' + selected_list_item.id);
    }
});

//Adds focus to url field in 'share' modal
$('.share').on('shown.bs.modal', function () {
    console.log('Generating url...');
    $('#post-url').focus();
});


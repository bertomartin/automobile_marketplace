function load_content(target_element, url, data) {
    $.ajax({
        url: url,
        data: data,
        type: 'get',
        success: function (data) {
            $(target_element).html(data);
        }
    });
}

function append_content(target_element, url, data) {
    $.ajax({
        url: url,
        data: data,
        type: 'get',
        success: function (data) {
            $(target_element).append(data);
        }
    });
}

function submit_form(target_element, url, form) {
    $.ajax({
        url: url,
        data: form,
        type: 'post',
        success: function (data) {
            $(target_element).html(data);
        }
    });
}
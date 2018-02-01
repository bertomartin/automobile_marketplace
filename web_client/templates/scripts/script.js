function load_content(target_element, url, data) {
    $.ajax({
        url: url,
        data: data,
        success: function (data) {
            $(target_element).html(data);
        }
    });
}

function append_content(target_element, url, data) {
    $.ajax({
        url: url,
        data: data,
        success: function (data) {
            $(target_element).append(data);
        }
    });
}
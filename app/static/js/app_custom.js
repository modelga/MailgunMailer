// NAVIGATION //
$(document).ready(function () {
    $(".nav>li").each(function () {
        var navItem = $(this);
        if (navItem.find("a").attr("href") == location.pathname) {
            navItem.addClass("active");
        }
    });
});
// NAVIGATION //


// ADMIN SITES //

// PW_Generator Start
$(document).ready(function () {
    if ($("#pw_gen").length) {
        var url_data = $('#pw_gen').attr('action');
        console.log("URL_DATA : " + url_data);
        $('#gen_pw_button').click(function () {
            var password = $('#password').val();
            $.ajax({
                url: url_data,
                data: $('form').serialize(),
                type: 'POST',
                success: function (response) {
                    console.log("PW Generate response : " + response);
                    $('.gen_pw_responsed_data').empty().append('<div class="alert alert-info">' + response + '</div>');
                },
                error: function (error) {
                    console.log(error);
                }
            });
        });
    }
});
// PW_Generator End

// ADMIN SITES //
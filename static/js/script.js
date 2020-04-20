$(function () {

    $('#upload-file-btn').click(function () {

        var form_data = new FormData($('#upload-file')[0]);

        $('#loading-image').show();
        $('#result').html('');

        $.ajax({

            type: 'POST',
            url: '/classify',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function (classes) {

                $('#loading-image').hide();

                if (classes && classes.length) {

                    $('#result').html(
                        '<table><tr><th>Class</th><th>Score</th></tr>'
                        + classes.sort(function (a, b) {
                            return b.score - a.score
                        }).map(function (c) {
                            return '<tr><td>' + c.class + '</td><td>' + c.score + '</td></tr>'
                        }).join('') + '</table>'
                    );

                } else {

                    $('#result').html('No match!')
                }
            },
            error: function () {

                $('#loading-image').hide();
                $('#result').html('No match!')
            }
        });
    });

    $('#loading-image').bind('ajaxStart', function () {
        $(this).show();
    }).bind('ajaxStop', function () {
        $(this).hide();
    });

    $("#imgInp").change(function () {
        readURL(this);
    });
});

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#blah').attr('src', e.target.result);
            $('#blah').show();
            $('#result').html('')
        };
        reader.readAsDataURL(input.files[0]); // convert to base64 string
    }
}

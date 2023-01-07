$(document).on('submit', '#create-link-form', function(e){
    e.preventDefault();

    $.ajax({
        type: 'POST',
        url: '',
        data: {
            long_link: $('#link').val(),
            time_to_delete: $('#delete').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },

        success: function(data){
            $('#success').html(data);
        }
    })
})

console.log('hello')
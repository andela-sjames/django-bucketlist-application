$(document).ready(function(){
    $('#set').click(function(){
        $(this).fadeOut('fast');
    });

    $('#get').click(function(){
        $('#set').show('fast');
    });

});
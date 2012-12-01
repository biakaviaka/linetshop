$(document).ready(function() {
    $("form").submit(function(event) 
    {
        if( $('.requested').val().length == 0 ) 
        {
            event.preventDefault();
        }
    });
});

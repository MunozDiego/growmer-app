(function($) {
    
    var $DOC = $(document);
    $DOC.on('click', 'input[type="submit"]', function() {
        console.log("Se presionó el Boton")
            
            //your client side validation here
            $("#username").change(function() {
                $("#username").data("changed",true);
            });
            $("#password").change(function() {
                $("#password").data("changed",true);
            });
            if($("#username").data("changed") & $("#password").data("changed"))
                {
                $(this).attr('hidden','hidden');
                $('#divMsg').show();
                } 
        
            
    });
    

    
})(jQuery);


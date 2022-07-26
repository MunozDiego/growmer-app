(function($) {

    "use strict";
    
    var $WIN = $(window);
    var $DOC = $(document);


   /* Preloader
    * ----------------------------------------------------- */
     /*   
    $("html").addClass('cl-preload');

    $WIN.on('load', function() {

        //force page scroll position to top at page refresh
        // $('html, body').animate({ scrollTop: 0 }, 'normal');

        // will first fade out the loading animation 
        $("#loader").fadeOut("slow", function() {
            // will fade out the whole DIV that covers the website.
            $("#preloader").delay(300).fadeOut("slow");
        }); 
        
        // for hero content animations 
        $("html").removeClass('cl-preload');
        $("html").addClass('cl-loaded');
    
    });        */

    // botton preload /login and /login_ig        
    $("input[id='username']").change(function() {
        $("input[id='username']").data("changed",true);
    });
    $("input[id='password']").change(function() {
        $("input[id='password']").data("changed",true);
    });

    $DOC.on('click', 'input[id="login"]', function() {
        console.log("Se presionó el Boton")
            
        if($("input[id='username']").data("changed") & $("input[id='password']").data("changed"))
            {
            $(this).attr('hidden','hidden');
            $('#divMsg').show();
            //$("input[id='username']").data("changed",false);
            //$("input[id='password']").data("changed",false);
            }       
    });

    //button preload /seguir and /seguir-advanced
    $("input[id='seed']").change(function() {
        $("input[id='seed']").data("changed",true);
    });
    $("input[id='n_follows']").change(function() {
        $("input[id='n_follows']").data("changed",true);
    });

    $DOC.on('click', 'input[id="seguir"]', function() {
        console.log("Se presionó el Boton")
            
        if($("input[id='seed']").data("changed") & $("input[id='n_follows']").data("changed"))
            {
            $(this).attr('hidden','hidden');
            $('#advance').attr('hidden','hidden');
            $('#divMsg').show();
            }       
    });

    //button preload para /unfollow

    //$("input[id='date']").change(function() {
        //$("input[id='date']").data("changed",true);
    //});

    $DOC.on('click', 'input[id="dejar-seguir"]', function() {
        console.log("Se presionó el Boton")
            
        //if($("input[id='date']").data("changed"))
            //{
            $(this).attr('hidden','hidden');
            $('#dsList').attr('hidden','hidden');
            $('#UfAll').attr('hidden','hidden');
            $('#divMsg').show();
            //}       
    });


    // button preload /unfollow-list
    $("input[id='user_list']").data("changed",false)

    $("textarea[id='user_list']").change(function() {
        $("textarea[id='user_list']").data("changed",true);
    });

    $DOC.on('click', 'input[id="dejar-seguir-list"]', function() {
        console.log("Se presionó el Boton")
            
        if($("textarea[id='user_list']").data("changed"))
            {
            $(this).attr('hidden','hidden');
            $('#divMsg').show();
            }       
    });

    //button preload /not-follow-back

    $DOC.on('click', 'input[id="not-follow-back"]', function() {
        console.log("Se presionó el Boton")

        $(this).attr('hidden','hidden');
        $('#divMsg').show();
      
    });
    //button preload /change-account

    $DOC.on('click', 'a[id="change_salir"]', function() {
        console.log("Se presionó el Boton")

        $(this).attr('hidden','hidden');
        $('#change_cancel').attr('hidden','hidden');
        $('#divMsgModal').show();
      
    });
})(jQuery);


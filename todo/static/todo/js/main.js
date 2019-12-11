function item_text_controller(){
    $(".todo_title").click(function(){
        if($(this).parent().parent().children("main").css("display")=="none"){
            $(this).parent().parent().children("main").css({display: "block", opacity: "1"})
        }
        else{
            $(this).parent().parent().children("main").css({display: "none", opacity: "0"})
        }
    })
}


function todo_add_form_controller(){
    $(".todo_add").click(function(){
        if($(".todo_add_form").css("visibility")=="hidden"){
            $(".todo_add_form").css({visibility: "visible", opacity: "1", display: "block"})
            $(".todo_add").children().removeClass("fa-plus").addClass("fa-minus")
        }
        else{
            $(".todo_add_form").css({visibility: "hidden", opacity: "0", display: "none"})
            $(".todo_add").children().removeClass("fa-minus").addClass("fa-plus")
        }
    })
}


window.onload = function(){
    item_text_controller()
    todo_add_form_controller()
}
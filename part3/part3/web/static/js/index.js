function shimada_rotate(shimada) {
    var angle = 0;

    var tid = setInterval(function() { 

        if (parseFloat($(shimada).css("width").replace("px", "")) < ($(document).width() * 0.35))
        {
            angle += 0.1 + (angle / 10);
            $(shimada).css("width", (1 + (angle / 10)).toString() + "%");
        } else {
            angle += 30;
        }
        $(shimada).rotate(angle);
        
        if (parseFloat($(shimada).css("width").replace("px", "")) >= ($(document).width() * 0.2))
        {
            var src = "/static/img/hos_logo.png";
            $(shimada).attr("src", src);
            $("#high_class_restaurant").show();
        }
    }, 20);
}
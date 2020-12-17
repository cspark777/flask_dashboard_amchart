/**
Custom module for you to write your own javascript functions
**/
var Custom = function () {

    // private functions & variables


    var myFunc = function(text) {
        
    }

    // public functions
    return {

        //main function
        init: function () {
            //initialize here something. 
            function setCookie(name,value,days) {
                var expires = "";
                if (days) {
                    var date = new Date();
                    date.setTime(date.getTime() + (days*24*60*60*1000));
                    expires = "; expires=" + date.toUTCString();
                }
                document.cookie = name + "=" + (value || "")  + expires + "; path=/";
            }
            function getCookie(name) {
                var nameEQ = name + "=";
                var ca = document.cookie.split(';');
                for(var i=0;i < ca.length;i++) {
                    var c = ca[i];
                    while (c.charAt(0)==' ') c = c.substring(1,c.length);
                    if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
                }
                return null;
            }

            var themecolor = getCookie("themecolor");
            if(themecolor == null) themecolor = "dark";

            if(themecolor == "dark")
                $('.color-darkblue').trigger("click");
            else
                $('.color-light').trigger("click");

            $('.color-darkblue').on("click", function(e){
                setCookie("themecolor", "dark", 10000);
            });
            $('.color-light').on("click", function(e){
                setCookie("themecolor", "light", 10000);
            });           
        },

        //some helper function
        doSomeStuff: function () {
            myFunc();
        }

    };

}();

/***
Usage
***/
//Custom.init();
//Custom.doSomeStuff();
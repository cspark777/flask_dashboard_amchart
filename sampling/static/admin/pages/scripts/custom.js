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
            function setTheme(themeName, color) {
                localStorage.setItem('theme', themeName);
                var color_ = (Metronic.isRTL() ? color + '-rtl' : color);
                $('#style_color').attr("href", Layout.getLayoutCssPath() + 'themes/' + color_ + ".css");    
                if(typeof Detail !== "undefined"){
                    Detail.change_theme(color);    
                }
                
            }

            // function to toggle between light and dark theme
            function toggleTheme() {
                if (localStorage.getItem('theme') === 'theme-dark') {
                    setTheme('theme-light', "light");
                } else {
                    setTheme('theme-dark', "darkblue");
                }
            }

            $("#slider_theme").on("click", function(e){
                toggleTheme();
            });

            // Immediately invoked function to set the theme on initial load
            (function () {
                if (localStorage.getItem('theme') === 'theme-dark') {
                    setTheme('theme-dark', "darkblue");
                    document.getElementById('slider_theme').checked = false;
                } else {
                    setTheme('theme-light', "light");
                    document.getElementById('slider_theme').checked = true;
                }
            })();
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
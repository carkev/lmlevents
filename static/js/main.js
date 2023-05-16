// Show the password
function showPword() {
    let x = document.getElementsByClassName("password");
    for (let i = 0; i < x.length; i++){
        if (x[i].type === "password") {
          x[i].type = "text";
        } else {
          x[i].type = "password";
        }
    }
}

// Send HTTP request
function SendToggleAJAX(action){

    $.ajax({
        method: "POST",
        url: "/account",
        data: {
            "toggle": action
        },
    });
}

function Toggle() {
    let toggle = $('#2-step-toggle')
    let term = $('#2-step-term')
    if (toggle.prop("checked") == true){
        term.text("Activer la double authentification")
        SendToggleAJAX("off")
    } 
    else{
        term.text("Désactiver la double authentification")
        SendToggleAJAX("on")
    }

}

let temp_button_text;

function CustomFormSubmitPost(e){
    let el = $(e);
    temp_button_text = el.text()
    el.attr('disabled', 'disabled').text("").append('<class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>Loading...');
};

function CustomFormSubmitResponse(e){
    let el = $(e);
    el.removeAttr('disabled').text(temp_button_text);
};

$("#saved-cards tr").click(function(){
    $(this).addClass('selected').siblings().removeClass('selected');    
    let value=$(this).find('td:first').html();
    $('#use-card').removeAttr("disabled")    
});

$('.ok').on('click', function(e){
    alert($("saved-cards tr.selected td:first").html());
});


function EmailVerification(){
    CustomFormSubmitPost($('#request-email'));
    const URL = "/email/";
    $.ajax({
        method: "POST",
        success: function(json){
            CustomFormSubmitResponse($('#request-email'));
            alert(json["message"]);
        },
        error: function(xhr){
            CustomFormSubmitResponse($('#request-email'));
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
}

"use strict";
var FormControls = function () {

    var usersignup = function () {

        var form = $('#signupform')
        form.submit(function(event){
            event.preventDefault();
            CustomFormSubmitPost($('#signupform button[type=submit]'));
            
            let formdata = form.serialize() 
            $.ajax({
                url: form.attr("action"),
                method: form.attr("method"),
                data: formdata,
                success: function(json){
                    CustomFormSubmitResponse($('#signupform button[type=submit]'));
                    alert(json["message"]);
                    window.location.assign("/verification/" + json["url_safe"] +"/" + json["token"])
                },
                error: function(xhr){
                    CustomFormSubmitResponse($('#signupform button[type=submit]'));
                    console.log(xhr.status + ": " + xhr.responseText);
                }
            }) 

        })    
    };

    var usersignin = function (){
        var form = $('#signinform')
        form.submit(function(event){
            event.preventDefault();
            CustomFormSubmitPost($('#signinform button[type=submit]'));
            
            let formdata = form.serialize() 
            $.ajax({
                url: form.attr("action"),
                method: form.attr("method"),
                data: formdata,
                success: function(json){
                    CustomFormSubmitResponse($('#signinform button[type=submit]'));
                    alert(json["message"])
                    if (json["message"] == "Nous vous avons envoyé un SMS"){
                        window.location.assign("/verification/" + json["url_safe"] +"/" + json["token"])
                    }
                    else{
                        window.location.assign('/account')
                    }
                },
                error: function(xhr){
                    CustomFormSubmitResponse($('#signinform button[type=submit]'));
                    console.log(xhr.status + ": " + xhr.responseText);
                }
            }) 
        });
    };

    var requestpassword = function (){

        var form = $('#requestpasswordform')
        form.submit(function(event){
            event.preventDefault();
            CustomFormSubmitPost($('#requestpasswordform button[type=submit]'));
            
            let formdata = form.serialize() 
            
            $.ajax({
                url: form.attr("action"),
                method: form.attr("method"),
                data: formdata,
                success: function(json){

                    CustomFormSubmitResponse($('#requestpasswordform button[type=submit]'));
                    alert(json["message"]);                
                },
                error: function(xhr){
                    CustomFormSubmitResponse($('#requestpasswordform button[type=submit]'));
                    console.log(xhr.status + ": " + xhr.responseText);
                }
            })
        });
    };

    var updatepassword = function (){
        var form = $('#updatepasswordform')
        form.submit(function(event){
            event.preventDefault();
            CustomFormSubmitPost($('#updatepasswordform button[type=submit]'));
            
            let formdata = form.serialize() 
            $.ajax({
                url: form.attr("action"),
                method: form.attr("method"),
                data: formdata,
                success: function(json){
                    CustomFormSubmitResponse($('#updatepasswordform button[type=submit]'));
                    alert(json["message"]);
                    if (json["result"] == "perfect"){
                        window.location.assign('/account')
                    }
                },
                error: function(xhr){
                    CustomFormSubmitResponse($('#updatepasswordform button[type=submit]'));
                    console.log(xhr.status + ": " + xhr.responseText);
                }
            })  
        });
    };

    var twostep = function (){
        var form = $('#twostepform')
        form.submit(function(event){
            event.preventDefault();
            CustomFormSubmitPost($('#twostepform button[type=submit]'));
            
            let formdata = form.serialize() 
            $.ajax({
                url: form.attr("action"),
                method: form.attr("method"),
                data: formdata,
                success: function(json){
                    CustomFormSubmitResponse($('#twostepform button[type=submit]'));
                    alert(json["message"]);
                    if (json["result"] == "perfect"){
                        window.location.assign('/shop?name=\'product_list\'')
                    }
                },
                error: function(xhr){
                    CustomFormSubmitResponse($('#twostepform button[type=submit]'));
                    console.log(xhr.status + ": " + xhr.responseText);
                }
            })  
        });
    };
                        

    return {
        init: function() { 
            usersignup();
            usersignin();
            requestpassword();
            updatepassword(); 
            twostep(); 
        }
    };
}();

jQuery(document).ready(function() {     
    FormControls.init();
});

$(function() {
    // This function gets cookie with a given name
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie != '') {
            let cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                let cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    let csrftoken = getCookie('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        let host = document.location.host; // host + port
        let protocol = document.location.protocol;
        let sr_origin = '//' + host;
        let origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
})

$(document).ready(function() {
   
    var swiper = new Swiper(".sliderFeaturedPosts", {
      spaceBetween: 0,
      speed: 500,
      centeredSlides: true,
      loop: true,
      slideToClickedSlide: true,
      autoplay: {
        delay: 3000,
        disableOnInteraction: false,
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
      navigation: {
        nextEl: ".custom-swiper-button-next",
        prevEl: ".custom-swiper-button-prev",
      },
    });
  
  
    const glightbox = GLightbox({
      selector: '.glightbox'
    });

    AOS.init({
      duration: 2000,
      easing: 'ease-in-out',
      once: true,
      mirror: false
    });
  
      tinymce.init({
        selector: 'textarea#editor',
        plugins: ' anchor autolink charmap codesample emoticons image link lists media searchreplace table visualblocks wordcount',
      toolbar: 'undo redo | blocks fontfamily fontsize | bold italic underline strikethrough | link image media table mergetags | align lineheight | tinycomments | checklist numlist bullist indent outdent | emoticons charmap | removeformat',
      tinycomments_mode: 'embedded',
      tinycomments_author: 'Author name',
      mergetags_list: [
        { value: 'First.Name', title: 'First Name' },
        { value: 'Email', title: 'Email' },
      ],
      ai_request: (request, respondWith) => respondWith.string(() => Promise.reject("See docs to implement AI Assistant")),
      setup: (editor) => {
          // Apply the focus effect
          editor.on("init", () => {
          editor.getContainer().style.transition = "border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out";
            });
          editor.on("focus", () => { (editor.getContainer().style.boxShadow = "0 0 0 .2rem rgba(0, 123, 255, .25)"),
          (editor.getContainer().style.borderColor = "#80bdff");
            });
          editor.on("blur", () => {
          (editor.getContainer().style.boxShadow = ""),
          (editor.getContainer().style.borderColor = "");
           });
         },
      });
   
     
      
       
})

function Login(){
  email = $("#email").val();
  password = $("#password").val()

 if(email == "" || password == ""){
  $("#alerterr").addClass("show")
  $("#loginerr").text("field cannot be empty")
 }else{
  $.ajax({
    type: "post",
    url: "/login/",
    data: {
      email: email,
      password: password,
      csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
      },
      cache: false,
    dataType: "json",
    success: function (response) {
      $("#alertres").addClass("show")
      $("#loginres").text(response);

      location.href = "/"

    },
    error: function (jqXHR, textStatus, errorThrown){
      $("#alerterr").addClass("show")
      $("#loginerr").text(jqXHR.responseJSON)


    }
  });
 }
}

function Signup(){
  let _this = $(this)
let email = $("#email").val();  
let fname = $("#first_name").val();  
let lname = $("#last_name").val();  
let password = $("#password").val()
let username = $("#username").val()
let question = $("#question").val()
let answer = $("#answer").val()


  if(email == "" || password == "" || username == "" || first_name == "" || last_name == ""){
    $("#alerterr").addClass("show")
    $("#loginerr").text("field cannot be empty")
   }else if(question == "" || answer == ""){
    $("#alerterr").addClass("show")
    $("#loginerr").text("pick a question and answer")
   }
    else{
    $.ajax({
      type: "post",
      url: "/register/",
      data: {
        email: email,
        password: password, 
        username: username, 
        first_name: fname, 
        last_name: lname, 
        question: question,
        answer: answer,
        csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
        },
        cache: false,
      dataType: "json",
      success: function (response) {
        $("#alertres").addClass("show")
        $("#loginres").text(response);
  
        location.href = "/"
  
      },
      error: function (jqXHR, textStatus, errorThrown){
        $("#alerterr").addClass("show")
        $("#loginerr").text(jqXHR.responseJSON)
  
  
      }
    });
   }
 
}

function ChangePassword(){

  let email = $("#email").val()
 
 if(email == ""){
  $("#alerterr").addClass("show")
  $("#loginerr").text("field cannot be empty")
 }else{
  $.ajax({
    type: "post",
    url: "/forgetpassword/",
    data: {
      email: email,
    
      csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
      },
      cache: false,
    dataType: "json",
    success: function (response) {
       
        $("#checkmail").hide(2000)
        $("#question").text(response)
        document.getElementById("checkq").classList.remove("d-none")
    

    },
    error: function (jqXHR, textStatus, errorThrown){
      $("#alerterr").addClass("show")
      $("#loginerr").text(jqXHR.responseJSON)


    }
  });
 }
}
function CheckQuestion(){

  let answer = $("#answer").val()
  let email = $("#email").val()

 
  $.ajax({
    type: "post",
    url: "/forgetpassword/",
    data: {
      answer: answer,
      useremail: email,
      csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
      },
      cache: false,
    dataType: "json",
    success: function (response) {
       
        $("#checkq").hide(2000)
        document.getElementById("chpwd").classList.remove("d-none")
    

    },
    error: function (jqXHR, textStatus, errorThrown){
      $("#alerterr").addClass("show")
      $("#loginerr").text(jqXHR.responseJSON)


    }
  });
 
}
function newPassword(){

  let password = $("#newp").val()
  let email = $("#email").val()

 
  $.ajax({
    type: "post",
    url: "/forgetpassword/",
    data: {
      newpassword: password,
      emailType: email,
      csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
      },
      cache: false,
    dataType: "json",
    success: function (response) {
       
      $("#alertres").addClass("show")
      $("#loginres").text("Password Change Successfully");

      location.href = "/login/"
    

    },
    error: function (jqXHR, textStatus, errorThrown){
      $("#alerterr").addClass("show")
      $("#loginerr").text(jqXHR.responseJSON)


    }
  });
 
}

function handleNameUpdate(){
  fname = $("#first_name").val()
  lname = $("#last_name").val()
  username = $("#username").val()
  oldusername = $("#oldusername").val()
  id = $("#user").val()

  if(fname == "" || lname == "" || username == ""){
    $("#alerterr").addClass("show")
  $("#loginerr").text("field cannot be empty")
  }else{

    $.ajax({
      type: "post",
      url: "/update-profile/"+id,
      data: {
        username: username, 
        first_name: fname, 
        last_name: lname, 
        oldusername: oldusername, 
        csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
        },
        cache: false,
      dataType: "json",
      success: function (response) {
        $("#alertres").addClass("show")
        $("#loginres").text(response);
  
        location.href = "/"
  
      },
      error: function (jqXHR, textStatus, errorThrown){
        $("#alerterr").addClass("show")
        $("#loginerr").text(jqXHR.responseJSON)
  
  
      }
    });

  }
}

function handledelete(){
  let id = $("#logid").val();
  let ask = confirm("Are you sure you want to delete your account?")

  if(ask){
    $.ajax({
      type: "get",
      url: "/delete/",
      data: {id: id},
      dataType: "json",
      success: function (response) {
        $("#alertres").addClass("show")
        $("#loginres").text("account deleted successfully");

  
        location.href = "/login"
      },
      error: function (jqXHR, textStatus, errorThrown){
        $("#alerterr").addClass("show")
      $("#loginerr").text(jqXHR.responseJSON)
      }
    });
  }

}


function handleRemove(){
  $("#alerterr").removeClass("show")
}

function handleRemovePos(){
  $("#alertres").removeClass("show")
}

function handleRemoveReply(comment, reply){


 $.ajax({
  type: "GET",
  url: "/del-reply",
  data: {id: reply, comment: comment},
  dataType: "json",
  success: function (response) {
    location.reload()
  },
  error: function (jqXHR, textStatus, errorThrown) {
  //  $("#err").text(errorThrown)
  }
 });
}
function handleRemoveComment(comment){


 $.ajax({
  type: "GET",
  url: "/del-comment",
  data: {comment: comment},
  dataType: "json",
  success: function (response) {
    location.reload()
  },
  error: function (jqXHR, textStatus, errorThrown) {
  //  $("#err").text(errorThrown)
  }
 });
}

$("#searchtext").keyup(() =>{
  setTimeout(() =>{
    let text = $("#searchtext").val();
    if(text !== ""){
      $.ajax({
        type: "get",
        url: "/search",
        data: {text:text},
        dataType: "json",
        success: function (response) {
          $("#header").removeClass("d-flex")
          $("#header").addClass("none")
        //  response.map((item, i) =>{
        //   let title = `${item.length > 10 ? item.title.slice(0, 10)+"..." : item.title } `;
        //   let id = item.id;
        //   let newele = document.createElement("a")
        //   newele.href = "/single-post"+id
        //   newele.innerText = title
        //   $(".searchres").append(newele);
        //  })
        },
        error: function (jqXHR, textStatus, errorThrown){
          console.log(jqXHR.responseJSON);
        }
      });
    }
  }, 1000)
})

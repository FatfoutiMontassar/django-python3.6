/*
  change the destinatio user , his messages and the
  products related to him using ajax(without reloading the page)
*/
$(function (){
  var scrolled = 0
  $(".list-group-item").click(function(){
    if($(this).hasClass("product")){
      console.log("do nothing ..")
    }else{
      if($(this).hasClass("active")){
        console.log("do nothing ..")
      }else{
        //alert("function call ..")
        var numberOfMessages = "0" ;
        var csrf = $("#list-of-messages").attr("csrf");
        var to   = $(this).attr("username");
        document.getElementById("upload_picture_to").setAttribute("value",to) ;
        $.ajax({
          url: '/messenger/load_more/',
          data: {
            'numberOfMessages':numberOfMessages,
            'required':"10",
            'to':to,
            'csrfmiddlewaretoken': csrf,
          },
          cache: false,
          type: 'post',
          success: function (data) {
            $(".list-group").children('a').each(function(){
              if($(this).hasClass('product')){
                console.log("ignore this one ..")
              }else{
                $(this).removeClass().addClass('list-group-item')
                if($(this).attr("username") == to){
                  $(this).addClass('active')
                }
              }
            });
            $("#list-of-messages").html(data);
            document.getElementById("list-of-messages").setAttribute("numberOfMessages",10);
            history.pushState(null, null, '/messenger/'+to+"/");
            scrolled=scrolled+10000;
            $("#list-of-messages").animate({
              scrollTop:  scrolled
            });


            $.ajax({
              url: '/messenger/get_products/',
              data: {
                'to':to,
                'csrfmiddlewaretoken': csrf,
              },
              cache: false,
              type: 'post',
              success: function (data) {
                $("#list-of-selected-products").html(data)
                //alert(data)
              }
            });
            return false ;
          }
        });
        return false ;
      }
    }
  });
});

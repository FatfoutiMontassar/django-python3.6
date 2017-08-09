/*
  add 5 more messages when user scrolls to top.
*/
$(function(){
  $('#list-of-messages').scroll(function(){
    if ($('#list-of-messages').scrollTop() == 0){
      var numberOfMessages = $("#list-of-messages").attr("numberOfMessages");
      var csrf = $("#list-of-messages").attr("csrf");
      var to   = $("#picture-upload-form input[name=to]").val();
      //alert(numberOfMessages)
      $.ajax({
        url: '/messenger/load_more/',
        data: {
          'numberOfMessages':numberOfMessages,
          'required':"5",
          'to':to,
          'csrfmiddlewaretoken': csrf,
        },
        cache: false,
        type: 'post',
        success: function (data) {
          $("#list-of-messages").prepend(data);
          //alert("success ... " + data)
          var numberOfMessages = $("#list-of-messages").attr("numberOfMessages");
          document.getElementById("list-of-messages").setAttribute("numberOfMessages",(parseInt(numberOfMessages) + 5));

          //var numberOfMessages = $("#list-of-messages").attr("numberOfMessages");
          //document.getElementById("list-of-messages").setAttribute("numberOfMessages",(parseInt(numberOfMessages) + 1));
        }
      });
      return false;
    }
  });
});

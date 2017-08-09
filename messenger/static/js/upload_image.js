/*
  upload images deirectly by submitting the from through a hidden sumbit
  button , clicked when the value of the image is changed.
*/
$(function () {
  var scrolled = 0
  $("#btn-upload-picture").click(function () {
    $("#picture-input").click();
  });

  $("#picture-input").change(function() {
    $("#picture-upload-form").submit() ;
  });

  $("#picture-upload-form").submit(function () {
    var csrf = $("#picture-upload-form").attr("csrf");
    var to   = $("#picture-upload-form input[name=to]").val();
    var file = $("#picture-upload-form input[name=picture]").val();
    //alert("it works")
    $.ajax({
      url: '/messenger/send_image/',

      data: new FormData( this ),
      processData: false,
      contentType: false,
      cache: false,
      type: 'post',
      success: function (data) {
        //alert('success');

        $("#list-of-messages").append(data);
        $("input[name='message']").val('');
        $("input[name='message']").focus();
        var numberOfMessages = $("#list-of-messages").attr("numberOfMessages");
        document.getElementById("list-of-messages").setAttribute("numberOfMessages",(parseInt(numberOfMessages) + 1));
        scrolled=scrolled+10000;
        $("#list-of-messages").animate({
          scrollTop:  scrolled
        });

      }
    });
    return false;
  });
});

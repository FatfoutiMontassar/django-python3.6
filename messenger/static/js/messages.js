$(function () {
  $("#send").submit(function () {
    //window.alert("message should've been sent !")

    $.ajax({
      url: '/messenger/send/',
      data: $("#send").serialize(),
      cache: false,
      type: 'post',
      success: function (data) {
        $(".send-message").before(data);
        $("input[name='message']").val('');
        $("input[name='message']").focus();
      }
    });
    return false;

  });
});

/*
  check the unread messages and update their value in the inbox span.
*/
$(function () {
  function check_messages() {
    $.ajax({
      url: '/messenger/check/',
      cache: false,
      success: function (data) {
        $("#unread-count").text(data);
        //alert(data + " -- " + data.length )
      },
      complete: function () {
        window.setTimeout(check_messages, 10000);
      }
    });
  };
  check_messages();

});

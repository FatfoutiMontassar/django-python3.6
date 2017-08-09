/*
  cheks whether there is unread notifications or not.
  if there is unread notifications, it will load the newest 5 notifications.
  a 'see all' link is shown which will direct to a page containig all the
  current user's notifications.
*/
$(function () {
  $('#notifications').popover({html: true, content: 'Loading...', trigger: 'manual'});

  $("#notifications").click(function () {
    if ($(".popover").is(":visible")) {
      $("#notifications").popover('hide');
    }
    else {
      $("#notifications").popover('show');
      $.ajax({
        url: '/notifications/last/',
        beforeSend: function () {
          $(".popover-content").html("<div style='text-align:center'><img src='/static/img/loading.gif'></div>");
          $("#notifications").removeClass("new-notifications");
        },
        success: function (data) {
          $(".popover-content").html(data);
        }
      });
    }
    return false;
  });


  function check_notifications() {
    $.ajax({
      url: '/notifications/check/',
      cache: false,
      success: function (data) {
        if (data != "0") {
          $("#notifications").addClass("new-notifications");
        }
        else {
          $("#notifications").removeClass("new-notifications");
        }
      },
      complete: function () {
        window.setTimeout(check_notifications, 10000);
      }
    });
  };
  check_notifications();
});

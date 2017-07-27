$(function () {
  var scrolled = 0

  function scrollall(){
    scrolled=scrolled+10000;
    $("#list-of-messages").animate({
      scrollTop:  scrolled
    });
  }
  window.onload = function() {
    //alert("please...")
    scrollall();
  };

  $("#send").submit(function () {
    //window.alert("message should've been sent !")
    var selectedProducts = ""
    $("#list-of-selected-products").children('a').each(function(){
      if($(this).hasClass("active")){
        if(selectedProducts.length > 0 )selectedProducts += "&"
        selectedProducts += $(this).attr("product-id")
      }
    });
    $("#send").append('<input type="hidden" name="relatedProducts" id="relatedProducts" value="' + selectedProducts + '">')
    //alert(selectedProducts)
    $.ajax({
      url: '/messenger/send/',
      data: $("#send").serialize(),
      cache: false,
      type: 'post',
      success: function (data) {
        $("#list-of-messages").append(data);
        $("input[name='message']").val('');
        $("input[name='message']").focus();

        scrolled=scrolled+10000;
        $("#list-of-messages").animate({
          scrollTop:  scrolled
        });
      }
    });
    $("#relatedProducts").remove()
    $("#list-of-selected-products").children('a').each(function(){
      if($(this).hasClass("active")){
        $(this).removeClass().addClass('list-group-item').addClass('product')
      }
    });


    return false;
  });
});

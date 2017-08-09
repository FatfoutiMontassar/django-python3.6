/*
  responsible for the selection and deselection of products on the
  'attach products' process , it's also responsible for filtering the
  products whenever the user types a new letter.
*/
$(function(){
  var scrolled = 0
  $(".list-group").on("click",".list-group-item",function(){
    if($(this).hasClass("product")){
        if($(this).hasClass("active")){
          $(this).removeClass().addClass('list-group-item').addClass('product')
        }else{
          $(this).removeClass().addClass('list-group-item').addClass('active').addClass('product')
        }
    }else{
        //alert("not product ...")
    }
  });
  function fun(str1,str2){
    for(var i = 0 ; i <= str1.length-str2.length ; i++){
      var ret = true
      for(var j = 0 ; j < str2.length ; j++){
        if(str1[i+j] != str2[j]){
          ret = false
          break
        }
      }
      if(ret == true)return true
    }
    return false
  }
  $("#choose-list-search").keyup(function(){
    if($("#choose-list-search").val() != "" ){
      var input = $("#choose-list-search").val()
      $("#list-of-selected-products").children('a').each(function(){
        $(this).css('display','')
      });
      $("#list-of-selected-products").children('a').each(function(){
        product_name = $(this).attr("product-name")
        if(!fun(product_name.toLowerCase(),input.toLowerCase()) && !fun(input.toLowerCase(),product_name.toLowerCase()) && !$(this).hasClass('active') ){
          //alert(product_name + "1")
          $(this).css('display','none')
        }else{
          //alert(product_name + "2")
        }
      });
    }else{
      $("#list-of-selected-products").children('a').each(function(){
        $(this).css('display','')
      });
    }
  });
});

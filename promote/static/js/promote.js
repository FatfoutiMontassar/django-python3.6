$(function() {
	//console.log("hello from redirect !!!") ;
	redirectFromTable = function(x){
		var link = '' ;
		switch (x){
		case 0 :
			link = 'Settings' ;
		break;
		case 1 :
			link = 'Info' ;
		break ;
		case 2 :
			link = 'Payment' ;
		break ;
		case 3:
			link = 'About' ;
		break;
		case 4:
			link = 'Options' ;
		break;
		case 5:
			link = 'Promote' ;
		break;
		case 6:
			link = 'Listings' ;
		break;
		default:
			link = 'Settings' ;
		break;
		}
	
		var csrf = $("#sidebar").attr("csrf")
		$.ajax({
	        url: '/promote/redirect'+link+'/',
	      data:{
	        'csrfmiddlewaretoken': csrf,
	      },
	      cache: false,
	      type:'post',
	      success: function (data) {
	        $("#mainSpan").html(data);
	      },
	    });
	}

});

$(function () {
    var substringMatcher = function(strs) {
    //window.alert("it_s not working !! " + q);
    return function findMatches(q, cb) {
      //window.alert(q + " : " + cb);
      var matches, substringRegex;
      matches = [];
      substrRegex = new RegExp(q, 'i');
      $.each(strs, function(i, str) {
        if (substrRegex.test(str) && matches.length < 6 ) {
          matches.push({ value: str });
        }
      });
      cb(matches);
    };
  };

  $.ajax({
    url: '/shop/products/',
    cache: false,
    success: function (data) {
      $('#q').typeahead({
        hint: true,
        highlight: true,
        minLength: 1
      },
      {
        name: 'data',
        displayKey: 'value',
        source: substringMatcher(data)
      });
      //window.alert(substringMatcher(data))
    }
  });
});

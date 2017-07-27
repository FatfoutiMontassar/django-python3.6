$(function () {
  var substringMatcher = function(strs) {
    return function findMatches(q, cb) {
      //window.alert(q + " : " + cb);
      var matches, substringRegex;
      matches = [];
      substrRegex = new RegExp(q, 'i');
      $.each(strs, function(i, str) {
        if (substrRegex.test(str)) {
          matches.push({ value: str });
        }
      });
      cb(matches);
    };
  };

  $.ajax({

    url: '/messenger/users/',
    //url: '/shop/products',
    cache: false,
    success: function (data) {
      $('#to').typeahead({
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

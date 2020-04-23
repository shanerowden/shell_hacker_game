$(function() {
  let timer = null;
  let xhr = null;
  $('.test-popup').hover(
    function(event) {
      // mouse in element handler
      let elem = $(event.currentTarget);
      timer = setTimeout(function() {
        timer = null;
        xhr = $.ajax(
          '/campaign/' + elem.first().text().trim() + '/popup').done(
            function(data) {
              xhr = null;
              // create and display popup here
              elem.popover({
                trigger: 'manual',
                html: true,
                animation: true,
                container: elem,
                content: data
              }).popover('show')
            }
          );
      }, 250);
    },
    function(event) {
      // mouse over event handler
      var elem = $(event.currentTarget);
      if (timer) {
        clearTimeout(timer);
        timer = null;
      }
      else if (xhr) {
        xhr.abort();
        xhr = null;
      }
      else {
        elem.popover('dispose');
      }
    }
  )
});

// popover
$(document).ready(function() {
  $('[data-toggle="popover"]').popover({html:true});
});

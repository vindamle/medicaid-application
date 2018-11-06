$(document).ready(function () {
  var url = window.location.pathname;
  $('a[href="'+ url +'"]').addClass('currentPage');
});

$(document).ready( () => {
    $('table').dataTable( {
    "paging": false
} );
});

// Call Datatables with parameters
$(document).ready( () => {
  $('table').dataTable({
	  "paging": false,
	  "info": false
	});
});

$(document).ready(function () {
  var url = window.location.pathname;
  $('a[href="'+ url +'"]').addClass('currentPage');
});


// show Table Count next to headings
const showTableCount = (table) => {
  const countSpanId = table.parentNode.id + "Count";
  const countSpan = document.getElementById(countSpanId);
  const count =table.children.length;
  countSpan.innerHTML = count;
};

const tables = document.getElementsByTagName('tbody')
for (var i = 0; i < tables.length; i++) {
  showTableCount(tables[i]);
};

// jQuery AJAX request to track or ignore residents, then remove resident's row from view upon success
const trackOrIgnore = (row, trueOrFalse) => {
	const ajaxCall = $.ajax(
	{
		type:"GET",
		url: "/application/ajax/track_or_ignore",
		data:{
			patient_id: row.id,
			tracking: trueOrFalse
		},
		success: function() 
		{
			const table = row.parentNode;
			$(row).remove();
			showTableCount(table);
		}
	});
	return(ajaxCall);
}
  
$('.btn-track').click(function(){
    const row = this.parentNode.parentNode;
    trackOrIgnore(row, true);
});

$('.btn-ignore').click(function(){
  button = this;
  // console.log(button);
  if (confirm("Are you sure you want ignore this alert?")) {
    const row = this.parentNode.parentNode;
    trackOrIgnore(row, false);
   };
});
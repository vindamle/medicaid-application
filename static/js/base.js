
$(document).ready( () => {
// Call Datatables with parameters
  $('table:not(.miscDocsTable)').dataTable({
	  "paging": false,
	  "info": false
	});
	$('.content').fadeIn(200);

	//datatable search fields styling
	const filters = document.querySelectorAll('.dataTables_filter')
	for (var i = 0; i < filters.length; i++) {
		let filter = filters[i]
		let input = filter.firstElementChild.firstElementChild
		input.style.border = "2px solid #eee"
		// input.style.boxShadow = "1px 1px 1px #aaa"
		// input.style.backgroundColor = "#eee"
		input.style.padding = "5px 15px"
		input.style.textAlign = "center"
		$(input).focus(() => {
			input.style.outline = "none"
		// input.style.boxShadow = "inset 1px 1px 1px #aaa"
		})
		// input.addClass('fdsa')
		// $('.asdf').css('background-color', 'red')
		input.setAttribute('placeholder', 'Search This Table')
		filter.removeChild(filter.firstElementChild)
		filter.appendChild(input)
	}

  var url = window.location.pathname;
  $('a[href="'+ url +'"]').addClass('currentPage');
});

// show Table Count next to headings
const showTableCount = table => {
  const countSpanId = table.parentNode.id + "Count";
  const countSpan = document.getElementById(countSpanId);
  const count =table.children.length;
  if(countSpan) {
  	countSpan.innerHTML = count;
  }
};

const tables = document.getElementsByTagName('tbody')
for (var i = 0; i < tables.length; i++) {
  showTableCount(tables[i]);
};

// for Activity Page, show total of all activity next to heading
const totalActivityCountSpan = document.getElementById('totalActivityCount');
const countSpans = document.querySelectorAll('.countSpan')

const showTotalActivityCount = () => {
  let total = 0;
  for (var i = 0; i < countSpans.length; i++) {
	  total += parseInt(countSpans[i].textContent);
	};
	if (totalActivityCountSpan) {
		totalActivityCountSpan.innerHTML = total;
	}
};
if (totalActivityCountSpan) {
	showTotalActivityCount();
}
// jQuery AJAX request to track or ignore residents, then remove resident's row from view upon success
const trackOrIgnore = (row, trueOrFalse) => {
	const ajaxCall = $.ajax(
	{
		type:"GET",
		url: "/application/ajax/track_or_ignore",
		data:{
			row_id: row.id,
			tracking: trueOrFalse
		},
		success: function()
		{
			const table = row.parentNode;
			$(row).remove();
			// $(row).fadeOut(30);
			showTableCount(table);
			showTotalActivityCount();
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
  if (confirm("Are you sure you want stop tracking this resident? (They'll still be available in 'Not Tracking' if you change your mind.)")) {
    const row = this.parentNode.parentNode;
    trackOrIgnore(row, false);
   };
});

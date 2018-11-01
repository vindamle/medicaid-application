// jQuery AJAX request to track or ignore residents and remove resident's row from view upon success
$('.btn-track').click(function(){
    const row = this.parentNode.parentNode;
    $.ajax(
    {
        type:"GET",
        url: "/application/ajax/track_or_ignore",
        data:{
                 patient_id: row.id,
                 tracking: true
        },
        success: function() 
        {
            row.parentNode.removeChild;
        }
     })
});

$('.btn-ignore').click(function(){
  if (confirm("Are you sure you want ignore this alert?")) {
    const row = this.parentNode.parentNode;
    $.ajax(
      {
        type:"GET",
        url: "/application/ajax/track_or_ignore",
        data:
          {
            patient_id: row.id,
            tracking: false
          },
        success: function() 
          {
            row.parentNode.removeChild;
          }
     });
   };
});

// const trackSelectedBtn = document.getElementById('trackSelectedBtn');

// document.addEventListener('click', (e) => {
// //change row color when clicking/unclicking 'Track' button
// 	if (e.target.parentNode.classList.contains('trackBtnCell')) {
// 		const button = e.target;
// 		if (e.target.textContent == 'Track') {
// 			e.target.textContent = '\u2713';
// 			button.className = 'btn-tracked';
// 		} else {
// 			e.target.textContent = 'Track';
// 			button.className = 'btn-track';
// 		};
//   } else if (e.target.className == 'btn-ignore') {
// 		if (confirm("Are you sure you want ignore this alert?")) {
// 			const row = e.target.parentNode.parentNode;
// 			$(row).remove();
// 		} else if (e.target == trackSelectedBtn) {
// 		const tracked = document.querySelectorAll('.btn-tracked');
// 		console.log(tracked);
// 		for (var i = 0; i < tracked.length; i++) {
// 			const row = tracked[i].parentNode.parentNode;
// 			console.log(row);
// 			$(row).remove();
// 		};
// 	};
// };
// });



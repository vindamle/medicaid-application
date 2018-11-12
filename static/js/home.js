// jQuery AJAX request to stop tracking residents
// $('.btn-track').click(function(){
//     const row = this.parentNode.parentNode;
//     $.ajax(
//     {
//         type:"GET",
//         url: "/application/ajax/track_or_ignore",
//         data:{
//                  patient_id: row.id,
//                  tracking: true
//         },
//         success: function() 
//         {
//             $(row).remove();
//         }
//      })
// });

// $('.btn-ignore').click(function(){
//   if (confirm("Are you sure you want ignore this alert?")) {
//     const row = this.parentNode.parentNode;
//     $.ajax(
//       {
//         type:"GET",
//         url: "/application/ajax/track_or_ignore",
//         data:
//           {
//             patient_id: row.id,
//             tracking: false
//           },
//         success: function() 
//           {
//             $(row).remove();
//           }
//      });
//    };
// });

// // 'Remove' button demo functionality (doesn't affect database yet)
// const trackedResidentsTable = document.querySelector('#trackedResidentsTable');
// trackedResidentsTable.addEventListener('click', (e) => {
// 	if (e.target.className == 'btn-remove') {
// 		if (confirm("Are you sure you want to stop tracking this resident?")) {
// 			const row = e.target.parentNode.parentNode;
// 			const rowParent = row.parentNode;
// 			rowParent.removeChild(row);
// 		};
// 	};
// });

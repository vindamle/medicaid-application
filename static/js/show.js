// jQuery AJAX request to track or ignore residents, then remove resident's row from view upon success

const editBtn = document.querySelector("#editBtn");
const patientId = document.querySelector("#patientId").innerHTML;
// const uploadFile = (patient_id, file) => {
// 	const ajaxCall = $.ajax(
// 	{
// 		type:"GET",
// 		url: "/application/ajax/file_uploader",
// 		data:{
// 			patient_id: patient_id,
// 			file: file
// 		},
// 		success: function() 
// 		{
		
// 		}
// 	});
// 	return(ajaxCall);
// };

$(editBtn).click(() => {
	const applicationFile = document.getElementById('medicaidApplicationFile');
	const file = applicationFile.files[0];
	// uploadFile(patientId, file);
	const ajaxCall = $.ajax(
	{
		type:"GET",
		contentType: false,
		processData: false,
		url: "/application/ajax/file_uploader",
		data:{
			patient_id: patientId,
			file: file
		},
		success: function() 
		{
			alert('file uploaded!');
		}
	});
	return(ajaxCall);
});


// $('.editable').dblclick((e) => {
// 	const	editableItem = e.target;
// 	const input = document.createElement('input');
// 	input.type = 'text';
// 	input.value = editableItem.textContent;
// 	input.className = 'editable';
// 	const parent = editableItem.parentNode;
// 	parent.insertBefore(input, editableItem);
// 	parent.removeChild(editableItem);
// 	parent.style.borderBottom="none";
// });


// Toggle fields in and out of editable state on show pages
// const editBtn = document.querySelector("#editBtn");
// editBtn.addEventListener('click', (e) => {	
// 	const editableItems = document.querySelectorAll('.editable');
// 	if (editBtn.textContent == 'Edit') {
// 			for (var i = 0; i < editableItems.length; i++) {
// 			const	editableItem = editableItems[i]
// 			const input = document.createElement('input');
// 			input.type = 'text';
// 			input.value = editableItem.textContent;
// 			input.className = 'editable';
// 			const parent = editableItem.parentNode;
// 			parent.insertBefore(input, editableItem);
// 			parent.removeChild(editableItem);
// 			parent.style.borderBottom="none";
// 			const ul = parent.parentNode;
// 			ul.style.textAlign = 'right';
// 			editBtn.textContent = 'Save';
// 			editBtn.classList.toggle('saveBtn');
// 		};
// 	} else if (editBtn.textContent == 'Save') {
// 			for (var i = 0; i < editableItems.length; i++) {
// 			const editableItem = editableItems[i]
// 			const span = document.createElement('span');
// 			span.textContent = editableItem.value;
// 			span.className = 'editable';
// 			const parent = editableItem.parentNode;
// 			parent.insertBefore(span, editableItem);
// 			parent.removeChild(editableItem);
// 			parent.style.borderBottom="1px solid #ddd";
// 			const ul = parent.parentNode;
// 			ul.style.textAlign = 'left';
// 			editBtn.textContent = 'Edit';
// 			editBtn.classList.toggle('saveBtn');
// 		};
// 	};
// });
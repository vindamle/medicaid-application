//file upload button functionality
// const patientId = document.querySelector("#patientId").innerHTML;
// const uploadFile = (fileType, file) => {
// 	const ajaxCall = $.ajax(
// 	{
// 		type:"GET",
// 		url: "/application/ajax/file_uploader",
// 		contentType: false,
// 		processData: false,
// 		data:{
// 			patient_id: patientId,
// 			fileType: fileType,
// 			file: file
// 		},
// 		success: function(response) 
// 		{
// 			console.log(response);
// 			alert(`File uploaded! (Response: ${response})`);
// 		}
// 	});
// 	return(ajaxCall);
// };

// $('.uploadBtn').click((e) => {
// 	li = e.target.parentNode;
// 	const fileType = li.id;
// 	const file = li.querySelector('input').files[0];
// 	console.log(file);
// 	if (file) {
// 		uploadFile(fileType, file);
// 	} else {
// 		alert("Please select a file to upload.")
// 	};	
// });


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
const editBtn = document.querySelector("#editBtn");
editBtn.addEventListener('click', (e) => {	
	const editableItems = document.querySelectorAll('.editable');
	if (editBtn.textContent == 'Edit') {
			for (var i = 0; i < editableItems.length; i++) {
			const	editableItem = editableItems[i]
			const input = document.createElement('input');
			input.className = 'editable';
			if (editableItem.classList.contains('date')) {
				input.type = 'date';
				input.classList.add('date');
			} else {
				input.type = 'text';
			};
			input.value = editableItem.textContent;
			
			const parent = editableItem.parentNode;
			parent.insertBefore(input, editableItem);
			parent.removeChild(editableItem);
			parent.style.borderBottom="none";
			const ul = parent.parentNode;
			ul.style.textAlign = 'right';
			editBtn.textContent = 'Save';
			editBtn.classList.toggle('saveBtn');
		};
	} else if (editBtn.textContent == 'Save') {
			for (var i = 0; i < editableItems.length; i++) {
			const editableItem = editableItems[i]
			const span = document.createElement('span');
			span.textContent = editableItem.value;
			span.className = 'editable';
			if (editableItem.classList.contains('date')) {
				span.classList.add('date');
			};
			const parent = editableItem.parentNode;
			parent.insertBefore(span, editableItem);
			parent.removeChild(editableItem);
			parent.style.borderBottom="1px solid #ddd";
			const ul = parent.parentNode;
			ul.style.textAlign = 'left';
			editBtn.textContent = 'Edit';
			editBtn.classList.toggle('saveBtn');
		};
	};
});

//code below, if implemented, would allow for fields to be edited individually by double-clicking them

// document.addEventListener('dblclick', (e)=>{
// 	if (e.target.classList.contains('editable')) {
// 		const editableItem = e.target;
// 		const input = document.createElement('input');
// 		input.className = 'editable';
// 		if (editableItem.classList.contains('date')) {
// 			input.type = 'date';
// 			input.classList.add('date');
// 		} else {
// 			input.type = 'text';
// 		};
// 		input.value = editableItem.textContent;
// 		const parent = editableItem.parentNode;
// 		parent.insertBefore(input, editableItem);
// 		parent.removeChild(editableItem);
// 		parent.style.borderBottom="none";

// 		input.addEventListener('keyup',function(e){
// 	    if (e.keyCode === 13) {
// 		    const span = document.createElement('span');
// 				span.textContent = input.value;
// 				span.className = 'editable';
// 				if (input.classList.contains('date')) {
// 					span.classList.add('date');
// 				};
// 				const parent = input.parentNode;
// 				parent.insertBefore(span, input);
// 				parent.removeChild(input);
// 				parent.style.borderBottom="1px solid #ddd";
// 		  };
// 		});
// 	};
// });

$('#approveBtn').click((e) => {
	btn = e.target;
	if(btn.innerHTML == 'Approve') {
		e.target.innerHTML = 'Approved &check;';
		$('#approvedSection').css('display', 'block');
	} else {
		e.target.innerHTML = 'Approve';
		$('#approvedSection').css('display', 'none');
	}
})
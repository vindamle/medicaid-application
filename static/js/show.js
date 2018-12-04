const updateField = (field, newValue) => {
	const patientId = document.querySelector("#patientId").innerHTML;
	const ajaxCall = $.ajax(
	{
		type:"GET",
		url: "/application/ajax/updateField",
		data:{
			patient_id: patientId,
			field: field,
			newValue: newValue
		},
		success: function() 
		{
			console.log("Value of " + field + " set to " + newValue)
		}
	});
	return(ajaxCall);
}

const replaceElement = (oldElement, newElementType) => {
	const newElement = document.createElement(newElementType);
	newElement.id = oldElement.id;
	newElement.classList = oldElement.classList;
	const parent = oldElement.parentNode;
	
	if (newElementType == 'input') {
		newElement.value = oldElement.textContent;
		if (newElement.classList.contains('date')) {
			newElement.type = 'date';
		} else {
			newElement.type = 'text';
		};

		parent.style.borderBottom="none";

		//Pressing 'Enter' in an input leaves editing mode
		newElement.addEventListener('keyup',function(e){
	    if (e.keyCode === 13) {
	    	updateField(newElement.id, newElement.value)
		    replaceElement(newElement, 'span');
		  };
		});
	} else if (newElementType == 'span') {
		newElement.textContent = oldElement.value;
		parent.style.borderBottom="1px solid #ddd";
	};
	$(oldElement).replaceWith(newElement);
};

// Allow fields to be individually toggled in and out of editing mode by double-clicking them

document.addEventListener('dblclick', (e)=>{
	if (e.target.classList.contains('editableLi') || e.target.parentNode.classList.contains('editableLi')) {
		// leave editing mode of any other inputs and updates them
		const activeInputs = document.querySelectorAll('INPUT.editable');
		for (var i = 0; i < activeInputs.length; i++) {
			const input = activeInputs[i];
			updateField(input.id, input.value);
			replaceElement(input, 'span');
		};

		let span = e.target;
 		if (span.tagName == 'LABEL') {
			span = e.target.nextElementSibling;
		} else if (span.tagName == 'LI') {
			span = e.target.getElementsByTagName('SPAN')[0];
		};
		replaceElement(span, 'input');
	};
});


// Approve Button toggles display of Approval Information Section

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

// const replaceInputWithSpan = input => {
// 	const span = document.createElement('span');
// 	span.id = input.id;
// 	span.textContent = input.value;
// 	span.classList = input.classList;
// 	const parent = input.parentNode;
// 	parent.style.borderBottom="1px solid #ddd";
// 	$(input).replaceWith(span);
// }

// const replaceSpanWithInput = span => {
// 		const input = document.createElement('input');
// 		input.id = span.id;
// 		input.classList = span.classList;
// 		if (input.classList.contains('date')) {
// 			input.type = 'date';
// 		} else {
// 			input.type = 'text';
// 		};
// 		input.value = span.textContent;
// 		const parent = span.parentNode;
// 		parent.style.borderBottom="none";
// 		$(span).replaceWith(input);

// 		//Pressing 'Enter' leaves editing mode

// 		input.addEventListener('keyup',function(e){
// 	    if (e.keyCode === 13) {
// 	    	updateField(input.id, input.value)
// 		    replaceInputWithSpan(input);
// 		  };
// 		});
// }

// File upload button functionality (NOTE: possibly irrelevant - it may not be possible to ajax file uploads)
//
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

// Toggle fields in and out of editable state on show pages with Edit Button

// const editBtn = document.querySelector("#editBtn");
// editBtn.addEventListener('click', (e) => {	
// 	const editableItems = document.querySelectorAll('.editable');
// 	if (editBtn.textContent == 'Edit') {
// 			for (var i = 0; i < editableItems.length; i++) {
// 			const	editableItem = editableItems[i]
// 			const input = document.createElement('input');
// 			input.className = 'editable';
// 			if (editableItem.classList.contains('date')) {
// 				input.type = 'date';
// 				input.classList.add('date');
// 			} else {
// 				input.type = 'text';
// 			};
// 			input.value = editableItem.textContent;
			
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
// 			if (editableItem.classList.contains('date')) {
// 				span.classList.add('date');
// 			};
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
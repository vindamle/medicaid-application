const meetingCheckbox = document.querySelector('.meetingCheckbox');
$(document).ready(()=>{
	if(meetingCheckbox.checked) {
	$('.step2').css('display', 'inline-block');
}
})
meetingCheckbox.addEventListener('change', () => {
	if(meetingCheckbox.checked) {
		const dataObject = {
			resident_id: document.querySelector("#residentId").innerHTML,
			column: "met_with_applicant",
			new_value: true
		}
		const table = "application";
		const successMessage = `Value of ${dataObject.column} in the ${table} table set to ${dataObject.new_value}`;
		updateDB(table, dataObject, successMessage);
		$('.step2').css('display', 'inline-block');
	} else {
		$('.step2').css('display', 'none');
	}
})

// Make select fields default to value (if there is one) in database:
const selectFields = document.querySelectorAll('SELECT');
for (let i = 0; i < selectFields.length; i++) {
	const selectField = selectFields[i];
	const selectFieldParent = selectField.parentNode;
	const DBinfo = selectFieldParent.querySelector('.DBinfo').innerHTML;
	const options = selectField.querySelectorAll('OPTION');
	for (let x = 0; x < options.length; x++) {
		const option = options[x];
		if (option.value == DBinfo) {
			option.setAttribute("selected", "selected");
		};
	};
};

//send AJAX call from select and radio button fields:
// REFACTOR THESE TWO FUNCTIONS:
for (let i = 0; i < selectFields.length; i++) {
	const selectField = selectFields[i];
	selectField.addEventListener('change', () => {
		const table = selectField.getAttribute('data-table');
			const dataObject = {
				resident_id: document.querySelector("#residentId").innerHTML,
				column: selectField.getAttribute('name'),
				new_value: selectField.value
			};
			const successMessage = `Value of ${dataObject.column} in the ${table} table set to ${dataObject.new_value}`;
			updateDB(table, dataObject, successMessage);
	});
};

const radio_forms = document.querySelectorAll('.radio_form');
for (let i = 0; i < radio_forms.length; i++) {
	const radio_form = radio_forms[i];
	radio_form.addEventListener('click',(e)=> {
		if (e.target.value) {
			const table = radio_form.getAttribute('data-table');
			const dataObject = {
				resident_id: document.querySelector("#residentId").innerHTML,
				column: e.target.getAttribute('name'),
				new_value: e.target.value
			};
			const successMessage = `Value of ${dataObject.column} in the ${table} table set to ${dataObject.new_value}`;
			updateDB(table, dataObject, successMessage);
		};
	});
};

const updateDB = (table, dataObject, successMessage) => {
	const ajaxCall = $.ajax(
	{
		type:"GET",
		url: `/application/ajax/update_${table}`,
		data: dataObject,
		success: function() 
		{
			console.log(successMessage)
		}
	});
	return(ajaxCall);
}

const sendInputInfoToDB = input => {
	const table = input.getAttribute('data-table');
	let dataObject = {
		resident_id: document.querySelector("#residentId").innerHTML,
		column: input.id,
		new_value: input.value
	};
	let successMessage = `Value of ${dataObject.column} in the ${table} table set to ${dataObject.new_value}`;
	updateDB(table, dataObject, successMessage);
	const alertId = input.getAttribute('data-alert_id');
	if (alertId != "") {
		 dataObject = {
		 	alert_id: alertId,
			addressed: true
		 };
		 successMessage = `Value of 'addressed' for alert with id ${dataObject.alert_id} in the alert table set to ${dataObject.addressed}`;
		 updateDB("alert", dataObject, successMessage);
	}
}

const replaceElement = (oldElement, newElementType) => {
	const newElement = document.createElement(newElementType);
	newElement.id = oldElement.id;
	newElement.classList = oldElement.classList;
	newElement.setAttribute("data-table", oldElement.getAttribute("data-table"));
	newElement.setAttribute("data-alert_id", oldElement.getAttribute("data-alert_id"));
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
				sendInputInfoToDB(newElement);
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
		for (let i = 0; i < activeInputs.length; i++) {
			const input = activeInputs[i];
			sendInputInfoToDB(input);
  		replaceElement(input, 'span');
		};
		let span = e.target;
 		if (span.tagName == 'LABEL') {
			span = e.target.parentNode.querySelector('SPAN')
		} else if (span.tagName == 'LI') {
			span = e.target.querySelector('SPAN');
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

// const updateDB = (table, column, newValue) => {
// 	const residentId = document.querySelector("#residentId").innerHTML;
// 	const ajaxCall = $.ajax(
// 	{
// 		type:"GET",
// 		url: `/application/ajax/update_${table}`,
// 		data:{
// 			resident_id: residentId,
// 			column: column,
// 			new_value: newValue
// 		},
// 		success: function() 
// 		{
// 			console.log(`Value of ${column} in the ${table} table set to ${newValue}`)
// 		}
// 	});
// 	return(ajaxCall);
// }

// const updateAlert = (alertId, newValue) => {
// 	const ajaxCall = $.ajax(
// 	{
// 		type:"GET",
// 		url: `/application/ajax/update_alert`,
// 		data:{
// 			alert_id: alertId,
// 			addressed: newValue
// 		},
// 		success: function() 
// 		{
// 			console.log(`Value of 'addressed' for alert with id ${alertId} in the alert table set to ${newValue}`)
// 		}
// 	});
// 	return(ajaxCall);
// }

// File upload button functionality (NOTE: possibly irrelevant - it may not be possible to ajax file uploads)
//
// const residentId = document.querySelector("#residentId").innerHTML;
// const uploadFile = (fileType, file) => {
// 	const ajaxCall = $.ajax(
// 	{
// 		type:"GET",
// 		url: "/application/ajax/file_uploader",
// 		contentType: false,
// 		processData: false,
// 		data:{
// 			resident_id: residentId,
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
// 			for (let i = 0; i < editableItems.length; i++) {
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
// 			for (let i = 0; i < editableItems.length; i++) {
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
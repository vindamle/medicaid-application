


const phaseChange = new_phase_id => {
	const dataObject = {
		resident_id: document.querySelector("#residentId").innerHTML,
		phase_id: new_phase_id
	}
		const successMessage = `phase changed to ${dataObject.phase_id}`;
		const ajaxCall = $.ajax(
	{
		type:"GET",
		url: `/application/ajax/phase_change/`,
		data: dataObject,
		success: function() 
		{
			console.log(successMessage)
		}
	});
	$('#phase').innerHTML = new_phase_id;
	console.log($('#phase'));
	return(ajaxCall);
}

const meetingCheckbox = document.querySelector('.meetingCheckbox');
$(document).ready(()=>{
	if(meetingCheckbox.checked) {
	$('.step2').css('display', 'block');
}
})

meetingCheckbox.addEventListener('change', (e) => {
	if(meetingCheckbox.checked) {
		if(!$('#appointment_date').val()){
			alert("Please enter a meeting Date")
			meetingCheckbox.checked = false;
			return;
		} 
			$('.step2').css('display', 'block');
			phaseChange(2);
	} else {
		$('.step2').css('display', 'none');
		$('.step3').css('display', 'none');
		phaseChange(1);
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

const editableInputs = document.querySelectorAll('INPUT.editable');
for (var i = 0; i < editableInputs.length; i++) {
	const input = editableInputs[i]
	input.addEventListener('click', () => {
		input.select();
	})
	// Pressing 'Enter' in an input leaves editing mode - MIGHT BE IRRELEVANT, AS PRESSING 'ENTER' = FOCUSOUT
	input.addEventListener('keyup',(e)=>{
    if (e.keyCode === 13) {
    	// if the field user is completing is medicaid pickup date, show fields relevant to next step:
    	if (input.id == "medicaid_pickup_date") {
    		$('.step3').css('display', 'block');
    	};
			// sendInputInfoToDB(input);			
			// replaceElement(input, 'span');
			input.blur(); // this will trigger the 'blur' eventListener and send info to DB
	  };
	});
	input.addEventListener('blur',()=>{
  	// if the field user is completing is medicaid pickup date, show fields relevant to next step:
  	if (input.id == "medicaid_pickup_date" && input.value != "") {
  		$('.step3').css('display', 'block');
  	};
		sendInputInfoToDB(input);
		// replaceElement(newElement, 'span');
	});
};

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
		//Pressing 'Enter' in an input leaves editing mode - MIGHT BE IRRELEVANT, AS PRESSING 'ENTER' = FOCUSOUT
		// newElement.addEventListener('keyup',function(e){
	    // if (e.keyCode === 13) {
	    	// if the field user is completing is medicaid pickup date, show fields relevant to next step:
	   //  	if (newElement.id == "medicaid_pickup_date") {
	   //  		$('.step3').css('display', 'block');
	   //  	};
				// sendInputInfoToDB(newElement);
  			// replaceElement(newElement, 'span');
		  // };
		// });

		newElement.addEventListener('blur',function(e){
    	// if the field user is completing is medicaid pickup date, show fields relevant to next step:
    	if (newElement.id == "medicaid_pickup_date" && newElement.value != "") {
    		$('.step3').css('display', 'block');
    	};
			sendInputInfoToDB(newElement);
			// replaceElement(newElement, 'span');
		});

	} else if (newElementType == 'span') {
		newElement.textContent = oldElement.value;
		parent.style.borderBottom="1px solid #ddd";
	};

	$(oldElement).replaceWith(newElement);
	newElement.focus();
	console.log("Here's newElement: " + newElement)
	setTimeout(function () { newElement.select(); }, 50);
};

// Allow fields to be individually toggled in and out of editing mode by clicking them
// document.addEventListener('click', (e)=>{
// 	if (e.target.classList.contains('editableLi') || e.target.parentNode.classList.contains('editableLi')) {
// 		// // leave editing mode of any other inputs and updates them
// 		// const activeInputs = document.querySelectorAll('INPUT.editable');
// 		// for (let i = 0; i < activeInputs.length; i++) {
// 		// 	const input = activeInputs[i];
// 		// 	sendInputInfoToDB(input);
//   // 		replaceElement(input, 'span');
// 		// };
// 		let span = e.target;
//  		if (span.tagName == 'LABEL') {
// 			span = e.target.parentNode.querySelector('SPAN')
// 		} else if (span.tagName == 'LI') {
// 			span = e.target.querySelector('SPAN');
// 		};
// 		replaceElement(span, 'input');
// 	};
// });

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

	<!-- <script type="text/javascript">

//	const addAjaxEventListenersToAllInputTypes = (parent) => {
// 	const inputs = parent.querySelectorAll('INPUT'); //this includes checkboxes
// 	const selectFields = parent.querySelector('SELECT');
// 	// Add eventListeners for select fields to send their info to DB via AJAX:
// 		for (let i = 0; i < selectFields.length; i++) {
// 		const selectField = selectFields[i];
// 		addSelectEventListener(selectField);
// 	};
// 	// Add eventListeners for inputs to focus them and send their info to DB via AJAX:
// 	for (var i = 0; i < inputs.length; i++) {
// 		const input = inputs[i]
// 		if (input.type == 'checkbox') {
// 			console.log("It's a checkbox!");
// 		} else {
// 			//add autofocus on clicking an input:
// 			input.addEventListener('click', () => {
// 				input.select();
// 			})
// 			// Pressing 'Enter' in an input leaves editing mode - MIGHT BE IRRELEVANT, AS PRESSING 'ENTER' = FOCUSOUT
// 			input.addEventListener('keyup',(e)=>{
// 		    if (e.keyCode === 13) {
// 					input.blur(); // this will trigger the 'blur' eventListener and send info to DB
// 			  };
// 			});
// 			// Leaving an input is same as pressing 'Enter':
// 			input.addEventListener('blur',()=>{
// 				sendInputInfoToDB(input);
// 			});
// 		}
// 	};
// }


// const documentation = [
// "U.S. Birth Certificate",
// "Naturalization papers or alien registration card",
// "Social Security Card",
// "Marriage/Divorce/Death Certificates",
// "Veterans discharge paperwork",
// "Medicare Card",
// "Other Health Insurance cards",
// "Proof of health insurance premiums",
// "If employed current pay stubs for past 8 weeks",
// "Social Security Amount Received Monthly:   Award letter",
// "Workers’ Compensation:   Award letter or Check stub ",
// "Veterans’ Benefits: award letter or letter from Veterans Affair",
// "Military Pay:  Award letter or pay stub",
// "Income from Rent or Room/Board:   Letter from roomer, boarder, tenant, copy of lease",
// "Private Pensions/Annuities:  Letter from company or pay stub",
// "Power of Attorney or statement assigning representative",
// "Property Deed",
// "All bank account statement for past 5 years",
// "Verification of any sold or closed stock accounts past 5 years",
// "Verification of any transferred property past 5 years",
// "Life insurance policies:  Cash and Face Values",
// "Copy of all Trust Funds",
// "Information on pending lawsuits",
// "Proof of Irrevocable burial accounts",
// "Burial Plots",
// "Unpaid medical bills",
// "Proof from Doctor at Nursing Home if short-term or long-term care"
// ]


// const third = documentation.length/3
// const columnsArray = [
// 	documentation.slice(0,third),
// 	documentation.slice(third,(third*2)),
// 	documentation.slice((third*2),documentation.length + 1)
// ]

// // function dividArray(myArray){
//     // let index = 0;
//     const arrayLength = documentation.length;
//     let tempArray = [];
//     for (let index = 0; index < arrayLength; index += 3) {
//         const myChunk = documentation.slice(index, index+3);
//         // Do something if you want with the group
//         tempArray.push(myChunk);
//     }
// console.log(tempArray)





// let rfiHTML = `
// <div class="container-fluid">
// 	<div class="row">
// `

// for (var i = 0; i < columnsArray.length; i++) {
// 	rfiHTML += "<div class='col-lg-4'>"
// 	const columnArray = columnsArray[i]
// 	let documentationChecklist = ""
// 	for (let i = 0; i < columnArray.length; i++) {
// 		doc = columnArray[i]
// 		const words = doc.split(' ')
// 		const docNoSpaces = words.join('_')
// 		documentationChecklist += `
// 		<input type="checkbox" value="${doc}" class="documentationCheckBox" id="${docNoSpaces}_checkbox"><label for="${docNoSpaces}_checkbox" class="documentationLabel">${doc}</label>
// 		<br>
// 		`
// 	}
// 	rfiHTML += documentationChecklist;
// 	rfiHTML += "</div>"
// }

// rfiHTML += `
// </div>
// </div>
// `
// let containsRow = false
// const addEventListenersToDocumentationCheckboxes = () => {
// 	document.addEventListener('change', (e) => {
// 		if (e.target.classList.contains('documentationCheckBox') && e.target.checked){
// 			if (!containsRow) {
// 				applicationInfoSection.innerHTML += "<h6>Documentation Upload</h6>"
// 				let containerDiv = document.createElement('DIV');
// 				containerDiv.classList.add('container-fluid')
// 				containerDiv.id = "documentUploadFormsDiv"
// 				let rowDiv = document.createElement('DIV');
// 				rowDiv.classList.add('row')
// 				rowDiv.id = "documentUploadFormsRow"
// 				containerDiv.appendChild(rowDiv)
// 				applicationInfoSection.appendChild(containerDiv)
// 				containsRow = true;
// 			}
// 			const checkbox = e.target;
// 			let rowDiv = document.querySelector('#documentUploadFormsRow')
// 			rowDiv.innerHTML += `
// 	 			<div class="col-lg-4">
// 	 				<form class="fileInputLi" id="${checkbox.id.slice(0, -9)}" method="post" enctype="multipart/form-data">
// 	 	  			{% csrf_token %}
// 	 					<label>Upload ${checkbox.value} Here:</label>
// 	 					<input type="file" name="${checkbox.id.slice(0, -9)}" value="{{application.rfi}}" accept="image/jpeg
// 	 					,image/png,application/pdf" multiple>
// 	 					<input type="hidden" name="resident_id" value="{{resident.resident_id}}">
// 	 					<input type="hidden" name="file_type" value="${checkbox.id.slice(0, -9)}">
// 	 					<button type="submit" class="uploadBtn">Upload</button>
// 	 				</form>
// 	 			</div>
// 	 		`
// 		};

// 	});
	// const documentationCheckBoxes = document.querySelectorAll('.documentationCheckBox');
	// for (var i = 0; i < documentationCheckBoxes.length; i++) {
	// 	const checkbox = documentationCheckBoxes[i];
	// 	console.log(checkbox)
	// 	checkbox.addEventListener('change', () => {
	// 		applicationInfoSection.innerHTML += `
	// 			<div class="col-lg-3">
	// 				<form class="fileInputLi" id="${checkbox.id.slice(0, -9)}" method="post" enctype="multipart/form-data">
	// 	  			{% csrf_token %}
	// 					<label>Upload ${checkbox.value} Here:</label>
	// 					<input type="file" name="${checkbox.id.slice(0, -9)}" value="{{application.medicaid_application}}" accept="image/jpeg
	// 					,image/png,application/pdf" multiple>
	// 					<input type="hidden" name="resident_id" value="{{resident.resident_id}}">
	// 					<input type="hidden" name="file_type" value="${checkbox.id.slice(0, -9)}">
	// 					<button type="submit" class="uploadBtn">Upload</button>
	// 				</form>
	// 			</div>
	// 		`
	// 	});
	// };
// }
// console.log(documentationChecklist);

		const personalInfoObjects = [];

		function newLi(labelValue, inputValue, inputType) {
			const liObject = {
				label: labelValue,
				value: inputValue,
				type: inputType
			};
			personalInfoObjects.push(liObject);
			// this.labelValue = labelValue;
  	// 	this.spanValue = spanValue;
		};

		const personalInfoFields = [
			['First Name','{{resident.first_name}}', 'text'],
			['Last Name','{{resident.last_name}}', 'text'],
			['Date of Birth','{{resident.dob|date:"Y-m-d"}}', 'date'],
		]

		// newLi('First Name','{{resident.first_name}}', 'text');
		// newLi('Last Name','{{resident.last_name}}', 'text');
		for (var i = 0; i < personalInfoFields.length; i++) {
			const field = personalInfoFields[i];
			newLi(field[0],field[1], field[2]);
		};

		// console.log(personalInfoObjects);
		const demoSection = document.querySelector('#demo');
		// const someText = "<span>Hello</span>"

		for (var i = 0; i < personalInfoObjects.length; i++) {
			const field = personalInfoObjects[i];
			demoSection.innerHTML += `
			<li class="editableLi">
				<label>${field['label']}</label>
				<input type="${field['type']}" class="editable" id="first_name" data-table="alert" data-alert_id="" value="${field['value']}">
			</li>
			`
		}

			const addEventListenerToResponse = (responseField.value) => {
			// const appSection = document.querySelector('#applicationInfoSection');
			// console.log(responseField);
			responseField.addEventListener('change', (e) => {
				// sendInputInfoToDB(response_select)
				// const options = responseField.querySelectorAll('OPTION');
				// 	for (let x = 0; x < options.length; x++) {
				// 		const option = options[x];
				// 		if (option.value == e.target.value) {
				// 			option.setAttribute("selected", "selected");
				// 		};
				// 	};
				//generate new html depending on selected option:

				if (e.target.value == 'rfi') {
					// send selection to db:
					// const section = e.target.parentNode.parentNode.parentNode.parentNode.parentNode;
					// const application_id = section.querySelector('.applicationId').innerHTML;
					// dataObject = {
					// 	// method: "create",
					// 	resident_id: {{resident.resident_id}},
					// 	application_id: application_id
					// 	// rfi_id:
					// }
					// updateDB("rfi", dataObject, "RFI row created!");
					// if approved was showing, unshow it:
					// $('#approvedSection').css('display', 'none');
					//add rfi section:
					// applicationInfoSection.insertAdjacentHTML("beforeend", newResponseRowHTML);
					// set application_id in needed sections of the new html:
					// section.querySelector('.formApplicationId').setAttribute('value', application_id)
					// const rfiRow = section.lastElementChild;
					// const elements = rfiRow.querySelectorAll('.needsAttributesSet');
					// for (var i = 0; i < elements.length; i++) {
					// 	const element = elements[i];
					// 	element.setAttribute('data-application_id', application_id);
					// }
					// addAjaxEventListenersToAllInputTypes(rfiRow)

					// let newID = `#response${submission}_select`
					// addEventListeners(newID);
					// const submittedCheckbox2 = document.querySelector('#documentationSubmittedCheckbox2');
					// $(document).ready(()=>{
					// 	if(submittedCheckbox2.checked) {
					// 		$('.step4').css('display', 'block');
					// 	}
					// });
					// submittedCheckbox2.addEventListener('change', (e) => {
					// 	if(submittedCheckbox2.checked) {
					// 		submission += 1;
					// 			$('.step4').fadeIn();
					// 	} else {
					// 		submission -= 1;
					// 		// $('.step4').css('display', 'none');
					// 	};
					// });
// 				}	else if (e.target.value == 'denied') {
// 					$('#approvedSection').css('display', 'none');
// 				} else if (e.target.value == 'approved'){
// 					$('#approvedSection').css('display', 'block');
// 				};
// 			});
// 		};

// 	</script> 
// •	Any admission that is Medicaid (or Mltc) should have a page created. The page should have:
// o	Name of resident (preferably generated from NCS)
// o	Admission date (preferably generated from NCS)
// o	Medicaid Pickup Date (i.e. the date from which Medicaid is needed to cover)
// o	Application type (New application, conversion, recertification – single, spousal, SSI)
// o	County in which the application is being filed (specific to most states which have a county system)
// o	Applicant resource information
// o	Income and NAMI information (preferably generated from NCS)

// Application History
// The program should include the following fields for data entry
// •	Date of application submission
// o	Field to upload the Medicaid application (requirements will vary by state)
// o	Field to upload confirmation of receipt by the Medicaid office
// •	Date of RFI issued by the Medicaid Office
// o	Field to upload RFI
// •	Date of RFI deadline
// •	Items required for the RFI (have it become a checklist once typed in as we have in some other programs)
// •	Note section for correspondence with the Medicaid office
// If approved
// •	Date of Medicaid approval
// o	Field to upload Medicaid approval
// •	Date recertification is needed
// If denied
// •	Date of Medicaid Denial
// o	Field to upload Medicaid denial
// •	Date of fair hearing request
// o	Field to upload confirmation of fair hearing request
// •	Date of fair hearing
// o	Field to upload fair hearing notice
// •	Denial triggers the need for new application which should restart the process

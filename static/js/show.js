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
	// console.log($('#phase'));
	return(ajaxCall);
}

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
	// If field affects alerts, update Alerts table:
	const alertId = input.getAttribute('data-alert_id');
	if (alertId != "") {
		 dataObject = {
		 	alert_id: alertId,
			addressed: true
		 };
		 successMessage = `Value of 'addressed' for alert with id ${dataObject.alert_id} in the alert table set to ${dataObject.addressed}`;
		 updateDB("alert", dataObject, successMessage);
	};
};

const sendSelectInfoToDB = selectField => {
	const table = selectField.getAttribute('data-table');
	const dataObject = {
		resident_id: document.querySelector("#residentId").innerHTML,
		column: selectField.getAttribute('name'),
		new_value: selectField.value
	};
	const successMessage = `Value of ${dataObject.column} in the ${table} table set to ${dataObject.new_value}`;
	updateDB(table, dataObject, successMessage);
};

const addSelectEventListener = selectField => {
	selectField.addEventListener('change', () => {
		sendSelectInfoToDB(selectField);
	});
};


const meetingCheckbox = document.querySelector('.meetingCheckbox');
$(document).ready(()=>{
	if(meetingCheckbox.checked) {
		$('.step2').css('display', 'block');
	}
})

meetingCheckbox.addEventListener('change', (e) => {
	if(meetingCheckbox.checked) {
		if(!$('#appointment_date').val()){
			alert("Please enter a meeting date")
			meetingCheckbox.checked = false;
			return;
		} 
			$('.step2').fadeIn();
			phaseChange(2);
	} else {
		$('.step2').css('display', 'none');
		$('.step3').css('display', 'none');
		phaseChange(1);
	}
})

// Make select fields default to value in database (if there is one):
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

// Add eventListeners for select fields to send their info to DB via AJAX: 
for (let i = 0; i < selectFields.length; i++) {
	const selectField = selectFields[i];
	if (selectField.id != 'response1_select') {
		addSelectEventListener(selectField);
	};
};

// Add eventListeners for inputs to focus them and send their info to DB via AJAX: 
const editableInputs = document.querySelectorAll('INPUT.editable');
for (var i = 0; i < editableInputs.length; i++) {
	const input = editableInputs[i]
	//add autofocus on clicking an input:
	input.addEventListener('click', () => {
		input.select();
	})
	// Pressing 'Enter' in an input leaves editing mode - MIGHT BE IRRELEVANT, AS PRESSING 'ENTER' = FOCUSOUT
	input.addEventListener('keyup',(e)=>{
    if (e.keyCode === 13) {
			input.blur(); // this will trigger the 'blur' eventListener and send info to DB
	  };
	});
	// Leaving an input is same as pressing 'Enter':
	input.addEventListener('blur',()=>{
  	// if the field user is completing is medicaid pickup date, show fields relevant to next step:
  	if (input.id == "medicaid_pickup_date" && input.value != "") {
  		$('.step3').fadeIn();
  		phaseChange(3);
  	};
		sendInputInfoToDB(input);
	});
};



// Approve Button toggles display of Approval Information Section
// const approveBtn = document.querySelector('#approveBtn');
// approveBtn.addEventListener('click', () => {
// 	if(approveBtn.innerHTML == 'Approve') {
// 		approveBtn.innerHTML = 'Approved &check;';
// 		$('#approvedSection').css('display', 'block');
// 	} else {
// 		approveBtn.innerHTML = 'Approve';
// 		$('#approvedSection').css('display', 'none');
// 	}
// })



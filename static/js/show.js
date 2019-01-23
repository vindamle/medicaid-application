const phaseChange = (element, phaseId) => {
	const dataObject = {
		application_id: element.getAttribute('data-application_id'),
		phase_id: phaseId
	};
		const successMessage = `phase changed to ${dataObject.phase_id}`;
		const ajaxCall = $.ajax(
	{
		type:"GET",
		url: `/application/ajax/phase_change/`,
		dataType: "html",
		data: dataObject,
		success: function(response) 
		{
			console.log(successMessage);
			const status = document.querySelector('#showStatus');
			status.innerHTML = `Status: ${response}`;
		}
	});
	return(ajaxCall);
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
};
const sendInputInfoToDB = input => {
	if(input.type == 'date' && parseInt(input.value) < 2010 || parseInt(input.value) > 2020) {
		alert("Sorry - that year is out of range.")
	} else if (input.value) {
		const table = input.getAttribute('data-table');
		let dataObject = {
			resident_id: document.querySelector("#residentId").innerHTML,
			column: input.id,
			new_value: input.value
		};
		if (table == "application") {
		 dataObject.application_id = input.getAttribute('data-application_id')
		} else if (table == "rfi") {
		 dataObject.rfi_id = input.getAttribute('data-rfi_id')	
		} else if (table == "approval") {
		 dataObject.approval_id = input.getAttribute('data-approval_id')	
		} else if (table == "denial") {
		 dataObject.denial_id = input.getAttribute('data-denial_id')	
		} else if (table == "nami") {
		 dataObject.nami_id = input.getAttribute('data-nami_id')
		}
		let successMessage = `Value of ${dataObject.column} in the ${table} table set to ${dataObject.new_value}`;
		updateDB(table, dataObject, successMessage);
		// If field affects alerts, update Alerts table:
		const alertId = input.getAttribute('data-alert_id');
		if (alertId) {
			 dataObject = {
			 	alert_id: alertId,
				addressed: true
			 };
			 if (table == "application") {
			 	dataObject.application_id = input.getAttribute('data-application_id')
			 }
			 successMessage = `Value of 'addressed' for alert with id ${dataObject.alert_id} in the alert table set to ${dataObject.addressed}`;
			 updateDB("alert", dataObject, successMessage);
		}
	}
};

const addSelectEventListener = selectField => {
	selectField.addEventListener('change', () => {
		sendInputInfoToDB(selectField);
	});
};

const alertDiv = document.querySelector('.alertDiv');
alertDiv.addEventListener('click', (e) => {
	if (e.target.classList.contains('dismissBtn')) {
		const alert = e.target.parentNode;
		const dataObject = {
			alert_id: alert.querySelector(".alertId").innerHTML,
			alert_status: true
		}
		const successMessage = `Alert status for alert with id ${dataObject.alert_id} set to true`;
		updateDB("alert", dataObject, successMessage)
		$(alert).css('display', 'none');
	}
});

const meetingCheckbox = document.querySelector('.meetingCheckbox');
$(document).ready(()=>{
	if(meetingCheckbox.checked) {
		$('.step2').css('display', 'block');
	}
})

const pickup_date = document.querySelector('#medicaid_pickup_date');
$(document).ready(()=>{
	if(pickup_date.value != "") {
		$('.step3').css('display', 'block');
	}
})

meetingCheckbox.addEventListener('change', () => {
	if(meetingCheckbox.checked) {
		if(!$('#appointment_date').val()){
			alert("Please enter a meeting date")
			meetingCheckbox.checked = false;
			return;
		} 
			$('.step2').fadeIn();
			 phaseChange(meetingCheckbox, 2);
	} else {
		$('.step2').css('display', 'none');
		$('.step3').css('display', 'none');
		 phaseChange(meetingCheckbox, 1);
	}
})

// Add eventListeners for select fields to send their info to DB via AJAX: 
const selectFields = document.querySelectorAll('SELECT');
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
  		 phaseChange(input, 3);
  		// console.log(phaseName)
  		// document.querySelector('#showStatus').innerHTML = phaseName;

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

// const collapsibleDiv = document.querySelector('.collapsible');
// collapsibleDiv.addEventListener('click', (e) => {
// 	const section = e.target.parentNode;
// 	const ul = e.target.nextElementSibling;
// 	$(ul).fadeOut(200, () => {
// 		section.style.height = "50px";
// 		section.style.width = "350px";
// 	});
	// section.classList.add('disappear');
	// const stuff = section.querySelectorAll('*:not(h4)')
	
	// section.style.overflow = "hidden";
	// for (var i = 0; i < stuff.length; i++) {
	// 	thingy = stuff[i];
	// 	thingy.style.display = "none";
	// }
// })



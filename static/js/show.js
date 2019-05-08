const phaseChange = (element, phaseId) => {
	let appId;
	// to check if this function is being called from the generateApproval() function, where there is no element:
	if (typeof(element.getAttribute) == 'function') {
		appId = element.getAttribute('data-application_id')
	} else {
		appId = element.appId
	}
	const dataObject = {
		application_id: appId,
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
			const status = document.querySelector(`#app${dataObject.application_id}showStatus`);
			status.innerHTML = `Status: ${response}`;
			const tab = document.querySelector(`#app${dataObject.application_id}TabPhaseName`);
			tab.innerHTML = response;
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
		success: function(response) 
		{
			if(dataObject.column == "medicaid_pickup_date") {
				formattedDeadline = response
				const appId = dataObject.application_id;
				const deadlineField = document.querySelector(`#application${appId} #date_of_application_submission_deadline`)
				deadlineField.value = formattedDeadline
			}
			console.log(successMessage)
		}
	});
};

const sendInputInfoToDB = input => {
	if(input.type == 'date' && (parseInt(input.value) < 2010 || parseInt(input.value) > 2100)) {
		alert("Sorry - that year is out of range. Please enter a year after 2010 and before, ya know, doomsday.")
	} else {
		let value;
		if(input.type == 'checkbox') {
			value = input.checked
		} else {
			value = input.value
		}
		const table = input.getAttribute('data-table');
		const rowId = input.getAttribute(`data-${table}_id`)
		let appId = "";
		if (table == "application") {
			appId = rowId;
		}
		let dataObject = {
			resident_id: document.querySelector("#residentId").innerHTML,
			application_id: appId,
			column: input.id,
			new_value: value,
			row_id: rowId
		};
		let successMessage = `Value of ${dataObject.column} in the ${table} table set to ${dataObject.new_value}`;
		updateDB(table, dataObject, successMessage);
	}
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

// Add eventListeners for inputs to focus them: 
const editableInputs = document.querySelectorAll('INPUT.editable');
editableInputs.forEach( input => {
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
  	};
  	sendInputInfoToDB(input);
	});
});

const verifyOrUnverify = (btn, appId) => {
	let trueOrFalse;
	$(btn).toggleClass('verified');
	if (btn.innerHTML == "Approval Not Verified") {
		btn.innerHTML = "Approval Verified &check;";
		trueOrFalse = "true"
	} else {
		btn.innerHTML = "Approval Not Verified";
		trueOrFalse = "false"
	}
	const ajaxCall = $.ajax(
	{
		type:"GET",
		url: "/application/ajax/approval_verified",
		data:{
			application_id: appId,
			approval_verified: trueOrFalse
		},
		success: function() 
		{
			console.log("approval set to " + trueOrFalse)
		}
	});
	return(ajaxCall);
}

// show proccessing overlay on refresh button click:

// $('.refreshBtn').click(()=>{
// 	$('#processingOverlay').css('display', 'block');
// })

const rotateArrow = refreshBtn => {
	$(refreshBtn).addClass('rotateZ')
}
	

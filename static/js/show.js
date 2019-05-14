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
			status.innerHTML = `Current Status: ${response}`;
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

// Make select fields default to value in database (if there is one):
	const selectFields = document.querySelectorAll('SELECT');
	selectFields.forEach( selectField => {
		const selectFieldParent = selectField.parentNode;
		const DBinfo = selectFieldParent.querySelector('.DBinfo').innerHTML;
		const options = selectField.querySelectorAll('OPTION');
		options.forEach(option => {
			if (option.value == DBinfo) {
				option.setAttribute("selected", "selected");
			};
		});
	});

// class ResponseRowHTML {
// 	constructor (applicationId, responseId, rfiOrDenialOrApprovalId, date) {
// 		this.rfiRowHtml = `
// 			<section id="rfi${rfiOrDenialOrApprovalId}">
// 				<button type="button" class="deleteResponseBtn" title="Delete this response" aria-label="Close" onclick="deleteResponse('rfi',${rfiOrDenialOrApprovalId})">
// 	        Delete This Response
// 	      </button>
// 				<h4 class="numberOfRFIs collapsibleSection responseH4" title="Click to minimize" onclick="collapseSection(this)">RFI #${numberOfRFIs}</h4>
// 				<ul class="collapsibleContent" id="">
// 					<div class="row">
// 						<div class="col-lg-3 firstColumn applicationColumn">
// 							<li>
// 								<label>Choose or <span class="dragNDropText">Drag n' Drop&trade;</span> RFI here:</label>
// 								<br>
// 								<input 
// 									type="file" 
// 									accept="image/jpeg,image/png,application/pdf" 
// 									onchange="
// 										uploadDoc(
// 											this, 
// 											${applicationId},
// 											'rfi',
// 											${rfiOrDenialOrApprovalId},
// 											'rfi'
// 										)
// 									"
// 								>
// 							</li>
// 						</div>
// 						<div class="col-lg-3 applicationColumn">
// 							<li class="editableLi ">
// 								<label>RFI Due Date:</label>
// 								<input class="editable date  due_date" id="rfi_due_date" data-table="rfi"  data-application_id="${applicationId}" data-rfi_id="${rfiOrDenialOrApprovalId}" type="date" onblur="sendInputInfoToDB(this)" onkeyup="checkIfEnterKey(this, event)" value="${date}">
// 							</li>
// 							<li class="editableLi">
// 								<label>Extension Requested?</label>
// 								<select name="rfi_extension_request" id="rfi_extension_request" data-table="rfi" data-application_id="${applicationId}" data-rfi_id="${rfiOrDenialOrApprovalId}" onchange="sendInputInfoToDB(this); extensionRequested(this, ${applicationId}, ${rfiOrDenialOrApprovalId})">
// 									<option value="no">No</option>
// 									<option value="yes">Yes</option>
// 								</select>
// 							</li>
// 						</div>
// 						<div class="col-lg-3 applicationColumn">
// 							<li>
// 								<label><input type="checkbox" class="documentationSubmittedCheckbox " id="rfi_documentation_submitted" data-table="rfi" data-application_id="${applicationId}" data-rfi_id="${rfiOrDenialOrApprovalId}">Documentation Submitted</label>
// 							</li>
// 							<li class="editableLi step5 ">
// 								<label>Submission Date:</label>
// 								<input class="editable date " id="rfi_documentation_submitted_date" data-table="rfi"  data-application_id="${applicationId}" data-rfi_id="${rfiOrDenialOrApprovalId}" type="date" onblur="sendInputInfoToDB(this); updateAlert(${applicationId},this,'rfi')" onkeyup="checkIfEnterKey(this, event)">
// 							</li>
// 						</div>
// 						<div class="col-lg-3 applicationColumn">
// 							<li class="editableLi step5 ">
// 								<label>Response:</label>
// 								<select name="response_select" class=" responseSelect" id="rfi_response" data-table="rfi" data-application_id="${applicationId}" data-rfi_id="${rfiOrDenialOrApprovalId}" onchange="sendInputInfoToDB(this); showDatePromptDiv(${applicationId}, this); console.log('HERE IS THIS: ', this)">
// 									<option value="not_received">Not Received</option>
// 									<option value="rfi">RFI</option>
// 									<option value="approved">Approved</option>
// 									<option value="denied">Denied</option>
// 								</select>
// 							</li>
// 						</div>
// 					</div>
// 				</ul>
// 			</section>
// 		`

// 		this.approvedRowHtml = `
// 			<section id="approval${rfiOrDenialOrApprovalId}">
// 				<button type="button" class="deleteResponseBtn" title="Delete this response" aria-label="Close" onclick="deleteResponse('approval',${rfiOrDenialOrApprovalId})">
// 	        Delete This Response
// 	      </button>
// 				<h4 class="numberOfApprovals collapsibleSection responseH4" title="Click to minimize" onclick="collapseSection(this)">Approval</h4>
// 				<ul class="collapsibleContent" id="">
// 					<div class="row">
// 					<div class="col-lg-2 applicationColumn firstColumn">
// 					<li class="editableLi">
// 							<label>Approval Notice Date:</label>
// 							 <input class="editable date" id="approval_notice_date" data-table="approval" data-approval_id="${rfiOrDenialOrApprovalId}"  type="date" onblur="sendInputInfoToDB(this)" onkeyup="checkIfEnterKey(this, event)" value="${date}">
// 						</li>
// 					</div>
// 					<div class="col-lg-3 applicationColumn">
// 						<li class="editableLi">
// 							<label>Approval Start Date:</label>
// 							 <input class="editable date" id="approval_start_date" data-table="approval" data-approval_id="${rfiOrDenialOrApprovalId}"  type="date" onblur="sendInputInfoToDB(this)" onkeyup="checkIfEnterKey(this, event)">
// 						</li>
// 						<li class="editableLi">
// 							<label>Approval End Date:</label>
// 							 <input class="editable date" id="approval_end_date" data-table="approval" data-approval_id="${rfiOrDenialOrApprovalId}"  type="date" onblur="sendInputInfoToDB(this)" onkeyup="checkIfEnterKey(this, event)">
// 						</li>
// 						<li class="editableLi">
// 							<label>Recertification Date:</label>
// 							<input class="editable date" type="date" id="approval_recertification_date" data-table="approval" data-approval_id="${rfiOrDenialOrApprovalId}" onblur="sendInputInfoToDB(this)" onkeyup="checkIfEnterKey(this, event)">
// 						</li>
// 					</div>
// 					<div class="col-lg-4 applicationColumn">
// 						<li>
// 							<label>Choose or <span class="dragNDropText">Drag n' Drop&trade;</span> Approval here:</label>
// 							<br>
// 							<input 
// 									type="file" 
// 									accept="image/jpeg,image/png,application/pdf" 
// 									onchange="
// 										uploadDoc(
// 											this, 
// 											${applicationId},
// 											'approval',
// 											${rfiOrDenialOrApprovalId},
// 											'approval'
// 										)
// 									"
// 								>
// 						</li>
// 					`
// 						// numberOfNAMIs = 1;
// 	  this.approvedRowHtml += `
// 			<div class="modal fade bd-example-modal-lg" id="namiModal${rfiOrDenialOrApprovalId}" tabindex="-1" role="dialog" aria-labelledby="namiModalTitle" aria-hidden="true">
// 			  <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
// 			    <div class="modal-content">
// 			      <div>
// 			        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
// 			          <span aria-hidden="true">&times;</span>
// 			        </button>
// 			        <h5 class="modal-title" id="exampleModalLongTitle">NAMIs</h5>
// 			      </div>
// 			     <div class="modal-body">
// 					</div>
// 	      <div class="modal-footer">
// 		      <div class="editableLi addNamiBtnLi">
// 						<button class="addModalRowBtn" onclick="addNAMIRowHTML(this, ${rfiOrDenialOrApprovalId})">Add NAMI &#x271A; </button>
// 					</div>
// 		        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
// 		      </div>
// 		    </div>
// 		  </div>
// 		</div>
// 	`

// 		this.approvedRowHtml += `
// 			<div class="modal fade bd-example-modal-lg fairHearingsModal" id="fairHearingsModal${rfiOrDenialOrApprovalId}" tabindex="-1" role="dialog" aria-labelledby="fairHearingsModalTitle" aria-hidden="true">
// 							  <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
// 							    <div class="modal-content">
// 							      <div>
// 							        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
// 							          <span aria-hidden="true">&times;</span>
// 							        </button>
// 							        <h5 class="modal-title" id="exampleModalLongTitle">Fair Hearings</h5>
// 							      </div>
// 							      <div class="modal-body">
// 										</div>
//       							<div class="modal-footer">
// 								      <div class="editableLi addNamiBtnLi">
// 												<button class="addModalRowBtn" onclick="addFairHearingRowHTML(this, ${responseId})">Add Fair Hearing &#x271A; </button>
// 											</div>
//        								<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
//      								</div>
//    								</div>
// 							  </div>
// 							</div>
// 		`

// 		this.approvedRowHtml += `
// 			</div>
// 			<div class="col-lg-3 applicationColumn">
// 				<li>
// 					<button type="button" class="btn btn-primary" data-toggle="modal" data-target="#namiModal${rfiOrDenialOrApprovalId}" id="namiModalBtn">View/Add NAMIs</button>
// 				</li>
// 				<li class="editableLi step6">
// 						<label>Satisfied with approval?</label>
// 						<select name="approval_satisfied" id="approval_satisfied" data-table="approval" data-approval_id="${rfiOrDenialOrApprovalId}" onchange="sendInputInfoToDB(this); revealNextNotSatisfiedStep(this, 1)">
// 							<option value="">Select one:</option>
// 							<option value="yes">Yes</option>
// 							<option value="no">No</option>
// 						</select>
// 					</li>
// 			</div>
// 		</div>
// 		<div class="row satisfiedRow">
// 				<div class="col-lg-4">
// 					<li class="editableLi notSatisfied notSatisfied1">
// 						<label>Contacted DSS?</label>
// 						<select name="approval_contacted_dss" id="approval_contacted_dss" data-table="approval" data-approval_id="${rfiOrDenialOrApprovalId}" onchange="sendInputInfoToDB(this);revealNextNotSatisfiedStep(this, 2)">
// 							<option value="">Select one:</option>
// 							<option value="yes">Yes</option>
// 							<option value="no">No</option>
// 						</select>
// 					</li>
// 				</div>
// 				<div class="col-lg-4">
// 					<li class="editableLi notSatisfied notSatisfied2">
// 						<label>Resolved through DSS?</label>
// 						<select name="approval_resolved_through_dss" id="approval_resolved_through_dss" data-table="approval" data-approval_id="${rfiOrDenialOrApprovalId}" onchange="sendInputInfoToDB(this);revealNextNotSatisfiedStep(this, 3)">
// 							<option value="">Select one:</option>
// 							<option value="yes">Yes</option>
// 							<option value="no">No</option>
// 						</select>
// 					</li>
// 				</div>
// 				<div class="col-lg-4">
// 				<!-- Button trigger modal -->
// 					<button type="button" class="btn btn-primary notSatisfied notSatisfied3" data-toggle="modal" data-target="#fairHearingsModal${rfiOrDenialOrApprovalId}" id="fairHearingsModalBtn">View/Add Fair Hearing Info</button>
// 			</div>

// 			<div class="modal fade bd-example-modal-lg fairHearingsModal" id="fairHearingsModal${rfiOrDenialOrApprovalId}" tabindex="-1" role="dialog" aria-labelledby="fairHearingsModalTitle" aria-hidden="true">
// 			  <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
// 			    <div class="modal-content">
// 			      <div>
// 			        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
// 			          <span aria-hidden="true">&times;</span>
// 			        </button>
// 			        <h5 class="modal-title" id="exampleModalLongTitle">Fair Hearings</h5>
// 			      </div>
// 			      <div class="modal-body">

// 							</div>
// 						<div class="modal-footer">
// 				      <div class="editableLi addNamiBtnLi">
// 								<button class="addModalRowBtn" onclick="addFairHearingRowHTML(this, ${responseId})">Add Fair Hearing &#x271A; </button>
// 							</div>
// 								<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
// 							</div>
// 						</div>
// 			  </div>
// 			</div>
// 		</div>
// 	</ul>
// </section>
// `
// 		this.deniedRowHtml = `
// 			<section id="denial${rfiOrDenialOrApprovalId}">
// 				<button type="button" class="deleteResponseBtn" title="Delete this response" aria-label="Close" onclick="deleteResponse('denial',${rfiOrDenialOrApprovalId})">
// 	        Delete This Response
// 	      </button>
// 				<h4 class="numberOfRFIs collapsibleSection responseH4" title="Click to minimize" onclick="collapseSection(this)">Denial</h4>
// 				<ul class="collapsibleContent" id="">
// 					<div class="row">
// 						<div class="col-lg-3 firstColumn applicationColumn">
// 							<li class="editableLi ">
// 								<label>Denial Notice Date:</label>
// 								<input class="editable date  due_date" id="denial_notice_date" data-table="denial"  data-application_id="${applicationId}" data-denial_id="${rfiOrDenialOrApprovalId}" type="date" onkeyup="checkIfEnterKey(this, event)"  value="${date}">
// 							</li>
							
// 						</div>
// 						<div class="col-lg-5 applicationColumn">
// 							<li>
// 							<label>Choose or <span class="dragNDropText">Drag n' Drop&trade;</span> Denial here:</label>
// 							<br>
// 								<input 
// 									type="file" 
// 									accept="image/jpeg,image/png,application/pdf" 
// 									onchange="
// 										uploadDoc(
// 											this, 
// 											${applicationId},
// 											'denial',
// 											${rfiOrDenialOrApprovalId},
// 											'denial'
// 										)
// 									"
// 								>
// 							</li>
// 							<li>
// 								<label><input type="checkbox" class="noDenialLetterReceivedCheckbox " id="no_denial_letter_received" data-table="denial" data-application_id="${applicationId}" data-denial_id="${rfiOrDenialOrApprovalId}" onchange="sendInputInfoToDB(this)">No Denial Letter Received</label>
// 							</li>
// 						</div>
// 						<div class="col-lg-4 applicationColumn">
// 							<li>
// 								<label><input type="checkbox" class="documentationSubmittedCheckbox " id="denial_documentation_submitted" data-table="denial" data-application_id="${applicationId}" data-denial_id="${rfiOrDenialOrApprovalId}">Documentation Submitted</label>
// 							</li>
// 							<li class="editableLi step5 ">
// 								<label>Submission Date:</label>
// 								<input class="editable date " id="denial_documentation_submitted_date" data-table="denial"  data-application_id="${applicationId}" data-denial_id="${rfiOrDenialOrApprovalId}" type="date" onkeyup="checkIfEnterKey(this, event)">
// 							</li>
// 						</div>
						
// 					</div>


// 					<div class="row ">
// 						<div class="col-lg-3">
// 							<li class="editableLi  ">
// 								<label>Contacted DSS?</label>
// 								<select name="denial_contacted_dss" id="denial_contacted_dss" data-table="denial" data-denial_id="${rfiOrDenialOrApprovalId}"  onchange="sendInputInfoToDB(this)">
// 									<option value="">Select one:</option>
// 									<option value="yes">Yes</option>
// 									<option value="no">No</option>
// 								</select>
// 							</li>
// 						</div>
// 						<div class="col-lg-3">
// 							<li class="editableLi  ">
// 								<label>Resolved through DSS?</label>
// 								<select name="denial_resolved_through_dss" id="denial_resolved_through_dss" data-table="denial" data-denial_id="${rfiOrDenialOrApprovalId}"  onchange="sendInputInfoToDB(this); generateApproval(this, ${applicationId})">
// 									<option value="">Select one:</option>
// 									<option value="yes">Yes</option>
// 									<option value="no">No</option>
// 								</select>
// 							</li>
// 						</div>
// 						<div class="col-lg-3">
// 							<!-- Button trigger modal -->
// 								<button type="button" class="btn btn-primary  " data-toggle="modal" data-target="#fairHearingsModal${rfiOrDenialOrApprovalId}" id="fairHearingsModalBtn">View/Add Fair Hearing Info</button>
// 						</div>

// 							<div class="modal fade bd-example-modal-lg fairHearingsModal" id="fairHearingsModal${rfiOrDenialOrApprovalId}" tabindex="-1" role="dialog" aria-labelledby="fairHearingsModalTitle" aria-hidden="true">
// 							  <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
// 							    <div class="modal-content">
// 							      <div>
// 							        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
// 							          <span aria-hidden="true">&times;</span>
// 							        </button>
// 							        <h5 class="modal-title" id="exampleModalLongTitle">Fair Hearings</h5>
// 							      </div>
// 							      <div class="modal-body">
										
//      								</div>
//       							<div class="modal-footer">
// 								      <div class="editableLi addNamiBtnLi">
// 												<button class="addModalRowBtn" onclick="addFairHearingRowHTML(this, ${responseId})">Add Fair Hearing &#x271A; </button>
// 											</div>
//        								<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
//      								</div>
//    								</div>
// 							  </div>
// 							</div>
// 							<div class="col-lg-3">
// 							<li>
// 								<button type="button" class="btn btn-primary" id="createNewApp" onclick="createNewApp()">Create New Application</button>
// 							</li>
// 						</div>
							
// 					</div>

// 				</ul>
// 			</section>
// 		`
// 	}
// }

const addNAMIRowHTML = (addNamiBtn, approvalId) => {
	const ajaxCall = $.ajax(
		{
			type:"GET",
			url: `/application/ajax/create_nami`,
			data: {
				approval_id: approvalId
			},
			success: function(namiId) {
				const html = `
					<div class="modalRowDiv">
						<button type="button" class="close" onclick="removeModalRow(this, ${namiId},'nami')">
		          <span >&times;</span>
		        </button>
						<h6 class="namiH6">NAMI:</h6>
						<div class="modalRow">
							<div class="col-lg-4 col-sm-12 modalRowColumn">
							<label>NAMI Start Date:</label>
								<input class="editable date" id="nami_start_date" data-table="nami" data-nami_id="${namiId}" type="date" onblur="sendInputInfoToDB(this)" onkeyup="checkIfEnterKey(this, event)">
							</div>
							<div class="col-lg-4 col-sm-12 modalRowColumn">
							<label>NAMI End Date:</label>

								<input class="editable date" id="nami_end_date" data-table="nami" data-nami_id="${namiId}" type="date" onblur="sendInputInfoToDB(this)" onkeyup="checkIfEnterKey(this, event)">
							</div>
							<div class="col-lg-4 col-sm-12 modalRowColumn">
							<label>Amount:</label>
								$<input type="number" class="editable" id="nami_amount" data-table="nami" data-nami_id="${namiId}" onblur="sendInputInfoToDB(this)" onkeyup="checkIfEnterKey(this, event)">
							</div>
						</div>
					</div>
				`
				const modalBody = addNamiBtn.parentNode.parentNode.parentNode.querySelector('.modal-body');
				modalBody.insertAdjacentHTML('beforeend', html)
				// numberOfNAMIs += 1;
			}
		});
}

const addDSSLogEntryRowHTML = (addDSSLogEntryBtn, applicationId) => {
	const ajaxCall = $.ajax(
		{
			type:"GET",
			url: `/application/ajax/create_dss_contact_log_entry`,
			data: {
				application_id: applicationId
			},
			success: function(entryId) {
				const html = `
					<div class="modalRowDiv">
						<button type="button" class="close" onclick="removeModalRow(this, ${entryId}, 'dss_contact_log_entry')">
		          <span >&times;</span>
		        </button>
						<h6 class="fairHearingH6">Log Entry</h6>
						<div class="row modalRow">
							<div class="col-lg-6 col-md-6 col-sm-12 modalRowColumn">
								<li>
									<label>Contact Person:</label>
									<input type="text" class="editable" id="entry_contact_person" data-table="dss_contact_log_entry" data-dss_contact_log_entry_id="${entryId}" onblur="sendInputInfoToDB(this)" onkeyup="checkIfEnterKey(this, event)">
								</li>
								<li>
									<label>Date:</label>
									<input class="editable date" id="entry_date" data-table="dss_contact_log_entry" data-dss_contact_log_entry_id="${entryId}" type="date" onblur="sendInputInfoToDB(this)" onkeyup="checkIfEnterKey(this, event)">
								</li>
								<li>
									<label>Time:</label>
									<input class="editable time" id="entry_time" data-table="dss_contact_log_entry" data-dss_contact_log_entry_id="${entryId}" type="time" onblur="sendInputInfoToDB(this)" onkeyup="checkIfEnterKey(this, event)">
								</li>					
							</div>
							<div class="col-lg-6 col-md-6 col-sm-12 modalRowColumn">		
								<li>
									<label style="display: block;">Notes:</label>
									<textarea type="text" class="editable notes" id="entry_notes" data-table="dss_contact_log_entry" data-dss_contact_log_entry_id="${entryId}" onblur="sendInputInfoToDB(this)" onkeyup="checkIfEnterKey(this, event)"></textarea>
								</li>
							</div>
						</div>
					</div>
				`
				const modalBody = addDSSLogEntryBtn.parentNode.parentNode.parentNode.querySelector('.modal-body');
				modalBody.insertAdjacentHTML('beforeend', html)
			}
		});
}

const addFairHearingRowHTML = (addFairHearingBtn, responseId) => {
	const ajaxCall = $.ajax(
		{
			type:"GET",
			url: `/application/ajax/create_fair_hearing`,
			data: {
				response_id: responseId
			},
			success: function(fairHearingId) {
				const html = `
								<div class="modalRowDiv">
									<button type="button" class="close" onclick="removeModalRow(this, ${fairHearingId}, 'fair_hearing')">
					          <span >&times;</span>
					        </button>
									<h6 class="fairHearingH6">Fair Hearing</h6>
									<div class="row modalRow">
										<div class="col-lg-4 col-md-6 col-sm-12 modalRowColumn">
											<li>
												<label>Date:</label>
												<input class="editable date" id="fair_hearing_date" data-table="fair_hearing" data-fair_hearing_id="${fairHearingId}" type="date" onblur="sendInputInfoToDB(this)" onkeyup="checkIfEnterKey(this, event)">
											</li>
											<li>
												<label>Time:</label>
												<input class="editable time" id="fair_hearing_time" data-table="fair_hearing" data-fair_hearing_id="${fairHearingId}" type="time" onblur="sendInputInfoToDB(this)" onkeyup="checkIfEnterKey(this, event)">
											</li>
										</div>
										<div class="col-lg-4 col-md-6 col-sm-12 modalRowColumn">
											<li>
												<label>Address:</label>
												<input type="text" class="editable" id="fair_hearing_address" data-table="fair_hearing" data-fair_hearing_id="${fairHearingId}" onblur="sendInputInfoToDB(this)" onkeyup="checkIfEnterKey(this, event)">
											</li>
											<li>
												<label>Outcome:</label>
												<input type="text" class="editable" id="fair_hearing_outcome" data-table="fair_hearing" data-fair_hearing_id="${fairHearingId}" onblur="sendInputInfoToDB(this)" onkeyup="checkIfEnterKey(this, event)">
											</li>
										</div>
										<div class="col-lg-4 col-md-6 col-sm-12 modalRowColumn">
											<li>
												<label>Facility Representative:</label>
												<select id="fair_hearing_representative_type" data-table="fair_hearing" data-fair_hearing_id="${fairHearingId}" onchange="sendInputInfoToDB(this)">
													<option value="">Select one:</option>
													<option value="regional_coordinator">Regional Coordinator</option>
													<option value="facility_coordinator">Facility Coordinator</option>
													<option value="attorney">Attorney</option>
												</select>
											</li>
											<li>
												<label>Representative's Name:</label>
												<input type="text" class="editable" id="fair_hearing_representative_name" data-table="fair_hearing" data-fair_hearing_id="${fairHearingId}"  onblur="sendInputInfoToDB(this)" onkeyup="checkIfEnterKey(this, event)">
											</li>
										</div>
										<div class="col-lg-6 col-sm-12 modalRowColumn">
											<li>
												<label>Choose or <span class="dragNDropText">Drag n' Drop&trade;</span> Fair Hearing Notice here:</label>
												<br>
												<input 
													type="file" 
													accept="image/jpeg,image/png,application/pdf" 
													onchange="
														uploadDoc(
															this, 
															${responseId},
															'fair_hearing',
															${fairHearingId},
															'fair_hearing_confirmation'
														)
													"
												>
											</li>
										</div>
										<div class="col-lg-6 col-sm-12 modalRowColumn">
											<li>
												<label>Choose or <span class="dragNDropText">Drag n' Drop&trade;</span> Fair Hearing Decision here:</label>
												<br>
												<input 
													type="file" 
													accept="image/jpeg,image/png,application/pdf" 
													onchange="
														uploadDoc(
															this, 
															${responseId},
															'fair_hearing',
															${fairHearingId},
															'fair_hearing_outcome_document'
														)
													"
												>
											</li>
										</div>
									</div>
								</div>
				`
				const modalBody = addFairHearingBtn.parentNode.parentNode.parentNode.querySelector('.modal-body');
				modalBody.insertAdjacentHTML('beforeend', html)
				// numberOfFairHearings += 1;
			}
		});
}

const removeModalRow = (removeModalRowBtn, modalRowId, rowType) => {
	if(confirm("Delete this row?")) {
		const ajaxCall = $.ajax(
			{
				type:"GET",
				url: `/application/ajax/delete_${rowType}`,
				data: {
				row_id: modalRowId
			},
			success: function() {
				console.log("Row deleted");
				const modalRow = removeModalRowBtn.parentNode;
				$(modalRow).fadeOut();
			}
		});
	}
}

const extensionRequested = (extensionRequestedField,applicationId,rfiId) => {
	const col = extensionRequestedField.parentNode.parentNode;
	const html = `
	<li class="editableLi">
		<label>Extension Granted?</label>
		<select name="rfi_extension_response" id="rfi_extension_response" data-table="rfi" data-application_id="${applicationId}" data-rfi_id="${rfiId}" onchange="sendInputInfoToDB(this); newRfiDueDatePrompt(this)">
			<option value="no">No</option>
			<option value="yes">Yes</option>
		</select>
	</li>
	`
	col.insertAdjacentHTML("beforeend", html);
}

const newRfiDueDatePrompt = selectField => {
	if (selectField.value == "yes") {
		alert("Please enter a new RFI Due Date");
 		const dueDateField = selectField.parentNode.parentNode.querySelector('#rfi_due_date');
  	dueDateField.focus();
	}
}

const showDatePromptDiv = (appId, responseField) => {
	const datePromptDiv = document.querySelector('#datePromptDiv');
	const responseType = responseField.value
	datePromptDiv.querySelector('.appId').value = appId
	datePromptDiv.querySelector('.responseType').value = responseType
	const responseTypeSpan = datePromptDiv.querySelector('#responseType')
	const input = datePromptDiv.querySelector('INPUT')
	if (responseType != 'not_received') {
		if (responseType == 'rfi') {
			responseTypeSpan.innerHTML = 'RFI Due'
		} else if (responseType == 'denied') {
			responseTypeSpan.innerHTML = 'Denial Notice'
		} else if (responseType == 'approved') {
			responseTypeSpan.innerHTML = 'Approval Notice'
		}
		datePromptDiv.style.display = 'initial'
	}
	input.focus()
}


let numberOfRFIs = 0;

const createResponseRow = (dateInput) => {
	const date = dateInput.value
	const applicationId = dateInput.parentNode.querySelector('.appId').value
	const responseType = dateInput.parentNode.querySelector('.responseType').value
	dateInput.value = ''
	datePromptDiv.style.display = 'none'
	if(date) {
		const ajaxCall = $.ajax(
			{
				type:"GET",
				url: `/application/ajax/create_response`,
				data: {
					application_id: applicationId,
					response_type: responseType,
					date: date
				},
				success: function(idArray) {
					if (idArray != 'no response created for not_received') {
						// const responseId = idArray[0]
						// rfiOrDenialOrApprovalId = idArray[1]
						// newResponseRowHTML = new ResponseRowHTML(applicationId, responseId, rfiOrDenialOrApprovalId, date)
						// const applicationDiv = document.querySelector(`#application${applicationId}`)
						// applicationDiv.insertAdjacentHTML("beforeend", newResponseRowHTML[`${responseType}RowHtml`]);
						const responseField = {
							appId: applicationId
						}
						if (responseType == "rfi") {
							phaseChange(responseField, 5);
							numberOfRFIs += 1;
						} else if (responseType == 'approved'){
							phaseChange(responseField, 6);
						} else if (responseType == 'denied'){
							phaseChange(responseField, 12);
						};
						location.reload()
					}
				}
			});
		
	}
}

const checkIfEnterKey = (input,event) => {
	if (event.keyCode == 13) {
		input.blur();
	}
}

const revealNextNotSatisfiedStep = (selectField, stepToReveal) => {
	if(selectField.id != 'approval_contacted_dss') {
		if (selectField.value == "no") {
			const ul = selectField.parentNode.parentNode.parentNode.parentNode;
			const element = ul.querySelector(`.notSatisfied${stepToReveal}`)
			$(element).fadeIn();
		} else if (selectField.value == "yes") {
			document.querySelector('.overlay').style.display = "block";
		};
	} else {
		if (selectField.value == "yes") {
			const ul = selectField.parentNode.parentNode.parentNode.parentNode;
			const element = ul.querySelector(`.notSatisfied${stepToReveal}`)
			$(element).fadeIn();
		}
	}
}

const createNewApp = thisAppId => {
	const ajaxCall = $.ajax(
		{
			type:"GET",
			url: `/application/ajax/create_application`,
			data: {
				resident_id: residentId
			},
			success: function(newAppId) {
				location.reload();

			}
		});
}

const rotateArrow = refreshBtn => {
	$(refreshBtn).addClass('rotateZ')
}
	
const deleteDoc = (deleteBtn, appId, docId, table, tableRowId, docFieldToEmptyOnDelete) => {
	if (confirm("Remove this document?")) {
		const successMessage = `${docFieldToEmptyOnDelete} field in ${table} table set to null`;
		const dataObject =  {
			document_id: docId,
			row_id: tableRowId,
			column: docFieldToEmptyOnDelete,
			new_value: null
		}
		updateDB(table, dataObject, successMessage)
		if (docFieldToEmptyOnDelete == 'application_document') {
			docFieldToEmptyOnDelete = 'medicaid_application'
		}
		// if it's a misc doc:
		if (table == 'document' && docFieldToEmptyOnDelete == 'application_id') {
			const row = deleteBtn.parentNode.parentNode;
			$(row).fadeOut()
		} else {
			const html = `
			<input type="file" accept="image/jpeg,image/png,application/pdf" onchange="uploadDoc(this, ${appId}, '${table}', ${tableRowId}, '${docFieldToEmptyOnDelete}')">
			`
			$(deleteBtn).prev().remove()
			$(deleteBtn).replaceWith(html);
		}		
	}
}

const deleteResponse = (responseType,responseId) => {
	if (confirm("Delete this response and all its data?")) {
		const ajaxCall = $.ajax(
		{
			type:"GET",
			url: `/application/ajax/delete_response`,
			data: {
				response_type: responseType,
				response_id: responseId
			},
			success: function() {
				const section = document.querySelector(`#${responseType}${responseId}`)
				$(section).fadeOut()
				location.reload()
			}
		});
	}
}

const generateApproval = (select, appId) => {
	if(select.value == "yes") {
		const responseField = {
			value: "approved",
			appId: appId
		}
		showDatePromptDiv(appId, responseField)
	}
}

const showSection = sectionLink => {
	const sectionType = sectionLink.getAttribute('data-section_type')
	const sectionIdNumber = sectionLink.getAttribute('data-section_id_number')
	const sectionId = sectionType + sectionIdNumber
	const activeSection = document.querySelector(`#${sectionId}`)
	const sections = document.querySelectorAll('SECTION');
	const sectionLinks = document.querySelectorAll('.sectionLink');
	for (var section of sections) {
		section.style.display = 'none'
	}
	for (var link of sectionLinks) {
		link.style.backgroundColor = 'none'
	}
	activeSection.style.display = 'block';
	for (var link of sectionLinks) {
		link.classList.remove('activeTab')
	}
	sectionLink.classList.add('activeTab')
}

const refreshResidentInfo = (refreshBtn, residentId, appId) => {
	const ajaxCall = $.ajax(
		{
			type:"GET",
			// url: `/application/ajax/refresh/demographics/?resident_id=10014003&application_id=88`,
			url: `/application/ajax/refresh/demographics/`,
			data: {
				resident_id: residentId,
				application_id: appId
			},
			success: function(residentInfoArray) {
				const section = refreshBtn.parentNode.parentNode.parentNode
				section.querySelector('#resident_name').innerHTML = `${residentInfoArray[0]} ${residentInfoArray[1]}`
				section.querySelector('#resident_dob').innerHTML = new Date(Date.parse(residentInfoArray[2])).toLocaleDateString()
				section.querySelector('#resident_address').innerHTML = residentInfoArray[3]
				section.querySelector('#resident_city').innerHTML = residentInfoArray[4]
				section.querySelector('#resident_state').innerHTML = residentInfoArray[5]
				section.querySelector('#resident_zip').innerHTML = residentInfoArray[6]
				section.querySelector('#resident_phone').innerHTML = residentInfoArray[7]
				section.querySelector('#resident_marital_status').innerHTML = residentInfoArray[8]

				refreshBtn.classList.remove('rotateZ')
				// sectionToShow = document.querySelector('#residentSectionTab')
				// location.reload();

			}
		});	
}

$("#mostRecentAppTab li:last-of-type").click();
document.getElementById("olderAppsTabsDiv").lastElementChild.style.display = "none";

const toggleOlderApps = link => {
	link.classList.toggle('minusSignAfter');
	const div = document.getElementById('olderAppsTabsDiv')
	if (div.style.display != "block") {
		div.style.display = "block"
	} else {
		div.style.display = "none"
	}
}
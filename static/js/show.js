//Toggle fields in and out of editable state on show pages
const editBtn = document.querySelector("#editBtn");
editBtn.addEventListener('click', (e) => {	
	const editableItems = document.querySelectorAll('.editable');
	if (editBtn.textContent == 'Edit') {
			for (var i = 0; i < editableItems.length; i++) {
			const	editableItem = editableItems[i]
			const input = document.createElement('input');
			input.type = 'text';
			input.value = editableItem.textContent;
			input.className = 'editable';
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

// jQuery AJAX request to track or ignore residents, then remove resident's row from view upon success
const trackOrIgnore = (row, trueOrFalse) => {
	const ajaxCall = $.ajax(
	{
		type:"GET",
		url: "/application/ajax/track_or_ignore",
		data:{
			patient_id: row.id,
			tracking: trueOrFalse
		},
		success: function() 
		{
			const table = row.parentNode;
			$(row).remove();
			// $(row).fadeOut(30);
			showTableCount(table);
			showTotalActivityCount();
		}
	});
	return(ajaxCall);
}
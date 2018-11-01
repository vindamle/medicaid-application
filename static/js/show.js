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
			editableItem.parentNode.insertBefore(input, editableItem);
			editableItem.parentNode.removeChild(editableItem);
			editBtn.textContent = 'Save';
		};
	} else if (editBtn.textContent == 'Save') {
			for (var i = 0; i < editableItems.length; i++) {
			const editableItem = editableItems[i]
			const span = document.createElement('span');
			span.textContent = editableItem.value;
			span.className = 'editable';
			editableItem.parentNode.insertBefore(span, editableItem);
			editableItem.parentNode.removeChild(editableItem);
			editBtn.textContent = 'Edit';
		};
	};
});

//close bootstrap alert
// const alert = document.querySelector('.alert');
// const closeBtn = alert.querySelector('.close');

// closeBtn.addEventListener('click', () => {
// 	alert.parentNode.removeChild(alert);
// });
// 'Remove' button demo functionality (doesn't affect database yet)
const trackedResidentsTable = document.querySelector('#trackedResidentsTable');
trackedResidentsTable.addEventListener('click', (e) => {
	if (e.target.className == 'btn-remove') {
		if (confirm("Are you sure you want to stop tracking this resident?")) {
			const row = e.target.parentNode.parentNode;
			const rowParent = row.parentNode;
			rowParent.removeChild(row);
		};
	};
});

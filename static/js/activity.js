
const trackSelectedBtn = document.getElementById('trackSelectedBtn');

document.addEventListener('click', (e) => {
//change row color when clicking/unclicking 'Track' button
	if (e.target.parentNode.classList.contains('trackBtnCell')) {
		const button = e.target;
		if (e.target.textContent == 'Track') {
			e.target.textContent = '\u2713';
			button.className = 'btn-tracked';
		} else {
			e.target.textContent = 'Track';
			button.className = 'btn-track';
		};
// 'Ignore' button removes row - demo functionality (doesn't affect database yet)
	} else if (e.target.className == 'btn-ignore') {
		if (confirm("Are you sure you want ignore this alert?")) {
			const row = e.target.parentNode.parentNode;
			const rowParent = row.parentNode;
			rowParent.removeChild(row);
		};
// 'Track Selected' button removes all tracked rows - demo functionality (doesn't affect database yet)
	} else if (e.target == trackSelectedBtn) {
		const tracked = document.querySelectorAll('.btn-tracked');
		console.log(tracked);
		for (var i = 0; i < tracked.length; i++) {
			const row = tracked[i].parentNode.parentNode;
			console.log(row);
			row.parentNode.removeChild(row);
		};
	};
});
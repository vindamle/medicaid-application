$('.verifyBtn').click((e) => {
	const btn = e.target;
	$(btn).toggleClass('verified');
	if (btn.innerHTML == "Not Verified") {
		btn.innerHTML = "Verified &check;";
	} else {
		btn.innerHTML = "Not Verified";
	}
})


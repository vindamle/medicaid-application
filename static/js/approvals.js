const verifyOrUnverify = (row, trueOrFalse) => {
	const ajaxCall = $.ajax(
	{
		type:"GET",
		url: "/application/ajax/approval_verified",
		data:{
			resident_id: row.id,
			approval_verified: trueOrFalse
		},
		success: function() 
		{
			console.log("approval set to " + trueOrFalse)
		}
	});
	return(ajaxCall);
}

$('.verifyBtn').click((e) => {
	const btn = e.target;
	const row = btn.parentNode.parentNode;
	$(btn).toggleClass('verified');
	if (btn.innerHTML == "Not Verified") {
		verifyOrUnverify(row, "true")
		btn.innerHTML = "Verified &check;";
	} else {
		verifyOrUnverify(row, "false")
		btn.innerHTML = "Not Verified";
	}
})


  
// $('.btn-track').click(function(){
//     const row = this.parentNode.parentNode;
//     trackOrIgnore(row, true);
// });

// $('.btn-ignore').click(function(){
//   button = this;
//   // console.log(button);
//   if (confirm("Are you sure you want stop tracking this resident?")) {
//     const row = this.parentNode.parentNode;
//     trackOrIgnore(row, false);
//    };
// });
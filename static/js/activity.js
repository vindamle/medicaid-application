  const newAdmissionsTable = document.getElementById('newAdmissionsTable');
  const payorChangesTable = document.getElementById('payorChangesTable');
  const dischargesTable = document.getElementById('dischargesTable');

  const showTableCount = (table) => {
    const countSpanId = table.id + "Count";
    const countSpan = document.getElementById(countSpanId);
    const count =table.children.length;
    countSpan.innerHTML = count;
  };

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
            showTableCount(table);
        }
     });
    return(ajaxCall);
  }

  showTableCount(newAdmissionsTable);
  showTableCount(payorChangesTable);
  showTableCount(dischargesTable);

// jQuery AJAX request to track or ignore residents, then remove resident's row from view upon success
$('.btn-track').click(function(){
    const row = this.parentNode.parentNode;
    trackOrIgnore(row, true);
});

$('.btn-ignore').click(function(){
  button = this;
  // console.log(button);
  if (confirm("Are you sure you want ignore this alert?")) {
    const row = this.parentNode.parentNode;
    trackOrIgnore(row, false);
   };
});
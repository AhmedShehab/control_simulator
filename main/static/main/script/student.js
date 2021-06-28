function openReqForm(x) {
	document.getElementsByClassName(x)[0].style.display = "flex";
}
function closeReqForm(x) {
	document.getElementsByClassName(x)[0].style.display = "none";
}
function tableSelect() {
	var status = document.getElementById("status").value;
	var pendingTable = document.getElementById("pendingTable");
	var submittedTable = document.getElementById("submittedTable");
	if (status === "submitted") {
		submittedTable.style.display = "block";
		pendingTable.style.display = "none";
	} else {
		submittedTable.style.display = "none";
		pendingTable.style.display = "block";
	}
}

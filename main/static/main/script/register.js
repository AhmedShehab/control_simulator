function openStudentForm() {
	document.getElementById("studentForm").style.display = "flex";
	document.getElementById("studForm").style.display = "none";
	document.getElementById("instForm").style.display = "none";
}

function closeRegisterForm() {
	location.reload();
}

function openInstructorForm() {
	status = "i";
	document.getElementById("instructorForm").style.display = "flex";
	document.getElementById("studForm").style.display = "none";
	document.getElementById("instForm").style.display = "none";
}

if (document.getElementById("instMSG")) {
	openInstructorForm();
}
if (document.getElementById("studMSG")) {
	openStudentForm();
}

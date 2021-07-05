function openAssignmentForm() {
	document.getElementById("assignmentForm").style.display = "flex";
}
function closeAssignmentForm() {
	document.getElementById("assignmentForm").style.display = "none";
}
function openCourseForm() {
	document.getElementById("courseForm").style.display = "flex";
}
function closeCourseForm() {
	document.getElementById("courseForm").style.display = "none";
}
function openCourseCodeForm() {
	document.getElementById("courseCodeForm").style.display = "flex";
}
function closeCourseCodeForm() {
	document.getElementById("courseCodeForm").style.display = "none";
}
function courseSelector(courses) {
	var table = document.getElementsByClassName("tr");
	for (let i = 0; i < table.length; i++) {
		document.getElementById(table[i].id).style.display = "none ";
	}
	var select = (document.getElementById("assignmentSelect").value = "Select an Assignment");
	var course = document.getElementById("courseSelect").value;
	var assignments = document.getElementsByClassName(course);
	for (let i = 0; i < courses.length; i++) {
		var assignments = document.getElementsByClassName(courses[i]);
		if (courses[i] == course) {
			for (let i = 0; i < assignments.length; i++) {
				assignments[i].style.display = "block";
			}
		} else {
			for (let i = 0; i < assignments.length; i++) {
				assignments[i].style.display = "none";
			}
		}
	}
}
function assignmentsSubmitted() {
	var course = document.getElementById("courseSelect").value;
	var assignments = document.getElementById("assignmentSelect").value;
	var s = course + ":" + assignments;
	var table = document.getElementsByClassName("tr");
	for (let i = 0; i < table.length; i++) {
		if (table[i].id == s) {
			document.getElementById(table[i].id).style.display = "table-row ";
		} else {
			document.getElementById(table[i].id).style.display = "none";
		}
	}
}
function gradeSelect() {
	var grade = document.getElementById("grade").value;
	if (grade == "auto") {
		document.getElementById("grade2").style.display = "block";
		document.getElementById("grade3").style.display = "none";
		document.getElementById("rise").required = true;
		document.getElementById("settle").required = true;
		document.getElementById("overshoot").required = true;
		document.getElementById("error").required = true;
		document.getElementById("grade3").required = false;
	}
	if (grade == "receive") {
		document.getElementById("grade2").style.display = "none";
		document.getElementById("grade3").style.display = "block";
		document.getElementById("rise").required = false;
		document.getElementById("settle").required = false;
		document.getElementById("overshoot").required = false;
		document.getElementById("error").required = false;
		document.getElementById("grade3").required = true;
	}
}

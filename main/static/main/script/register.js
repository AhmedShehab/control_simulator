function openStudentForm(){
    document.getElementById("studentForm").style.display = "block";
    document.getElementById("studForm").style.display = "none";
    document.getElementById("instForm").style.display = "none";
}

/* function closeStudentForm(){
    document.getElementById("studentForm").style.display = "none";
    document.getElementById("studInstForm").style.display = "block";
} */
function openInstructorForm(){
    status = "i";
    document.getElementById("instructorForm").style.display = "block";
    document.getElementById("studForm").style.display = "none";
    document.getElementById("instForm").style.display = "none";
}
/* 
function closeInstructorForm(){
    document.getElementById("instructorForm").style.display = "none";
} */
if (document.getElementById("instMSG")){
        openInstructorForm();
}
if (document.getElementById("studMSG")) {
    openStudentForm();
}

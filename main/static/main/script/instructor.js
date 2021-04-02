function openAssignmentForm(){
    document.getElementById("assignmentForm").style.display = "block";
    window.scroll(0,92);
}
function closeAssignmentForm(){
    document.getElementById("assignmentForm").style.display = "none";
}
function openCourseForm(){
    document.getElementById("courseForm").style.display = "block";
    window.scroll(0,92);
}
function closeCourseForm(){
    document.getElementById("courseForm").style.display = "none";
}
function courseSelector(courses){
var table = document.getElementsByClassName("tr");
for (let i = 0; i < table.length; i++) {
        document.getElementById(table[i].id).style.display="none "
}
var select= document.getElementById("assignmentSelect").value="Select an Assignment"
var course = document.getElementById("courseSelect").value;
var assignments= document.getElementsByClassName(course);
for (let i = 0; i < courses.length; i++) {
    var assignments= document.getElementsByClassName(courses[i]);
    if (courses[i]==course) {
        for (let i = 0; i < assignments.length; i++) {
            assignments[i].style.display="block"
        }
    }
    else{
        for (let i = 0; i < assignments.length; i++) {
            assignments[i].style.display="none"
        }
    }   
    }
}
function assignmentsSubmitted(){
    var course = document.getElementById("courseSelect").value;
    var assignments= document.getElementById("assignmentSelect").value;
    var s = course+":"+assignments;
    var table = document.getElementsByClassName("tr");
    for (let i = 0; i < table.length; i++) {
        if(table[i].id==s){
            document.getElementById(table[i].id).style.display="table-row "
        }
        else{
            document.getElementById(table[i].id).style.display="none"
        }
    }
}



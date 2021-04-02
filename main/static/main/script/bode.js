
window.onload = function () {
var omega = document.getElementById("omega").value;

console.log(limit);

var mag = document.getElementById("mag").value;
var ph = document.getElementById("ph").value;

omega = omega.match(/-?\d+(?:\.\d+)?/g).map(Number);
ph = ph.match(/-?\d+(?:\.\d+)?/g).map(Number);
mag = mag.match(/-?\d+(?:\.\d+)?/g).map(Number);
var limit = omega.length;
// console.log(omega[0], omega[1],omega[2],omega[998],omega[999]);
// console.log(ph[0], ph[1],ph[2],ph[998],ph[999]);
// console.log(mag[0], mag[1],mag[2],mag[998],mag[999]);

var data = [];
var dataSeries = { type: "line" };
var dataPoints = [];
for (var i = 0; i < limit; i += 1) {
    
    dataPoints.push({
        x: omega[i],
        y: mag[i]
    });
}
dataSeries.dataPoints = dataPoints;
data.push(dataSeries);


var data2 = [];
var dataSeries = { type: "line" };
var dataPoints = [];
for (var i = 0; i < limit; i += 1) {
    
    dataPoints.push({
        x: omega[i],
        y: ph[i]
    });
}
dataSeries.dataPoints = dataPoints;
data2.push(dataSeries);
var m = {
    zoomEnabled: true,
    animationEnabled: true,
    theme: "light",
    title: {
        text: "Bode Diagram"
    },
    axisX:{
        logarithmic: true,
        title: "Frequency (Log)",
        gridThickness: 1
        
    },
    axisY: {
        lineThickness: 1,
        title: "Magnitude dB",
        
    },
    data: data
    
    
};
var p = {
    zoomEnabled: true,
    animationEnabled: true,
    theme: "light",
    pointStyle:'dash',
    title: {
    },
    axisX:{
        logarithmic: true,
        title: "Frequency (Log)",
        gridThickness: 1
        
    },
    axisY: {
        lineThickness: 1,
        title: "Phase",
        
    },
    data: data2  
    
};

var chartM = new CanvasJS.Chart("Magnitude", m);
chartM.render();
var chartP = new CanvasJS.Chart("Phase", p);
chartP.render();
}

function display(){
    var elements = document.getElementsByClassName("no");
    for (var i=0; i<elements.length; i++) {
        elements[i].style.display = 'none';
    }
    var name= document.getElementById("selector").value;
    document.getElementById(name).style.display ="block";
    
}
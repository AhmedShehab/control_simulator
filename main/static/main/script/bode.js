window.onload = function () {
    var omega = document.getElementById("omega").value;
    var mag = document.getElementById("mag").value;
    var ph = document.getElementById("ph").value;
    omega = omega.match(/-?\d+(?:\.\d+)?/g).map(Number);
    ph = ph.match(/-?\d+(?:\.\d+)?/g).map(Number);
    mag = mag.match(/-?\d+(?:\.\d+)?/g).map(Number);
    var limit = omega.length;


    var omega_comp = document.getElementById("omega_comp");
    var mag_comp = document.getElementById("mag_comp");
    var ph_comp = document.getElementById("ph_comp");
    var Mag, Ph;
    var magnitude = [];
    var phase = [];
    var dataSeries = { type: "line" };
    var dataPoints = [];
    for (var i = 0; i < limit; i += 1) {
        
        dataPoints.push({
            x: omega[i],
            y: mag[i]
        });
    }
    dataSeries.dataPoints = dataPoints;
    magnitude.push(dataSeries);
    var dataSeries = { type: "line" };
    var dataPoints = [];
    for (var i = 0; i < limit; i += 1) {
        
        dataPoints.push({
            x: omega[i],
            y: ph[i]
        });
    }
    dataSeries.dataPoints = dataPoints;
    phase.push(dataSeries);


    Mag = {
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
        data: magnitude
        
        
    };
    Ph = {
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
        data: phase
        
    };


    if (omega_comp != null){
        console.log("Nooooo!")
        console.log(magnitude)
        omega_comp = omega_comp.value;
        mag_comp = mag_comp.value;
        ph_comp = ph_comp.value;
        omega_comp = omega_comp.match(/-?\d+(?:\.\d+)?/g).map(Number);
        ph_comp = ph_comp.match(/-?\d+(?:\.\d+)?/g).map(Number);
        mag_comp = mag_comp.match(/-?\d+(?:\.\d+)?/g).map(Number);
        var limit_comp = omega_comp.length;
        var magnitude_comp = [];
        var phase_comp = [];
        var dataSeries = { type: "line" };
        var dataPoints = [];
        for (var i = 0; i < limit_comp; i += 1) {
            
            dataPoints.push({
                x: omega_comp[i],
                y: mag_comp[i]
            });
        }
        dataSeries.dataPoints = dataPoints;
        magnitude_comp.push(dataSeries);
        var dataSeries = { type: "line" };
        var dataPoints = [];
        for (var i = 0; i < limit_comp; i += 1) {
            
            dataPoints.push({
                x: omega_comp[i],
                y: ph_comp[i]
            });
        }
        dataSeries.dataPoints = dataPoints;
        phase_comp.push(dataSeries);
        
        Mag = {
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
            axisY2:{
                lineThickness: 1,
                title: "Magnitude comp",
                
            },
            data: [{magnitude},{magnitude_comp}]
        };
        Ph = {
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
            axisY2: {
                title: "Phase_comp",
                lineThickness: 1
            },
            data: phase
            
        };
        
    }
        var chartPP = new CanvasJS.Chart("Phase", Ph);
        chartPP.render();
        var chartMM = new CanvasJS.Chart("Magnitude", Mag);
        chartMM.render();
    
    }
    
    function display(){
        var elements = document.getElementsByClassName("no");
        for (var i=0; i<elements.length; i++) {
            elements[i].style.display = 'none';
        }
        var name= document.getElementById("selector").value;
        document.getElementById(name).style.display ="block";
        
    }
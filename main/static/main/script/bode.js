window.onload = function () {
	var name = document.getElementById("selector2").value;
	var elements = document.getElementsByClassName("option");
	for (let i = 0; i < elements.length; i++) {
		var element = elements[i];
		if (element.id == name) {
			document.getElementById(name).style.display = "block";
		} else {
			element.style.display = "none";
		}
	}
	var omega = document.getElementById("omega").value;
	var mag = document.getElementById("mag").value;
	var ph = document.getElementById("ph").value;
	var pm = document.getElementById("pm").value;
	var gm = document.getElementById("gm").value;
	var wp = document.getElementById("wp").value;
	console.log("pmmmm"+ pm)
	console.log(typeof(pm))
	// if (parseFloat(pm) != NaN) {
	// 	pm = parseFloat(pm).toFixed(3);
	// }
	console.log(pm)
	var p = parseFloat(pm);
	var w = parseFloat(wp);
	console.log(p)
	if (!isNaN(w)) {
		wp = parseFloat(parseFloat(wp).toFixed(3));
		wp = "(at "+wp+"rad/s)"
	}
	else{
		wp = "";
	}
	console.log("sooof"+ wp)
	if (!isNaN(p)) {
		pm = parseFloat(parseFloat(pm).toFixed(3));
	}
	else{
		pm = "inf";
	}
	var g = parseFloat(gm);
	if (!isNaN(g)) {
		gm =parseFloat(parseFloat(gm).toFixed(3));
		gm = gm.toString()
	}
	else{
		gm = "inf";
	}

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
			y: mag[i],
		});
	}
	dataSeries.dataPoints = dataPoints;
	magnitude.push(dataSeries);
	var dataSeries = { type: "line" };
	var dataPoints = [];
	for (var i = 0; i < limit; i += 1) {
		dataPoints.push({
			x: omega[i],
			y: ph[i],
		});
	}
	dataSeries.dataPoints = dataPoints;
	phase.push(dataSeries);

	Mag = {
		zoomEnabled: true,
		animationEnabled: true,
		theme: "light",
		title: {
			display: true,
			text: "Gm =" + gm + " dB/ Pm =" + pm + " deg "+wp,
			fontSize: 20,
		},

		axisX: {
			logarithmic: true,
			title: "Frequency",
			gridThickness: 1,
		},
		axisY: {
			lineThickness: 1,
			title: "Magnitude dB",
		},
		data: magnitude,
	};
	Ph = {
		zoomEnabled: true,
		animationEnabled: true,
		theme: "light",
		pointStyle: "dash",
		title: {},
		axisX: {
			logarithmic: true,
			title: "Frequency",
			gridThickness: 1,
		},
		axisY: {
			lineThickness: 1,
			title: "Phase",
		},
		data: phase,
	};

	if (omega_comp.value != "" || omega_comp.value == null) {
		omega_comp = omega_comp.value;
		mag_comp = mag_comp.value;
		ph_comp = ph_comp.value;
		omega_comp = omega_comp.match(/-?\d+(?:\.\d+)?/g).map(Number);
		ph_comp = ph_comp.match(/-?\d+(?:\.\d+)?/g).map(Number);
		mag_comp = mag_comp.match(/-?\d+(?:\.\d+)?/g).map(Number);

		var pm = document.getElementById("pm_comp").value;
		var gm = document.getElementById("gm_comp").value;
		var wp = document.getElementById("wp_comp").value;
		var w = parseFloat(wp);
		console.log(p)
		if (!isNaN(w)) {
			wp = parseFloat(parseFloat(wp).toFixed(3));
			wp = "(at "+wp+"rad/s)"
		}
		else{
			wp = "";
		}
		console.log(wp+"shoof")
		console.log(pm+"rrrr")
		var p = parseFloat(pm);
		console.log(p)

		if (!isNaN(p)) {
			pm = parseFloat(parseFloat(pm).toFixed(3));
		}
		else{
			pm = "inf";
		}
		var g = parseFloat(gm);
		if (!isNaN(g)) {
			gm =parseFloat(parseFloat(gm).toFixed(3));
			gm = gm.toString()
		}
		else{
			gm = "inf";
		}

		var limit_comp = omega_comp.length;
		var dataSeries = { type: "line" };
		var dataPoints = [];
		for (var i = 0; i < limit_comp; i += 1) {
			dataPoints.push({
				x: omega_comp[i],
				y: mag_comp[i],
			});
		}
		dataSeries.dataPoints = dataPoints;
		magnitude.push(dataSeries);
		var dataSeries = { type: "line" };
		var dataPoints = [];
		for (var i = 0; i < limit_comp; i += 1) {
			dataPoints.push({
				x: omega_comp[i],
				y: ph_comp[i],
			});
		}
		dataSeries.dataPoints = dataPoints;
		phase.push(dataSeries);
		Mag = {
			zoomEnabled: true,
			animationEnabled: true,
			theme: "light",
			title: {
				display: true,
				text: "Gm =" + gm + " dB/ Pm =" + pm + " deg "+wp,
				fontSize: 20,
			},
			axisX: {
				logarithmic: true,
				title: "Frequency",
				gridThickness: 1,
			},
			axisY: {
				lineThickness: 1,
				title: "Magnitude dB",
			},
			axisY2: {
				lineThickness: 1,
				title: "Magnitude comp",
			},
			data: magnitude,
		};
		Ph = {
			zoomEnabled: true,
			animationEnabled: true,
			theme: "light",
			pointStyle: "dash",
			title: {},
			axisX: {
				logarithmic: true,
				title: "Frequency ",
				gridThickness: 1,
			},
			axisY: {
				lineThickness: 1,
				title: "Phase",
			},
			axisY2: {
				title: "Phase_comp",
				lineThickness: 1,
			},
			data: phase,
		};
	}
	var chartPP = new CanvasJS.Chart("Phase", Ph);
	chartPP.render();
	var chartMM = new CanvasJS.Chart("Magnitude", Mag);
	chartMM.render();
};

function display(){
	var name = document.getElementById("selector2").value;
	var elements = document.getElementsByClassName("option");
	for (let i = 0; i < elements.length; i++) {
		var element = elements[i];
		if (element.id == name) {
			document.getElementById(name).style.display = "block";
		} else {
			element.style.display = "none";
		}
	}
}
function openForm() {
	document.getElementById("edit").style.display = "block";
	document.getElementById("tf").style.display = "none";
}
function close() {
	document.getElementById("edit").style.display = "none";
	document.getElementById("tf").style.display = "block";
}

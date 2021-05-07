    function display() {
        var name = document.getElementById("selector").value;
        console.log(name)
        var elements = document.getElementsByClassName("option")
        for (let i = 0; i < elements.length; i++) {
            var element = elements[i];
            if (element.id == name) {
                document.getElementById(name).style.display = "block";
            } else {
                element.style.display = "none"
            }
        }
    }

    function sim(t ,v) {
        /* 
                    var ani = document.getElementById('animation')
                    if (ani.checked == true) */
        duration = 0;
        var ctx = document.getElementById('myChart').getContext('2d');
        var chart = new Chart(ctx, {
            // The type of chart we want to create
            type: 'line',

            // The data for our dataset
            data: {
                labels: [],
                datasets: [{
                    label: 'My First dataset',
                    borderColor: 'rgb(255, 99, 132)',
                    data: []
                }]
            },
            options: {
                scales: {
                    xAxes: [{
                        ticks: {
                            beginAtZero: true,

                        }
                    }],
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                },
                animation: {
                    duration: duration,
                    easing: 'easeInCirc',

                },
                hover: {
                    duration: 0
                },
                responsiveAnimationDuration: 0
            }
        });
        var counter = 0;
        var interval = setInterval(function () {
            if (lt < counter) {
                clearInterval(interval);
                return;
            }
            console.log(counter + ' ' + lt);
            chart.data.labels.push(t[counter]);
            chart.data.datasets[0].data.push(v[counter]);
            chart.update();
            counter++
        }, 100)
    }

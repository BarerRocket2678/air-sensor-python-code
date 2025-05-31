// Written by Cody Zavodsky
// Programming Assistance from ChatGPT
// Technical AQI info from the US EPA: https://document.airnow.gov/technical-assistance-document-for-the-reporting-of-daily-air-quailty.pdf

let dataChart;
let dataChart_hr;
let dataChart_dy;

let timeLabels = [];
let timeLabels_hr = [];
let timeLabels_dy = [];

let pm25 = [];
let pm100 = [];
let pm25_hr = [];
let pm100_hr = [];
let pm25_dy = [];
let pm100_dy = [];

let Colorblind = false;

function colorblind() {
        if (Colorblind == false) {
                Colorblind = true;
        }
        else {
                Colorblind = false;
        }

        dataChart.data.datasets.forEach((dataset) => {
                dataset.segment.borderColor = (ctx) => {
                        const y = ctx.p1.parsed.y;

                        if(Colorblind == true) {
                                if (y >= 301) return 'rgb(100, 0, 21)';
                                if (y >= 201) return 'rgb(137, 9, 151)';
                                if (y >= 151) return 'rgb(240, 34, 0)';
                                if (y >= 101) return 'rgb(255, 130, 5)';
                                if (y >= 51) return 'rgb(225, 201, 5)';
                                return 'rgb(158, 255, 145)';
                        }
                        else {
                                if (y >= 301) return 'rgb(126, 0, 35)';
                                if (y >= 201) return 'rgb(143, 63, 151)';
                                if (y >= 151) return 'rgb(255, 0, 0)';
                                if (y >= 101) return 'rgb(255, 126, 0)';
                                if (y >= 51) return 'rgb(225, 255, 0)';
                                return 'rgb(0, 228, 0)';
                        }

                };
        });

        dataChart.update();

        dataChart_hr.data.datasets.forEach((dataset) => {
                dataset.segment.borderColor = (ctx) => {
                        const y = ctx.p1.parsed.y;
                        
                        if(Colorblind == true) {
                                if (y >= 301) return 'rgb(100, 0, 21)';
                                if (y >= 201) return 'rgb(137, 9, 151)';
                                if (y >= 151) return 'rgb(240, 34, 0)';
                                if (y >= 101) return 'rgb(255, 130, 5)';
                                if (y >= 51) return 'rgb(225, 201, 5)';
                                return 'rgb(158, 255, 145)';
                        }
                        else {
                                if (y >= 301) return 'rgb(126, 0, 35)';
                                if (y >= 201) return 'rgb(143, 63, 151)';
                                if (y >= 151) return 'rgb(255, 0, 0)';
                                if (y >= 101) return 'rgb(255, 126, 0)';
                                if (y >= 51) return 'rgb(225, 255, 0)';
                                return 'rgb(0, 228, 0)';
                        }
                        
                };
        });

        dataChart_hr.update();

        dataChart_dy.data.datasets.forEach((dataset) => {
                dataset.segment.borderColor = (ctx) => {
                        const y = ctx.p1.parsed.y;
                        
                        if(Colorblind == true) {
                                if (y >= 301) return 'rgb(100, 0, 21)';
                                if (y >= 201) return 'rgb(137, 9, 151)';
                                if (y >= 151) return 'rgb(240, 34, 0)';
                                if (y >= 101) return 'rgb(255, 130, 5)';
                                if (y >= 51) return 'rgb(225, 201, 5)';
                                return 'rgb(158, 255, 145)';
                        }
                        else {
                                if (y >= 301) return 'rgb(126, 0, 35)';
                                if (y >= 201) return 'rgb(143, 63, 151)';
                                if (y >= 151) return 'rgb(255, 0, 0)';
                                if (y >= 101) return 'rgb(255, 126, 0)';
                                if (y >= 51) return 'rgb(225, 255, 0)';
                                return 'rgb(0, 228, 0)';
                        }
                        
                };
        });

        dataChart_dy.update();
}


window.onload = function() {
        const ctx = document.getElementById('Chart').getContext('2d')
        dataChart = new Chart(ctx, {
                type: 'line',
                data: {
                        labels: [],
                        datasets: [
                                {
                                        label: 'PM 2.5',
                                        fill: false,
                                        data: [],
                                        borderColor: 'white',
                                        backgroundColor: 'white',
                                        segment: {
                                                borderColor: ctx => {
                                                        const y = ctx.p1.parsed.y;
                                                        if (y >= 301) return 'rgb(126, 0, 35)';
                                                        if (y >= 201) return 'rgb(143, 63, 151)';
                                                        if (y >= 151) return 'rgb(255, 0, 0)';
                                                        if (y >= 101) return 'rgb(255, 126, 0)';
                                                        if (y >= 51) return 'rgb(225, 255, 0)';
                                                        return 'rgb(0, 228, 0)';
                                                }

                                        },
                                        pointBackgroundColor: 'white',
                                        pointBorderColor: 'white',
                                        tension: 1,
                                        cubicInterpolationMode: 'monotone'
                                },
                                {
                                        label: 'PM 10.0',
                                        fill: false,
                                        data: [],
                                        borderColor: 'black',
                                        backgroundColor: 'black',
                                        segment: {
                                                borderColor: ctx => {
                                                const y = ctx.p1.parsed.y;

                                                if (y >= 301) return 'rgb(126, 0, 35)';
                                                if (y >= 201) return 'rgb(143, 63, 151)';
                                                if (y >= 151) return 'rgb(255, 0, 0)';
                                                if (y >= 101) return 'rgb(255, 126, 0)';
                                                if (y >= 51) return 'rgb(225, 255, 0)';
                                                return 'rgb(0, 228, 0)';
                                                }
                                        },
                                        pointBackgroundColor: 'black',
                                        pointBorderColor: 'black',
                                        tension: 1,
                                        cubicInterpolationMode: 'monotone'
                                }

                        ]
                },
                options: {
                        responsive : true,
                        scales: {
                                x: { 
                                        grid: {color: '#8c8c8c'},
                                        title: { 
                                                display: true, text: 'Time' 
                                        } 
                                },
                                y: { 
                                        grid: {color: '#8c8c8c'},
                                        title: { 
                                                display: true, text: 'AQI level' 
                                        }, 
                                        beginAtZero: true 
                                }
                        }
                }
        });

        const ctx2 = document.getElementById('Chart_hr').getContext('2d')
        dataChart_hr = new Chart(ctx2, {
                type: 'line',
                data: {
                        labels: [],
                        datasets: [
                                {
                                        label: 'PM 2.5 hour mean',
                                        fill: false,
                                        data: [],
                                        borderColor: 'white',
                                        backgroundColor: 'white',
                                        segment: {
                                                borderColor: ctx => {
                                                        const y = ctx.p1.parsed.y;

                                                        if (y >= 301) return 'rgb(126, 0, 35)';
                                                        if (y >= 201) return 'rgb(143, 63, 151)';
                                                        if (y >= 151) return 'rgb(255, 0, 0)';
                                                        if (y >= 101) return 'rgb(255, 126, 0)';
                                                        if (y >= 51) return 'rgb(225, 255, 0)';
                                                        return 'rgb(0, 228, 0)';

                                                }
                                        },
                                        pointBackgroundColor: 'white',
                                        pointBorderColor: 'white',
                                        tension: 1,
                                        cubicInterpolationMode: 'monotone'
                                },
                                {
                                        label: 'PM 10.0 hour mean',
                                        fill: false,
                                        data: [],
                                        borderColor: 'black',
                                        backgroundColor: 'black',
                                        segment: {
                                                borderColor: ctx => {
                                                const y = ctx.p1.parsed.y;

                                                if (y >= 301) return 'rgb(126, 0, 35)';
                                                if (y >= 201) return 'rgb(143, 63, 151)';
                                                if (y >= 151) return 'rgb(255, 0, 0)';
                                                if (y >= 101) return 'rgb(255, 126, 0)';
                                                if (y >= 51) return 'rgb(225, 255, 0)';
                                                return 'rgb(0, 228, 0)';

                                                }
                                        },
                                        pointBackgroundColor: 'black',
                                        pointBorderColor: 'black',
                                        tension: 1,
                                        cubicInterpolationMode: 'monotone'
                                }

                        ]
                },
                options: {
                        responsive : true,
                        scales: {
                                x: { 
                                        grid: {color: '#8c8c8c'},
                                        title: { 
                                                display: true, text: 'Time' 
                                        } 
                                },
                                y: { 
                                        grid: {color: '#8c8c8c'},
                                        title: { 
                                                display: true, text: 'AQI level' 
                                        }, 
                                        beginAtZero: true 
                                }
                        }
                }

       });

        const ctx3 = document.getElementById('Chart_dy').getContext('2d');
        dataChart_dy = new Chart(ctx3, {
                type: 'line',
                data: {
                        labels: [],
                        datasets: [
                                {
                                        label: 'PM 2.5 day mean',
                                        fill: false,
                                        data: [],
                                        borderColor: 'white',
                                        backgroundColor: 'white',
                                        segment: {
                                                borderColor: ctx => {
                                                        const y = ctx.p1.parsed.y;

                                                        if (y >= 301) return 'rgb(126, 0, 35)';
                                                        if (y >= 201) return 'rgb(143, 63, 151)';
                                                        if (y >= 151) return 'rgb(255, 0, 0)';
                                                        if (y >= 101) return 'rgb(255, 126, 0)';
                                                        if (y >= 51) return 'rgb(225, 255, 0)';
                                                        return 'rgb(0, 228, 0)';

                                                }
                                        },
                                        pointBackgroundColor: 'white',
                                        pointBorderColor: 'white',
                                        tension: 1,
                                        cubicInterpolationMode: 'monotone'
                                },
                                {
                                        label: 'PM 10.0 day mean',
                                        fill: false,
                                        data: [],
                                        borderColor: 'black',
                                        backgroundColor: 'black',
                                        segment: {
                                                borderColor: ctx => {
                                                const y = ctx.p1.parsed.y;
                                                
                                                if (y >= 301) return 'rgb(126, 0, 35)';
                                                if (y >= 201) return 'rgb(143, 63, 151)';
                                                if (y >= 151) return 'rgb(255, 0, 0)';
                                                if (y >= 101) return 'rgb(255, 126, 0)';
                                                if (y >= 51) return 'rgb(225, 255, 0)';
                                                return 'rgb(0, 228, 0)';

                                                }
                                        },
                                        pointBackgroundColor: 'black',
                                        pointBorderColor: 'black',
                                        tension: 1,
                                        cubicInterpolationMode: 'monotone'
                                }

                        ]
                },
                options: {
                        responsive : true,
                        scales: {
                                x: { 
                                        grid: {color: '#8c8c8c'},
                                        title: { 
                                                display: true, text: 'Time' 
                                        } 
                                },
                                y: { 
                                        grid: {color: '#8c8c8c'},
                                        title: { 
                                                display: true, text: 'AQI level' 
                                        }, 
                                        beginAtZero: true 
                                }
                        }
                }
        });

        fetch('/history')
                .then(response => response.json())
                .then (database => {
                        if (database.length > 0) {
                                database.forEach((entry, index) => {
                                        let entrytimeserver = new Date(entry["time"]);
                                        timeLabels.push(entrytimeserver.toLocaleString());
                                        pm25.push(entry.pm25);
                                        pm100.push(entry.pm100);

                                });

                                dataChart.data.labels = timeLabels;
                                dataChart.data.datasets[0].data = pm25;
                                dataChart.data.datasets[1].data = pm100;
                                dataChart.update();
                        }
                }).catch(error => console.error("Could not load database:", error));

        fetch('/history_hr')
                .then(response_hr => response_hr.json())
                .then (database_hr => {
                        if (database_hr.length > 0) {
                                database_hr.forEach((entry, index) => {
                                        let entrytimeserver = new Date(entry["time"]);
                                        timeLabels_hr.push(entrytimeserver.toLocaleString());
                                        pm25_hr.push(entry.pm25_hr);
                                        pm100_hr.push(entry.pm100_hr)
                                });

                                dataChart_hr.data.labels = timeLabels_hr;
                                dataChart_hr.data.datasets[0].data = pm25_hr;
                                dataChart_hr.data.datasets[1].data = pm100_hr;
                                dataChart_hr.update();
                        }
                }).catch(error => console.error("Could not load database:", error));

        fetch('/history_dy')
                .then(response_dy => response_dy.json())
                .then (database_dy => {
                        console.log("Fetched daily history:", database_dy);
                        if (database_dy.length > 0) {
                                database_dy.forEach((entry, index) => {
                                        let entrytimeserver = new Date(entry["time"]);
                                        timeLabels_dy.push(entrytimeserver.toLocaleString());
                                        pm25_dy.push(entry.pm25_dy);
                                        pm100_dy.push(entry.pm100_dy)
                                });

                                dataChart_dy.data.labels = timeLabels_dy;
                                dataChart_dy.data.datasets[0].data = pm25_dy;
                                dataChart_dy.data.datasets[1].data = pm100_dy;
                                dataChart_dy.update();

                                let status = "Good";
                                let effects = ["Effects: None.", "Effects: Consider reducing exertion for sensitive people.", "Effects: Reduce exertion for sensitive people, people with asthma, and people with heart disease.", "Effects: Avoid exertion for sensitive people, people with asthma, and people with heart disease. The general public should reduce exertion.", "Effects: Avoid all activity for sensitive people, people with asthma, and people with heart disease. The general public should avoid exertion.", "Effects: Avoid contact with contaminated air for sensitive people, people with asthma, and people with heart disease. The general public should avoid all activity"]; 
                                if (pm25_dy[pm25_dy.length - 1] > pm100_dy[pm100_dy.length - 1]) {
                                        if(pm25_dy[pm25_dy.length - 1] > 500) {            
                                                document.getElementById("Status").innerHTML = "Status: Hazardous (DANGER: Levels have exceeded the max (500) of the AQI system!)";
                                                document.getElementById("Effects").innerHTML = effects[5];
                                        }
                                        else if(pm25_dy[pm25_dy.length - 1] > 300) {
                                                document.getElementById("Status").innerHTML = "Status: Hazardous";
                                                document.getElementById("Effects").innerHTML = effects[5];
                                        }
                                        else if(pm25_dy[pm25_dy.length - 1] > 200) {
                                                document.getElementById("Status").innerHTML = "Status: Very Unhealthy";
                                                document.getElementById("Effects").innerHTML = effects[4];
                                        }
                                        else if(pm25_dy[pm25_dy.length - 1] > 150) {
                                                document.getElementById("Status").innerHTML = "Status: Unhealthy";
                                                document.getElementById("Effects").innerHTML = effects[3];
                                        }
                                        else if(pm25_dy[pm25_dy.length - 1] > 100) {
                                                document.getElementById("Status").innerHTML = "Status: Unhealthy for sensitive groups";
                                                document.getElementById("Effects").innerHTML = effects[2];
                                        }
                                        else if(pm25_dy[pm25_dy.length - 1] > 50) {
                                                document.getElementById("Status").innerHTML = "Status: Moderate";
                                                document.getElementById("Effects").innerHTML = effects[1];
                                        }
                                        else if(pm25_dy[pm25_dy.length - 1] >= 0) {
                                                document.getElementById("Status").innerHTML = "Status: Good";
                                                document.getElementById("Effects").innerHTML = effects[0];
                                        }
                                } else {
                                        if(pm100_dy[pm100_dy.length - 1] > 500) {            
                                                document.getElementById("Status").innerHTML = "Status: Hazardous (DANGER: Levels have exceeded the max (500) of the AQI system!)";
                                                document.getElementById("Effects").innerHTML = effects[5];
                                        }
                                        else if(pm100_dy[pm100_dy.length - 1] > 300) {
                                                document.getElementById("Status").innerHTML = "Status: Hazardous";
                                                document.getElementById("Effects").innerHTML = effects[5];
                                        }
                                        else if(pm100_dy[pm100_dy.length - 1] > 200) {
                                                document.getElementById("Status").innerHTML = "Status: Very Unhealthy";
                                                document.getElementById("Effects").innerHTML = effects[4];
                                        }
                                        else if(pm100_dy[pm100_dy.length - 1] > 150) {
                                                document.getElementById("Status").innerHTML = "Status: Unhealthy";
                                                document.getElementById("Effects").innerHTML = effects[3];
                                        }
                                        else if(pm100_dy[pm100_dy.length - 1] > 100) {
                                                document.getElementById("Status").innerHTML = "Status: Unhealthy for sensitive groups";
                                                document.getElementById("Effects").innerHTML = effects[2];
                                        }
                                        else if(pm100_dy[pm100_dy.length - 1] > 50) {
                                                document.getElementById("Status").innerHTML = "Status: Moderate";
                                                document.getElementById("Effects").innerHTML = effects[1];
                                        }
                                        else if(pm100_dy[pm100_dy.length - 1] >= 0) {
                                                document.getElementById("Status").innerHTML = "Status: Good";
                                                document.getElementById("Effects").innerHTML = effects[0];
                                        }
                                }
                        }

                }).catch(error => console.error("Could not load database:", error));

}

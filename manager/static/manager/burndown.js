const taskboardID = Number(window.location.href.split('/').slice(-3)[0]);

// Back to Taskboard button
const taskboardLink = document.getElementById('taskboard-link');
taskboardLink.href = `/manager/taskboard/${taskboardID}`;

const today = new Date();
today.setHours(0, 0, 0, 0);

async function fetchEstimateHistoryData(interval) {
    const response = await fetch(`/api/estimate_history/?taskboard=${taskboardID}&interval=${interval}`);
    const estimateHistories = await response.json();
    return estimateHistories;
}

async function fetchVelocityData(startDate, interval, mode) {
    const response = await fetch(`/api/velocity/?taskboard=${taskboardID}&start=${startDate}&interval=${interval}&mode=${mode}`);
    const Velocity = await response.json();
    return Velocity
}

async function fetchTaskData(startDate, endDate){
    const response = await fetch(`/api/tasks/?taskboard=${taskboardID}&start_date=${startDate.toISOString().slice(0, 19)}&end_date=${endDate.toISOString().slice(0, 19)}`)
    const tasks = await response.json()
    return tasks
}

async function fetchEventData(startDate, endDate){
    const response = await fetch(`/api/events/?start_date=${startDate.toISOString().slice(0, 19)}&end_date=${endDate.toISOString().slice(0, 19)}`)
    const events = await response.json()
    return events
}

function calculateSlope(d1, d2, t1, t2) {
    const numberOfMiliseconds = 1000 * 60 * 60 * 24

    const startDate = new Date(d1);
    const endDate = new Date(d2);

    daysBetween = (endDate - startDate) / numberOfMiliseconds;

    if (daysBetween === 0) {
        return -t1;
    }
    return (t2 - t1) / daysBetween;
}

function formatDate(date) {
    return date.toLocaleDateString('en-CA').split('T')[0];
}

function generateDateRange(startDate, endDate) {
    const start = new Date(startDate);
    const end = new Date(endDate);
    const dateArray = [];

    let currentDate = start;
    while (currentDate <= end) {
        dateArray.push(formatDate(currentDate));
        currentDate.setDate(currentDate.getDate() + 1);
    }

    return dateArray;
}

function fillDates(inputData) {
    const previewCount = 14

    const today = new Date();
    const previewStartDate = new Date(today);
    previewStartDate.setDate(today.getDate() - previewCount - 1);

    const data = inputData.map(item => ({ date: new Date(item.date), time_remaining: item.time_remaining }));

    const result = [];
    let lastKnownTimeRemaining = null;

    for (let i = 0; i < data.length; i++) {
        const currentDate = data[i].date;
        const timeRemaining = data[i].time_remaining;
        if (lastKnownTimeRemaining !== null) {
            let previousDate = result.length > 0 ? new Date(result[result.length - 1].x) : previewStartDate;
            previousDate.setDate(previousDate.getDate() + 1);
            while (previousDate < currentDate) {
                result.push({ x: formatDate(previousDate), y: lastKnownTimeRemaining });
                previousDate.setDate(previousDate.getDate() + 1);
            }
        }
        result.push({ x: formatDate(currentDate), y: timeRemaining });
        lastKnownTimeRemaining = timeRemaining;
    }
    if (result.length > 0) {
        let lastDate = new Date(result[result.length - 1].x);
        lastDate.setDate(lastDate.getDate() + 1);
        while (lastDate <= today) {
            result.push({ x: formatDate(lastDate), y: lastKnownTimeRemaining });
            lastDate.setDate(lastDate.getDate() + 1);
        }
    }
    return result.filter(item => new Date(item.x) >= previewStartDate);
}

function trendAnnotation(x1, x2, y1, y2, color) {
    return {
        type: 'line',
        mode: 'xy',
        scaleID: 'x-axis-0',
        value: x1,
        endValue: x2,
        borderColor: color,
        borderWidth: 1,
        borderDash: [5, 5],
        xMin: x1,
        xMax: x2,
        yMin: y1,
        yMax: y2,
        display: true
    };
}

function lineAnnotation(endDate, title, color){
    return {
        type: 'line',
        scaleID: 'x',
        value: endDate,
        borderColor: color,
        borderWidth: 1,
        borderDash: [5, 5],
        label: {
            content: title,
            enabled: true,
            position: 'top'
        },
        display: true
    }
}

function createLineAnnotations(data, color) {
    const endDates = data.map(item => formatDate(new Date(item.end_date)));
    const titles = data.map(item => item.title);
    const annotations = endDates.map((endDate, index) => 
        lineAnnotation(endDate, titles[index], color)
    );

    return annotations;
}

function getNearestTrendData(dsiplayData, taskAnnotations, eventAnnotations) {

    const x1 = formatDate(today);

    const y1 = dsiplayData.find(item => item.x === x1).y;
    
    const checkableDates = [...taskAnnotations, ...eventAnnotations]
        .filter(annotation => annotation.display)
        .map(annotation => new Date(annotation.value))
        .sort((a, b) => a - b)[0];

    const x2 = checkableDates ? formatDate(checkableDates) : null;

    const y2 = 0;
    const color = 'rgba(255, 100, 100, 1)';

    return { x1, x2, y1, y2, color };
}

function initializeChart(ctx, dates, displayData, lineAnnotations, trendAnnotations, scaleMax) {

    const chartStartDate = lineAnnotations[lineAnnotations.length - 1].value;

    const startIndex = dates.indexOf(chartStartDate);
    const adjustedStartIndex = startIndex <= 7 ? 0 : startIndex - 7;
    const endIndex = startIndex + scaleMax;

    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: dates,
            datasets: [
                {
                    label: 'Time Remaining',
                    data: displayData,
                    borderWidth: 1,
                },
            ]
        },
        options: {
            scales: {
                x: {
                    type: 'category',
                    min: dates[adjustedStartIndex],
                    max: dates[endIndex],
                },
                y: {
                    beginAtZero: true,
                }
            },
            plugins: {
                annotation: {
                    annotations: [...lineAnnotations, ...trendAnnotations]
                },
                legend: {
                    display: false
                }
            }
        }
    });
}

function updateAnnotations(taskAnnotations, eventAnnotations, chart, displayData, velocityEndDate) {
    const updateDisplayStatus = (annotations, type) => {
        annotations.forEach((annotation, index) => {
            const checkbox = document.getElementById(`${type}-checkbox-${index}`);
            annotation.display = checkbox.checked;
        });
    };

    const updateTrendLine = (trendLine, x2, y1, y2, velocityEndDate) => {
        const trendEndDate = new Date(x2);
        if (x2 && y1 > 0 && trendEndDate <= velocityEndDate) {
            trendLine.xMax = x2;
            trendLine.yMax = y2;
            trendLine.display = true;
        } else {
            trendLine.display = false;
        }
    };

    updateDisplayStatus(taskAnnotations, 'task');
    updateDisplayStatus(eventAnnotations, 'event');

    const { x1, x2, y1, y2 } = getNearestTrendData(displayData, taskAnnotations, eventAnnotations);
    const trendLine = chart.options.plugins.annotation.annotations.find(annotation => 
        annotation.borderColor === 'rgba(255, 100, 100, 1)' && annotation.mode === 'xy'
    );

    updateTrendLine(trendLine, x2, y1, y2, velocityEndDate);

    if (trendLine && trendLine.display) {
        const slope = calculateSlope(x1, x2, y1, y2);
        updateWarningEstimate(slope);
    } else {
        updateWarningEstimate(0);
    }

    chart.update();
}

function createCheckboxes(container, data, type, updateAnnotations) {
    if (data.length === 0) {
        container.innerText = `No ${type.charAt(0).toUpperCase() + type.slice(1)}s.`;
        return; 
      }      
    data.forEach((item, index) => {
        const checkboxDiv = document.createElement('div');
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = `${type}-checkbox-${index}`;
        checkbox.checked = true;

        const label = document.createElement('label');
        label.htmlFor = `${type}-checkbox-${index}`;
        label.innerText = item.title;

        checkbox.addEventListener('change', updateAnnotations);

        checkboxDiv.appendChild(checkbox);
        checkboxDiv.appendChild(label);
        container.appendChild(checkboxDiv);
    });
}

function updateDoneByEstimate(velocityEndDate) {
    if (!velocityEndDate || velocityEndDate.length === 0) {
        document.getElementById("done-by").innerText = `Done-by Estimate: N/A`;
    } else {
        document.getElementById("done-by").innerText = `Done-by Estimate: ${velocityEndDate}`;
    }
}

function updateVelocityEstimate(velocitySlope) {
    if (velocitySlope === 0 || isNaN(velocitySlope)) {
        document.getElementById("slope").innerText = `Average Velocity: N/A`;
    } else {
        document.getElementById("slope").innerText = `Average Velocity: ${velocitySlope.toFixed(2)} hr/day`;
    }
}

function updateWarningEstimate(velocitySlope) {
    if (velocitySlope === 0 || isNaN(velocitySlope)) {
        document.getElementById('warning').innerText = 'Required velocity: N/A';
    } else {
        document.getElementById('warning').innerText = `Required velocity: ${-velocitySlope.toFixed(2)} hr/day`;
    }
}

async function main() {
    let interval = 'day'
    const scaleMax = 30;

    const estHistData = await fetchEstimateHistoryData(interval);

    if (estHistData.length === 0 ){
        const ctx = document.getElementById('no-data');
        ctx.innerHTML = `It seems like you haven't added any tasks. <br> Add some tasks on the taskboard.`;
        ctx.style.height = '220px';
        ctx.style.textAlign = 'center';

        updateDoneByEstimate(0)
        updateVelocityEstimate(0)
        updateWarningEstimate(0)
        
        return;
    }

    // Fill estimate history data
    const displayData = fillDates(estHistData)

    const maxElement = estHistData.reduce((max, current) => current.time_remaining > max.time_remaining ? current : max);

    const velocity = await fetchVelocityData(maxElement.date, interval)

    if (!velocity.x || !velocity.velocity) {
        var element = document.getElementById('not-enough-data');
        element.textContent = "Not enough data to estimate velocity.";
        element.style.color = 'yellow';

        updateVelocityEstimate(0);
        updateDoneByEstimate(0);

        // Initialize the chart with the data and annotations
        const ctx = document.getElementById('myChart');
        initializeChart(ctx, [], displayData, [lineAnnotation(formatDate(today), 'Today', 'blue')], [], scaleMax);

        createCheckboxes(document.getElementById('task-checkboxes'), [], 'task');
        createCheckboxes(document.getElementById('event-checkboxes'), [], 'event');

    } else {
        const velocityTrend = trendAnnotation(maxElement.date, velocity.x, maxElement.time_remaining, 0, 'rgba(75, 192, 192, 1)')

        updateVelocityEstimate(velocity.velocity);
        updateDoneByEstimate(velocity.x);

        // Get all relevant dates and generate date range for the chart
        const dates = generateDateRange(estHistData[0].date, velocity.x)

        // Get tasks and evets after today or before the velocityEndDate and annoEndDate
        const velocityEndDate = new Date(velocity.x)
        velocityEndDate.setHours(23, 59, 59, 999)

        const annoMaxDate = new Date(displayData[0].x);
        annoMaxDate.setDate(annoMaxDate.getDate() + scaleMax);

        const annoEndDate = velocityEndDate < annoMaxDate ? velocityEndDate : annoMaxDate;

        const tasks = await fetchTaskData(today, annoEndDate)
        const events = await fetchEventData(today, annoEndDate)

        // Create line annotations for tasks, events, and today
        const taskAnnotations = createLineAnnotations(tasks, 'red');
        const eventAnnotations = createLineAnnotations(events, 'yellow');
        const todayAnnotation = lineAnnotation(formatDate(today), 'Today', 'blue');

        // Create checkboxes for tasks and events to update annotations dynamically
        createCheckboxes(document.getElementById('task-checkboxes'), tasks, 'task', () => updateAnnotations(taskAnnotations, eventAnnotations, chart, displayData, velocityEndDate));
        createCheckboxes(document.getElementById('event-checkboxes'), events, 'event', () => updateAnnotations(taskAnnotations, eventAnnotations, chart, displayData, velocityEndDate));
    
        // Calculate the nearest trend line
        const { x1, x2, y1, y2, color } = getNearestTrendData(displayData, taskAnnotations, eventAnnotations);
        const nearestTrend = trendAnnotation(x1, x2, y1, y2, color);

        // Combine all annotations
        const lineAnnotations = [...taskAnnotations, ...eventAnnotations, todayAnnotation];
        const trendAnnotations = [velocityTrend, nearestTrend];

        // Initialize the chart with the data and annotations
        const ctx = document.getElementById('myChart');
        let chart = initializeChart(ctx, dates, displayData, lineAnnotations, trendAnnotations, scaleMax);

        updateAnnotations(taskAnnotations, eventAnnotations, chart, displayData, velocityEndDate)
    }

    document.getElementById('timescaleSelector').addEventListener('change', function() {
        const timescale = this.value;

        if (timescale === 'month') {
            interval = 'month';
        } else if (timescale === 'week') {
            interval = 'week';
        } else {
            interval = 'day';
        }

        const checkboxes = document.querySelectorAll('#task-checkboxes input, #event-checkboxes input');
        checkboxes.forEach(checkbox => {
            checkbox.disabled = (timescale !== 'day');
        });
    });

}

main();
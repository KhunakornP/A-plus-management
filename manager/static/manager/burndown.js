const taskboardID = Number(window.location.href.split('/').slice(-3)[0]);
const numberOfMiliseconds = 1000 * 60 * 60 * 24

// Back to Taskboard button
const taskboardLink = document.getElementById('taskboard-link');
taskboardLink.href = `/manager/taskboard/${taskboardID}`;

async function fetchEventJson(){
    const response = await fetch(`/api/events/`)
    const events = await response.json()
    return events
}

async function fetchTaskJson(){
    const response = await fetch(`/api/tasks/?taskboard=${taskboardID}`)
    const tasks = await response.json()
    return tasks
}

async function fetchEstimateHistoryData() {
    const response = await fetch(`/api/estimate_history/?taskboard=${taskboardID}`);
    const estimate_histories = await response.json();
    return estimate_histories;
}

// Return the number of days between d1 and d2
// par: Date, ret: Number
function calculateDaysBetween(d1, d2) {
    const startDate = new Date(d1);
    const endDate = new Date(d2);
    return (endDate - startDate) / numberOfMiliseconds;
  }

// ret: num
function calculateSlope(t1, t2, daysBetween) {
    return (t2 - t1) / daysBetween;
}

function formatDate(date) {
    return date.toISOString().split('T')[0];
}

// Return the number days from d1 to the day the trend reaches 0 based on t1 and t2.
function daysUntilZero(d1, d2, t1, t2) {
    const daysBetween = calculateDaysBetween(d1, d2);
    const slope = calculateSlope(t1, t2, daysBetween);
    document.getElementById("slope").innerText = `Average Velocity: ${-slope.toFixed(2)} hr/day`;
    return t1/-slope;
}

function drawLine(startTime, startDate, nDays) {
    const points = [];
    const start = new Date(startDate);
    for (let i = 0; i <= nDays; i++) {
        const currentDate = new Date(start);
        currentDate.setDate(start.getDate() + i);
        points.push({ x: formatDate(currentDate), y: startTime - (startTime / nDays) * i });
    }
    return points;
}

//Return a list of dates from startDate to endDate
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

function fillEstHistData(data) {
    const result = [];
    let lastKnownTimeRemaining = null;

    // Convert the date strings to Date objects for easier manipulation
    data.forEach((entry, index) => {
        const currentDate = new Date(entry.date);
        const nextDate = index < data.length - 1 ? new Date(data[index + 1].date) : null;

        // Add the current entry to the result
        result.push({ x: entry.date, y: entry.time_remaining });
        lastKnownTimeRemaining = entry.time_remaining;

        // Fill in the gaps between the current date and the next date
        if (nextDate) {
            let gapDate = new Date(currentDate);
            gapDate.setDate(gapDate.getDate() + 1);

            while (gapDate < nextDate) {
                result.push({ x: gapDate.toISOString().split('T')[0], y: lastKnownTimeRemaining });
                gapDate.setDate(gapDate.getDate() + 1);
            }
        }
    });

    return result;
}

function annotate(data, color){
    const endDates = data.map(task => formatDate(new Date(task.end_date)));
    const titles = data.map(item => item.title);
    const annotations = endDates.map((endDate, index) => ({
        type: 'line',
        mode: 'vertical',
        scaleID: 'x',
        value: endDate,
        borderColor: color,
        borderWidth: 1,
        borderDash: [5, 5],
        label: {
            content: titles[index],
            enabled: true,
            position: 'top'
        },
        display: true
    }));

    return annotations;
      
}

function initializeChart(ctx, dates, est_hist_data, velocity_trend, required_trend, annotations) {
    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: dates,
            datasets: [
                {
                    label: 'Time Remaining',
                    data: est_hist_data,
                    borderWidth: 1,
                },
                {
                    label: 'Velocity Trend',
                    data: velocity_trend,
                    borderDash: [5, 5],
                    borderWidth: 1,
                    pointStyle: false,
                    type: 'line'
                },
                {
                    label: 'Required Trend',
                    data: required_trend,
                    borderDash: [5, 5],
                    borderWidth: 1,
                    pointStyle: false,
                    type: 'line'
                }
            ]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                annotation: {
                    annotations: annotations
                }
            }
        }
    });
}

function updateAnnotations(taskAnnotations, eventAnnotations, chart) {
taskAnnotations.forEach((annotation, index) => {
    const checkbox = document.getElementById(`task-checkbox-${index}`);
    annotation.display = checkbox.checked;
});
eventAnnotations.forEach((annotation, index) => {
    const checkbox = document.getElementById(`event-checkbox-${index}`);
    annotation.display = checkbox.checked;
});
chart.update();
}

function createCheckboxes(container, data, type, updateAnnotations) {
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


Promise.all([fetchEstimateHistoryData(), fetchTaskJson(), fetchEventJson()])
  .then(([estimateHistoryData, tasksData, eventData]) => {

    // EstimateHistory data
    est_hist_data = fillEstHistData(estimateHistoryData)

    // Velocity Trend
    let maxElement = est_hist_data.reduce((max, current) => current.y > max.y ? current : max, est_hist_data[0]);
    eh_n_days = daysUntilZero(maxElement.x, est_hist_data[est_hist_data.length-1].x, maxElement.y, est_hist_data[est_hist_data.length-1].y)
    velocity_trend = drawLine(maxElement.y, maxElement.x, eh_n_days)

    if (velocity_trend.length > 0) {
        document.getElementById("done-by").innerText = `Done-by Estimate: ${velocity_trend[velocity_trend.length - 1].x}`;
    } else {
        document.getElementById("done-by").innerText = 'Done-by Estimate: N/A';
    }
    
    // Date range
    const estimateDates = estimateHistoryData.map(item => new Date(item.date)); // TODO get smallest and largest
    const taskEndDates = tasksData.map(item => new Date(item.end_date));
    const eventEndDates = eventData.map(item => new Date(item.end_date));
    const velocityEndDate = velocity_trend.map(item => new Date(item.x)) // TODO get largest

    const allDates = [...estimateDates, ...taskEndDates, ...eventEndDates, ...velocityEndDate];

    const min = new Date(Math.min(...estimateDates));
    const max = new Date(Math.max(...allDates));
    const dates = generateDateRange(min, max);


    //Annotations
    taskAnnotations = annotate(tasksData, 'red')
    eventAnnotations = annotate(eventData, 'yellow')
    todayAnnotation = annotate([{'end_date' : formatDate(new Date()), 'title' : 'Today'}], color = 'blue')
    const annotations = [...taskAnnotations, ...eventAnnotations, ...todayAnnotation];

    required_trend = {}
    
    const ctx = document.getElementById('myChart');
    const chart = initializeChart(ctx, dates, est_hist_data, velocity_trend, required_trend, annotations);

    const checkboxContainer = document.getElementById('task-checkboxes');
    createCheckboxes(checkboxContainer, tasksData, 'task', () => updateAnnotations(taskAnnotations, eventAnnotations, chart));

    const eventCheckboxContainer = document.getElementById('event-checkboxes');
    createCheckboxes(eventCheckboxContainer, eventData, 'event', () => updateAnnotations(taskAnnotations, eventAnnotations, chart));
  })
  .catch(error => {
    console.error('Error fetching data:', error);
  });

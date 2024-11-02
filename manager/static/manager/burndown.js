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
// par: String, ret: Number
function calculateDaysBetween(d1, d2) {
    const startDate = new Date(d1);
    const endDate = new Date(d2);
    return (endDate - startDate) / numberOfMiliseconds;
  }

// ret: num
function calculateSlope(t1, t2, daysBetween) {
    return (t2 - t1) / daysBetween;
}

// ret: Date
function formatDate(date) {
    return date.toISOString().split('T')[0];
}

// Return the number days from d1 to the day the trend reaches 0 based on t1 and t2.
// d1, d2 : String, t1, t2 : Number
// ret: number
function daysUntilZero(d1, d2, t1, t2) {
  if (d1 === d2 || t1 === t2) {
      document.getElementById("slope").innerText = `Average Velocity: N/A`;
      return 0;
  }
  const daysBetween = calculateDaysBetween(d1, d2);
  const slope = calculateSlope(t1, t2, daysBetween);
  document.getElementById("slope").innerText = `Average Velocity: ${-slope.toFixed(2)} hr/day`;
  return Math.ceil(t1 / -slope);
}

//Return a list of dates from startDate to endDate
// par: Date, ret: [String]
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
    data.forEach((entry, index) => {
        const currentDate = new Date(entry.date);
        const nextDate = index < data.length - 1 ? new Date(data[index + 1].date) : null;
        result.push({ x: entry.date, y: entry.time_remaining });
        lastKnownTimeRemaining = entry.time_remaining;
        if (nextDate) {
            let gapDate = new Date(currentDate);
            gapDate.setDate(gapDate.getDate() + 1);

            while (gapDate < nextDate) {
                result.push({ x: formatDate(gapDate), y: lastKnownTimeRemaining });
                gapDate.setDate(gapDate.getDate() + 1);
            }
        }
    });

    return result;
}

function lineAnnotation(data, color){
    const endDates = data.map(task => formatDate(new Date(task.end_date)));
    const titles = data.map(item => item.title);
    const annotations = endDates.map((endDate, index) => ({
        type: 'line',
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

function trendAnnotation(x1, x2, y1, y2) {
  return [{
      type: 'line',
      mode: 'xy',
      scaleID: 'x-axis-0',
      value: x1,
      endValue: x2,
      borderColor: 'rgba(75, 192, 192, 1)',
      borderWidth: 1,
      borderDash: [5, 5],
      xMin: x1,
      xMax: x2,
      yMin: y1,
      yMax: y2
  }];
}

function initializeChart(ctx, dates, est_hist_data, annotations) {
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
    const estHistData = fillEstHistData(estimateHistoryData);

    // Velocity Trend
    const maxElement = estHistData.reduce((max, current) => current.y > max.y ? current : max, estHistData[0]);
    const ehNDays = daysUntilZero(maxElement.x, estHistData[estHistData.length - 1].x, maxElement.y, estHistData[estHistData.length - 1].y);

    let velocityEndDate = [];
    let velocityTrend = [];

    if (ehNDays === 0) {
      document.getElementById("done-by").innerText = `Done-by Estimate: N/A`;
    } else {
      const maxDate = new Date(maxElement.x);
      maxDate.setDate(maxDate.getDate() + ehNDays);
      const ehEndDate = formatDate(maxDate);
      velocityEndDate = [new Date(ehEndDate)];
      document.getElementById("done-by").innerText = `Done-by Estimate: ${ehEndDate}`;
      velocityTrend = trendAnnotation(maxElement.x, ehEndDate, maxElement.y);
    }

    // Date range
    const estimateDates = estimateHistoryData.map(item => new Date(item.date));
    const taskEndDates = tasksData.map(item => new Date(item.end_date));
    const eventEndDates = eventData.map(item => new Date(item.end_date));

    const allDates = [...estimateDates, ...taskEndDates, ...eventEndDates, ...velocityEndDate, estimateDates[estimateDates.length - 1]];
    const minDate = new Date(estimateDates[0]);
    const maxDate = new Date(Math.max(...allDates));
    const dates = generateDateRange(minDate, maxDate);

    // Annotations
    const taskAnnotations = lineAnnotation(tasksData, 'red');
    const eventAnnotations = lineAnnotation(eventData, 'yellow');
    const todayAnnotation = lineAnnotation([{ end_date: formatDate(new Date()), title: 'Today' }], 'blue');
    const annotations = [...taskAnnotations, ...eventAnnotations, ...todayAnnotation, ...velocityTrend];

    // Chart
    const ctx = document.getElementById('myChart');
    const chart = initializeChart(ctx, dates, estHistData, annotations);

    const checkboxContainer = document.getElementById('task-checkboxes');
    createCheckboxes(checkboxContainer, tasksData, 'task', () => updateAnnotations(taskAnnotations, eventAnnotations, chart));

    const eventCheckboxContainer = document.getElementById('event-checkboxes');
    createCheckboxes(eventCheckboxContainer, eventData, 'event', () => updateAnnotations(taskAnnotations, eventAnnotations, chart));
  })
  .catch(error => {
    console.error('Error fetching data:', error);
  });

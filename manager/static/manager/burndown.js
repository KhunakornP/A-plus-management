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
    const estimateHistories = await response.json();
    return estimateHistories;
}

/**
 * Returns the number of days between two dates.
 * 
 * @function calculateDaysBetween
 * @param {Date} d1 - The start date.
 * @param {Date} d2 - The end date.
 * @returns {Number} The number of days between d1 and d2.
 */
function calculateDaysBetween(d1, d2) {
    const startDate = new Date(d1);
    const endDate = new Date(d2);
    return (endDate - startDate) / numberOfMiliseconds;
}

/**
 * Calculates the slope between two points over a given number of days.
 * 
 * @function calculateSlope
 * @param {Number} t1 - The value at the first point.
 * @param {Number} t2 - The value at the second point.
 * @param {Number} daysBetween - The number of days between the two points.
 * @returns {Number} The slope between t1 and t2.
 */
function calculateSlope(t1, t2, daysBetween) {
    if (daysBetween === 0) {
        return -t1;
    }
    return (t2 - t1) / daysBetween;
}

/**
 * Formats a date to 'YYYY-MM-DD' format.
 * 
 * @function formatDate
 * @param {Date} date - The date to format.
 * @returns {String} The formatted date.
 */
function formatDate(date) {
    return date.toLocaleDateString('en-CA').split('T')[0];
}

function getAllDates(estimateHistoryData, tasksData, eventData, velocityEndDate) {
    const estimateDates = estimateHistoryData.map(item => new Date(item.date));
    const taskEndDates = tasksData.map(item => new Date(item.end_date));
    const eventEndDates = eventData.map(item => new Date(item.end_date));
    return [...estimateDates, ...taskEndDates, ...eventEndDates, ...velocityEndDate, estimateDates[estimateDates.length - 1]];
}

/**
 * Returns a list of dates from startDate to endDate.
 * 
 * @function generateDateRange
 * @param {Date} startDate - The start date.
 * @param {Date} endDate - The end date.
 * @returns {String[]} An array of date strings in 'YYYY-MM-DD' format.
 */
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

/**
 * Fills in the estimate history data with daily entries, ensuring there are no gaps between dates.
 * 
 * @function fillEstHistData
 * @param {Object[]} data - Array of estimate history objects, each containing a date and time_remaining property.
 * @returns {Object[]} An array of objects with x (date) and y (time remaining) properties, filled in for each day.
 */
function fillEstHistData(data) {
    const result = [];
    let lastKnownTimeRemaining = null;
    const today = new Date();

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

    let lastDate = new Date(data[data.length - 1].date);
    lastDate.setDate(lastDate.getDate() + 1);

    while (lastDate <= today) {
        result.push({ x: formatDate(lastDate), y: lastKnownTimeRemaining });
        lastDate.setDate(lastDate.getDate() + 1);
    }

    return result;
}

/**
 * Creates line annotations for a chart based on provided data.
 * 
 * @function lineAnnotation
 * @param {Object[]} data - Array of objects, each containing an end_date and title property.
 * @param {String} color - The color of the annotation lines.
 * @returns {Object[]} An array of annotation objects for the chart.
 */
function lineAnnotation(data, color){
    const endDates = data.map(item => formatDate(new Date(item.end_date)));
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

/**
 * Creates a trend line annotation for a chart.
 * 
 * @function trendAnnotation
 * @param {String} x1 - The starting x-coordinate value.
 * @param {String} x2 - The ending x-coordinate value.
 * @param {Number} y1 - The starting y-coordinate value.
 * @param {Number} y2 - The ending y-coordinate value.
 * @param {String} color - The color of the trend line.
 * @returns {Object[]} An array containing a single trend line annotation object for the chart.
 */
function trendAnnotation(x1, x2, y1, y2, color) {
  return [{
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
  }];
}

function initializeChart(ctx, dates, estHistData, lineAnnotations, trendAnnotations, scaleMax) {
    const yMax = trendAnnotations[0].yMin;

    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: dates,
            datasets: [
                {
                    label: 'Time Remaining',
                    data: estHistData,
                    borderWidth: 1,
                },
            ]
        },
        options: {
            scales: {
                x: {
                    min: 0,
                    max: scaleMax,
                },
                y: {
                    beginAtZero: true,
                    max: yMax
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

function getNearestTrendData(estHistData, taskAnnotations, eventAnnotations) {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const x1 = formatDate(today);
    const estToday = estHistData.find(item => item.x === x1);
    const y1 = estToday ? estToday.y : 0;

    const checkableDates = [...taskAnnotations, ...eventAnnotations]
        .filter(annotation => annotation.display)
        .map(annotation => new Date(annotation.value))
        .sort((a, b) => a - b);

    const x2 = checkableDates.length > 0 ? formatDate(checkableDates[0]) : null;
    const y2 = 0;
    const color = 'rgba(255, 100, 100, 1)';

    return { x1, x2, y1, y2, color };
}

function updateAnnotations(taskAnnotations, eventAnnotations, chart, estHistData, velocityEndDate) {
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

    const addTrendLine = (chart, x1, x2, y1, y2) => {
        chart.options.plugins.annotation.annotations.push(
            trendAnnotation(x1, x2, y1, y2, 'rgba(255, 100, 100, 1)')[0]
        );
    };

    updateDisplayStatus(taskAnnotations, 'task');
    updateDisplayStatus(eventAnnotations, 'event');

    const { x1, x2, y1, y2 } = getNearestTrendData(estHistData, taskAnnotations, eventAnnotations);
    const trendLine = chart.options.plugins.annotation.annotations.find(annotation => 
        annotation.borderColor === 'rgba(255, 100, 100, 1)' && annotation.mode === 'xy'
    );

    if (trendLine) {
        updateTrendLine(trendLine, x2, y1, y2, velocityEndDate);
    } else if (x2) {
        addTrendLine(chart, x1, x2, y1, y2);
    }

    if (trendLine && trendLine.display) {
        const slope = calculateSlope(y1, y2, calculateDaysBetween(x1, x2));
        updateWarningEstimate(slope);
    } else {
        updateWarningEstimate(0);
    }

    chart.update();
}

function createCheckboxes(container, data, type, updateAnnotations) {
    if (data.length === 0) {
        container.innerText = `${type.charAt(0).toUpperCase() + type.slice(1)}s are on time.`;
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

/**
 * Updates the "Done-by Estimate" display based on the provided velocity end date.
 * 
 * @function updateDoneByEstimate
 * @param {Date[]} velocityEndDate - Array containing the velocity end date.
 */
function updateDoneByEstimate(velocityEndDate) {
    if (!velocityEndDate || velocityEndDate.length === 0) {
        document.getElementById("done-by").innerText = `Done-by Estimate: N/A`;
    } else {
        document.getElementById("done-by").innerText = `Done-by Estimate: ${formatDate(velocityEndDate[0])}`;
    }
}

/**
 * Updates the "Average Velocity" display based on the provided velocity slope.
 * 
 * @function updateVelocityEstimate
 * @param {Number} velocitySlope - The calculated velocity slope.
 */
function updateVelocityEstimate(velocitySlope) {
    if (velocitySlope === 0 || isNaN(velocitySlope)) {
        document.getElementById("slope").innerText = `Average Velocity: N/A`;
    } else {
        document.getElementById("slope").innerText = `Average Velocity: ${-velocitySlope.toFixed(2)} hr/day`;
    }
}

/**
 * Updates the "Required Velocity" display based on the provided velocity slope.
 * 
 * @function updateWarningEstimate
 * @param {Number} velocitySlope - The calculated velocity slope.
 */
function updateWarningEstimate(velocitySlope) {
    if (velocitySlope === 0 || isNaN(velocitySlope)) {
        document.getElementById('warning').innerText = 'Required velocity: N/A';
    } else {
        document.getElementById('warning').innerText = `Required velocity: ${-velocitySlope.toFixed(2)} hr/day`;
    }
}

function calculateVelocityTrend(estHistData) {
    const maxElement = estHistData.reduce((max, current) => current.y > max.y ? current : max, estHistData[0]);

    const d1 = maxElement.x
    const d2 = estHistData[estHistData.length - 1].x
    const t1 = maxElement.y
    const t2 = estHistData[estHistData.length - 1].y
    let ehNDays = 0;
    let velocitySlope = 0;

    if (!(d1 === d2 || t1 === t2)) {
        const daysBetween = calculateDaysBetween(d1, d2);
        velocitySlope = calculateSlope(t1, t2, daysBetween);
        ehNDays = Math.ceil(t1 / -velocitySlope);
    }
  
    if (ehNDays === 0) {
      return { velocityEndDate: [], velocityTrend: [], velocitySlope: 0};
    }

    const maxDate = new Date(maxElement.x);
    maxDate.setDate(maxDate.getDate() + ehNDays);
    const ehEndDate = formatDate(maxDate);
    const velocityEndDate = [new Date(ehEndDate)];

    velocityEndDate[0].setHours(23, 59, 59, 999)
    const velocityTrend = trendAnnotation(maxElement.x, ehEndDate, maxElement.y, 0, 'rgba(75, 192, 192, 1)');

    return { velocityEndDate, velocityTrend, velocitySlope};
}

function aggregateMonths(dates, estHistData, lineAnnotations, trendAnnotations) {
    const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    
    const getMonthYear = date => {
        const d = new Date(date);
        return `${monthNames[d.getMonth()]} ${d.getFullYear()}`;
    };

    const months = [...new Set(dates.map(date => getMonthYear(date)))];

    const estHistDataByMonth = {};
    estHistData.forEach(({ x, y }) => {
        const month = getMonthYear(x);
        if (!estHistDataByMonth[month]) estHistDataByMonth[month] = 0;
        estHistDataByMonth[month] += y;
    });
    const aggregatedEstHistData = Object.keys(estHistDataByMonth).map(month => ({ x: month, y: estHistDataByMonth[month] }));

    const aggregatedLineAnnotations = lineAnnotations.map(annotation => {
        const month = getMonthYear(annotation.value);
        return { ...annotation, value: month };
    });

    const aggregatedTrendAnnotations = trendAnnotations.map(annotation => {
        const monthValue = getMonthYear(annotation.value);
        const monthEndValue = getMonthYear(annotation.endValue);
        const monthXMin = getMonthYear(annotation.xMin);
        const monthXMax = getMonthYear(annotation.xMax);
        const yMin = aggregatedEstHistData.find(data => data.x === monthXMin)?.y || 0;
        return { ...annotation, value: monthValue, endValue: monthEndValue, xMin: monthXMin, xMax: monthXMax, yMin };
    });

    return [months, aggregatedEstHistData, aggregatedLineAnnotations, aggregatedTrendAnnotations];
}

function aggregateYears(dates, estHistData, lineAnnotations, trendAnnotations) {
    // Aggregate dates to years
    const years = [...new Set(dates.map(date => new Date(date).getFullYear().toString()))];

    // Aggregate estHistData by years
    const estHistDataByYear = {};
    estHistData.forEach(({ x, y }) => {
        const year = new Date(x).getFullYear().toString();
        if (!estHistDataByYear[year]) estHistDataByYear[year] = 0;
        estHistDataByYear[year] += y;
    });
    const aggregatedEstHistData = Object.keys(estHistDataByYear).map(year => ({ x: year, y: estHistDataByYear[year] }));

    // Aggregate lineAnnotations by years
    const aggregatedLineAnnotations = lineAnnotations.map(annotation => {
        const year = new Date(annotation.value).getFullYear().toString();
        return { ...annotation, value: year };
    });

    // Aggregate trendAnnotations by years
    const aggregatedTrendAnnotations = trendAnnotations.map(annotation => {
        const yearValue = new Date(annotation.value).getFullYear().toString();
        const yearEndValue = new Date(annotation.endValue).getFullYear().toString();
        const yearXMin = new Date(annotation.xMin).getFullYear().toString();
        const yearXMax = new Date(annotation.xMax).getFullYear().toString();
        const yMin = aggregatedEstHistData.find(data => data.x === yearXMin)?.y || 0;
        return { ...annotation, value: yearValue, endValue: yearEndValue, xMin: yearXMin, xMax: yearXMax, yMin };
    });

    return [years, aggregatedEstHistData, aggregatedLineAnnotations, aggregatedTrendAnnotations];
}


Promise.all([fetchEstimateHistoryData(), fetchTaskJson(), fetchEventJson()])
  .then(([estimateHistoryData, tasksData, eventData]) => {

    if (estimateHistoryData.length === 0 ){
        const ctx = document.getElementById('blank');
        ctx.textContent = "It seems like you haven't added any tasks. \n Add some tasks on the taskboard.";
        ctx.style.height = '500px';
        
        updateDoneByEstimate(0)
        updateVelocityEstimate(0)
        updateWarningEstimate(0)
        
        return;
    }

    // Fill estimate history data
    const estHistData = fillEstHistData(estimateHistoryData);

    // Calculate velocity trend and update done-by estimate
    const { velocityEndDate, velocityTrend, velocitySlope } = calculateVelocityTrend(estHistData);
    updateVelocityEstimate(velocitySlope);
    updateDoneByEstimate(velocityEndDate);

    const today = new Date();
    today.setHours(0, 0, 0, 0);

    // Filter tasks and evets after today or before the velocityEndDate
    const filteredTasksData = tasksData.filter(task => {
      const endDate = new Date(task.end_date);
      return endDate >= today && endDate <= velocityEndDate[0];
    });

    const filteredEventData = eventData.filter(event => {
      const endDate = new Date(event.end_date);
      return endDate >= today && endDate <= velocityEndDate[0];
    });

    // Get all relevant dates and generate date range for the chart
    const allDates = getAllDates(estimateHistoryData, filteredTasksData, filteredEventData, velocityEndDate);
    const dates = generateDateRange(new Date(estimateHistoryData[0].date), new Date(Math.max(...allDates)));

    // Create line annotations for tasks, events, and today
    const taskAnnotations = lineAnnotation(filteredTasksData, 'red');
    const eventAnnotations = lineAnnotation(filteredEventData, 'yellow');
    const todayAnnotation = lineAnnotation([{ 'end_date': formatDate(new Date()), title: 'Today' }], 'blue');

    // Calculate the nearest trend line
    const { x1, x2, y1, y2, color } = getNearestTrendData(estHistData, taskAnnotations, eventAnnotations);
    const nearestTrend = trendAnnotation(x1, x2, y1, y2, color);

    // Combine all annotations
    const lineAnnotations = [...taskAnnotations, ...eventAnnotations, ...todayAnnotation];
    const trendAnnotations = [...velocityTrend, ...nearestTrend];

    // Initialize the chart with the data and annotations
    const scaleMax = 30
    const ctx = document.getElementById('myChart');
    let chart = initializeChart(ctx, dates, estHistData, lineAnnotations, trendAnnotations, scaleMax);

    // Create checkboxes for tasks and events to update annotations dynamically
    createCheckboxes(document.getElementById('task-checkboxes'), filteredTasksData, 'task', () => updateAnnotations(taskAnnotations, eventAnnotations, chart, estHistData, velocityEndDate[0]));
    createCheckboxes(document.getElementById('event-checkboxes'), filteredEventData, 'event', () => updateAnnotations(taskAnnotations, eventAnnotations, chart, estHistData, velocityEndDate[0]));

    updateAnnotations(taskAnnotations, eventAnnotations, chart, estHistData, velocityEndDate[0])

    document.getElementById('timescaleSelector').addEventListener('change', function() {
        const timescale = this.value;
        let aggregatedData;
    
        if (timescale === 'months') {
            aggregatedData = aggregateMonths(dates, estHistData, lineAnnotations, trendAnnotations);
        } else if (timescale === 'years') {
            aggregatedData = aggregateYears(dates, estHistData, lineAnnotations, trendAnnotations);
        } else {
            aggregatedData = [dates, estHistData, lineAnnotations, trendAnnotations];
        }

        const checkboxes = document.querySelectorAll('#task-checkboxes input, #event-checkboxes input');
        checkboxes.forEach(checkbox => {
            checkbox.disabled = (timescale !== 'dates');
        });
    
        chart.destroy();
        chart = initializeChart(ctx, ...aggregatedData, scaleMax);
    });

  })
  .catch(error => {
    console.error('Error fetching data:', error);
  });

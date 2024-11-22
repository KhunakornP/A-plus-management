const taskboardID = Number(window.location.href.split('/').slice(-3)[0]);

// Back to Taskboard button
const taskboardLink = document.getElementById('taskboard-link');
taskboardLink.href = `/manager/taskboard/${taskboardID}`;

const today = new Date();
today.setHours(0, 0, 0, 0);

const scaleMax = 30;

async function fetchEstimateHistoryData(interval) {
    const response = await fetch(`/api/estimate_history/?taskboard=${taskboardID}&interval=${interval}`);
    const estimateHistories = await response.json();
    return estimateHistories;
}

async function fetchVelocityData(startDate, interval) {
    let response = await fetch(`/api/velocity/?taskboard=${taskboardID}&start=${startDate}&interval=${interval}`);
    let velocity = await response.json();
    console.log('basic', velocity)
    if (!velocity.x || !velocity.velocity) {
        response = await fetch(`/api/velocity/?taskboard=${taskboardID}&start=${startDate}&interval=${interval}&mode=average`);
        velocity = await response.json();
    }
    console.log('average', velocity)
    return velocity
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

    const daysBetween = (endDate - startDate) / numberOfMiliseconds;

    if (daysBetween === 0) {
        return -t1;
    }
    return (t2 - t1) / daysBetween;
}

function formatDate(date) {
    return date.toLocaleDateString('en-CA').split('T')[0];
}

function formatWeek(week) {
    return `${week.year}-W${String(week.week).padStart(2, '0')}`
}

function formatMonth(date) {
    const monthNames = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];
    return `${monthNames[date.getMonth()]} ${date.getFullYear()}`;
}


function getWeek(date) {
    const tempDate = new Date(date.getTime());
    tempDate.setUTCHours(0, 0, 0, 0);
    tempDate.setUTCDate(tempDate.getUTCDate() + 4 - (tempDate.getUTCDay() || 7));
    const yearStart = new Date(Date.UTC(tempDate.getUTCFullYear(), 0, 1));
    const weekNumber = Math.ceil(((tempDate - yearStart) / 86400000 + 1) / 7);
    return { year: tempDate.getUTCFullYear(), week: weekNumber };
}

function generateRange(startDate, endDate, interval) {
    const start = new Date(startDate);
    const end = new Date(endDate);
    const array = [];

    if (interval === 'day'){    
        let currentDate = start;
        while (currentDate <= end) {
            array.push(formatDate(currentDate));
            currentDate.setDate(currentDate.getDate() + 1);
        }
    } else if (interval === 'week') {            
        while (start <= end) {
            array.push(formatWeek(getWeek(start)));
            start.setUTCDate(start.getUTCDate() + 7);
        }
    } else if (interval === 'month') {
        let currentDate = start;
        while (currentDate <= end) {
            array.push(formatMonth(currentDate));
            currentDate.setMonth(currentDate.getMonth() + 1);
        }
    }

    return array;
}

function fillDates(data) {
    const previewCount = 14;
    const previewStartDate = new Date();
    previewStartDate.setDate(previewStartDate.getDate() - previewCount);
    
    let result = [];
    let nextIndex = data.findIndex(item => new Date(item.date) >= previewStartDate);
    let currentIndex = nextIndex - 1;  

    if (nextIndex === -1) {
        currentIndex = data.length -1
        nextIndex = data.length
    }
    else if (currentIndex < 0) {
        currentIndex = nextIndex;
        nextIndex = nextIndex + 1;
    } 

    for (let i = currentIndex; i < data.length; i++) {
        let currentDate = new Date(data[currentIndex].date) <= previewStartDate ? previewStartDate : new Date(data[currentIndex].date);

        let nextDate = i + 1 < data.length ? new Date(data[i + 1].date) : new Date();
        let currentTR = data.find(item => item.date === formatDate(currentDate)) ?
        data.find(item => item.date === formatDate(currentDate)).time_remaining :
        data[i].time_remaining
        
        while (currentDate <= nextDate) {
            result.push({ x: formatDate(currentDate), y: currentTR });
            currentDate.setDate(currentDate.getDate() + 1);
        }
    }
    
    return result;
}

function fillWeeks(data) {
    data.sort((a, b) => new Date(a.date) - new Date(b.date));

    const mappedData = data.map(item => {
        const { year, week } = getWeek(new Date(item.date));
        return { year, week, timeRemaining: item.time_remaining };
    });

    const result = [];
    let previousYear = null;
    let previousWeek = null;
    let previousTimeRemaining = null;

    mappedData.forEach(({ year, week, timeRemaining }) => {
        if (previousYear !== null && previousWeek !== null) {
            while (previousYear < year || previousWeek + 1 < week) {
                previousWeek += 1;
                if (previousWeek > 52) {
                    previousYear += 1;
                    previousWeek = 1;
                }
                result.push({
                    x: `${previousYear}-W${String(previousWeek).padStart(2, '0')}`,
                    y: previousTimeRemaining
                });
            }
        }
        result.push({
            x: formatWeek({ year: year, week: week }),
            y: timeRemaining
        });
        previousYear = year;
        previousWeek = week;
        previousTimeRemaining = timeRemaining;
    });

    // Fill from the last element to the current week
    if (previousYear !== null && previousWeek !== null) {
        const today = new Date();
        const { year: currentYear, week: currentWeek } = getWeek(today);

        while (previousYear < currentYear || previousWeek < currentWeek) {
            previousWeek += 1;
            if (previousWeek > 52) {
                previousYear += 1;
                previousWeek = 1;
            }
            result.push({
                x: `${previousYear}-W${String(previousWeek).padStart(2, '0')}`,
                y: previousTimeRemaining
            });
        }
    }

    return result;
}

function fillMonths(data) {
    data.sort((a, b) => new Date(a.date) - new Date(b.date));

    const mappedData = data.map(item => {
        const date = new Date(item.date);
        return { x: formatMonth(date), y: item.time_remaining };
    });

    const result = [];
    for (let i = 0; i < mappedData.length; i++) {
        const current = mappedData[i];
        result.push(current);

        if (i < mappedData.length - 1) {
            const next = mappedData[i + 1];
            let currentDate = new Date(current.x);
            const nextDate = new Date(next.x);

            while (
                currentDate.getFullYear() < nextDate.getFullYear() ||
                (currentDate.getFullYear() === nextDate.getFullYear() &&
                    currentDate.getMonth() + 1 < nextDate.getMonth())
            ) {
                currentDate.setMonth(currentDate.getMonth() + 1);
                result.push({
                    x: formatMonth(currentDate),
                    y: current.y,
                });
            }
        }
    }

    // Fill until the current month if needed
    const lastElement = result[result.length - 1];
    const lastDate = new Date(lastElement.x);
    const currentDate = new Date();

    while (
        lastDate.getFullYear() < currentDate.getFullYear() ||
        (lastDate.getFullYear() === currentDate.getFullYear() &&
            lastDate.getMonth() < currentDate.getMonth())
    ) {
        lastDate.setMonth(lastDate.getMonth() + 1);
        result.push({
            x: formatMonth(lastDate),
            y: lastElement.y,
        });
    }

    return result;
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

function createLineAnnotations(data, color, interval) {
    let endDates = []
    let titles = []

    if (interval === 'day') {
        endDates = data.map(item => formatDate(new Date(item.end_date)));
    } else if (interval === 'week') {
        endDates = data.map(item => { return formatWeek(getWeek(new Date(item.end_date))); });
    } else if (interval === 'month') {
        endDates = data.map(item => formatMonth(new Date(item.end_date)));
    }
    titles = data.map(item => item.title);  

    const annotations = endDates.map((endDate, index) => 
        lineAnnotation(endDate, titles[index], color)
    );

    return annotations;
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

function initializeChart(ctx, range, displayData, lineAnnotations, trendAnnotations, scaleMax) {

    const chartStartDate = lineAnnotations[lineAnnotations.length - 1].value;

    const startIndex = range.indexOf(chartStartDate);
    const adjustedStartIndex = startIndex <= 14 ? 0 : startIndex - 14;
    const endIndex = startIndex + scaleMax;

    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: range,
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
                    min: range[adjustedStartIndex],
                    max: range[endIndex],
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

function updateAnnotations(taskAnnotations, eventAnnotations, chart, displayData) {
    const updateDisplayStatus = (annotations, type) => {
        annotations.forEach((annotation, index) => {
            const checkbox = document.getElementById(`${type}-checkbox-${index}`);
            annotation.display = checkbox.checked;
        });
    };

    const updateTrendLine = (trendLine, x2, y1, y2) => {
        if (x2 && y1 > 0) {
            trendLine.xMax = x2;
            trendLine.yMax = y2;
            trendLine.display = true;
        } else {
            trendLine.display = false;
        }
    };

    updateDisplayStatus(taskAnnotations, 'task');
    updateDisplayStatus(eventAnnotations, 'event');

    const { x1, x2, y1, y2, color } = getNearestTrendData(displayData, taskAnnotations, eventAnnotations);
    const trendLine = chart.options.plugins.annotation.annotations.find(annotation => 
        annotation.borderColor === color && annotation.mode === 'xy'
    );
    
    if (trendLine !== undefined) { updateTrendLine(trendLine, x2, y1, y2) }

    if (trendLine && trendLine.display) {
        const slope = calculateSlope(x1, x2, y1, y2);
        updateWarningEstimate(slope);
    } else {
        updateWarningEstimate(0);
    }

    chart.update();
}

function updateDoneByEstimate(velocityEndDate, interval) {
    if (!velocityEndDate || velocityEndDate.length === 0) {
        document.getElementById("done-by").innerText = `Done-by Estimate: N/A`;
    } else {
        let formattedDate;
        if (interval === 'day') {
            formattedDate = velocityEndDate;
        } else if (interval === 'week') {
            formattedDate = formatWeek(getWeek(new Date(velocityEndDate)));
        } else if (interval === 'month') {
            formattedDate = formatMonth(new Date(velocityEndDate));
        }
        document.getElementById("done-by").innerText = `Done-by Estimate: ${formattedDate}`;
    }
}

function updateVelocityEstimate(velocitySlope, interval) {
    if (velocitySlope === 0 || isNaN(velocitySlope)) {
        document.getElementById("slope").innerText = `Average Velocity: N/A`;
    } else {
        document.getElementById("slope").innerText = `Average Velocity: ${velocitySlope.toFixed(2)} hr/${interval}`;
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
    // Get EstimateHistory data
    const dayEstHistData = await fetchEstimateHistoryData('day');
    if (dayEstHistData.length === 0) {
        const ctx = document.getElementById('no-data');
        ctx.innerHTML = `It seems like you haven't added any tasks. Add some tasks on the taskboard.`;
        ctx.style.height = '220px';
        ctx.style.textAlign = 'center';

        updateDoneByEstimate(0);
        updateVelocityEstimate(0);
        updateWarningEstimate(0);

        return;
    }
    const weekEstHistData = await fetchEstimateHistoryData('week');
    const monthEstHistData = await fetchEstimateHistoryData('month');
    console.log(dayEstHistData)

    // Get data that will be displayed on the chart
    const dayDisplayData = fillDates(dayEstHistData);
    const weekDisplayData = fillWeeks(weekEstHistData);
    const monthDisplayData = fillMonths(monthEstHistData)

    // Get velocity data
    const dayVelocity = await fetchVelocityData(dayEstHistData[0].date, 'day')
    const weekVelocity = await fetchVelocityData(weekEstHistData[0].date,  'week')
    const monthVelocity = await fetchVelocityData(monthEstHistData[0].date, 'month')

    // Generate the x axis for the chart
    const dayRange = generateRange(dayEstHistData[0].date, dayVelocity.x, 'day')
    const weekRange = generateRange(dayEstHistData[0].date, weekVelocity.x, 'week')
    const monthRange = generateRange(dayEstHistData[0].date, monthVelocity.x, 'month')


        // Get tasks and evets after today and before the velocityEndDate and annoEndDate
        const velocityEndDate = new Date(dayVelocity.x)
        velocityEndDate.setHours(23, 59, 59, 999)

        const annoMaxDate = new Date(dayDisplayData[0].x);
        annoMaxDate.setDate(annoMaxDate.getDate() + scaleMax);
        let annoEndDate;
        let tasks;
        let events;
        if (!isNaN(velocityEndDate.getTime())){
            annoEndDate = velocityEndDate < annoMaxDate ? velocityEndDate : annoMaxDate; // TODO fix this all tasks and events will appear
            tasks = await fetchTaskData(today, annoEndDate)
            events = await fetchEventData(today, annoEndDate)
        } else {
            tasks = [];
            events = [];
        }




    // Create line annotations for tasks, events, and today
    const dayTaskAnnotations = createLineAnnotations(tasks, 'red', 'day');
    const weekTaskAnnotations = createLineAnnotations(tasks, 'red', 'week');
    const monthTaskAnnotations = createLineAnnotations(tasks, 'red', 'month');

    const dayEventAnnotations = createLineAnnotations(events, 'yellow', 'day');
    const weekEventAnnotations = createLineAnnotations(events, 'yellow', 'week');
    const monthEventAnnotations = createLineAnnotations(events, 'red', 'month');

    const dayTodayAnnotation = lineAnnotation(formatDate(today), 'Today', 'blue');
    const weekTodayAnnotation = lineAnnotation(formatWeek(getWeek(today)), 'Today', 'blue');
    const monthTodayAnnotation = lineAnnotation(formatMonth(today), 'Today', 'blue');


        // Calculate the nearest trend line
        const { x1, x2, y1, y2, color } = getNearestTrendData(dayDisplayData, dayTaskAnnotations, dayEventAnnotations);
        const nearestTrend = trendAnnotation(x1, x2, y1, y2, color);


    const dayVelocityTrend = trendAnnotation(dayDisplayData[0].x, dayVelocity.x, dayDisplayData[0].y, 0, 'rgba(75, 192, 192, 1)')
    const weekVelocityTrend = trendAnnotation(weekDisplayData[0].x, formatWeek(getWeek(new Date(weekVelocity.x))), weekDisplayData[0].y, 0, 'rgba(75, 192, 192, 1)')
    const monthVelocityTrend = trendAnnotation(monthDisplayData[0].x, formatMonth(new Date(monthVelocity.x)), monthDisplayData[0].y, 0, 'rgba(75, 192, 192, 1)')

    const dayLineAnnotations = [...dayTaskAnnotations, ...dayEventAnnotations, dayTodayAnnotation];
    const weekLineAnnotations = [...weekTaskAnnotations, ...weekEventAnnotations, weekTodayAnnotation];
    const monthLineAnnotations = [...monthTaskAnnotations, ...monthEventAnnotations, monthTodayAnnotation];

    let dayTrendAnnotations = []
    let weekTrendAnnotations = []
    let monthTrendAnnotations = []
    if (dayVelocity.x !== '' && dayVelocity.velocity !== 0) {
        dayTrendAnnotations = [dayVelocityTrend, nearestTrend];
    }
    if (weekVelocity.x !== '' && weekVelocity.velocity !== 0) {
        weekTrendAnnotations = [weekVelocityTrend, {}];
    }
    if (monthVelocity.x !== '' && monthVelocity.velocity !== 0) {
        monthTrendAnnotations = [monthVelocityTrend, {}];
    }

    if (!dayVelocity.x || !dayVelocity.velocity) {
        const element = document.getElementById('not-enough-data');
        element.textContent = "Not enough data to estimate velocity.";
        element.style.color = 'yellow';
    }

    updateVelocityEstimate(dayVelocity.velocity, 'day');
    updateDoneByEstimate(dayVelocity.x, 'day');

    const ctx = document.getElementById('myChart');
    let chart = initializeChart(ctx, dayRange, dayDisplayData, dayLineAnnotations, dayTrendAnnotations, scaleMax);

    // Create checkboxes for tasks and events to update annotations dynamically
    createCheckboxes(document.getElementById('task-checkboxes'), tasks, 'task', () => updateAnnotations(dayTaskAnnotations, dayEventAnnotations, chart, dayDisplayData));
    createCheckboxes(document.getElementById('event-checkboxes'), events, 'event', () => updateAnnotations(dayTaskAnnotations, dayEventAnnotations, chart, dayDisplayData));
    updateAnnotations(dayTaskAnnotations, dayEventAnnotations, chart, dayDisplayData, new Date(dayVelocity.x).setHours(23, 59, 59, 999));

    document.getElementById('timescaleSelector').addEventListener('change', function() {
        const timescale = this.value;
        const element = document.getElementById('not-enough-data');

        chart.destroy();

        if (timescale === 'week') {

            if (!weekVelocity.x || !weekVelocity.velocity) {
                element.textContent = "Not enough data to estimate velocity.";
                element.style.color = 'yellow';
            } else {
                element.textContent = "";
            }
            
            updateVelocityEstimate(weekVelocity.velocity, timescale);
            updateDoneByEstimate(weekVelocity.x, timescale);

            chart = initializeChart(ctx, weekRange, weekDisplayData, weekLineAnnotations, weekTrendAnnotations, scaleMax)
            updateWarningEstimate(0)

        } else if (timescale === 'month') {

            if (!monthVelocity.x || !monthVelocity.velocity) {
                const element = document.getElementById('not-enough-data');
                element.textContent = "Not enough data to estimate velocity.";
                element.style.color = 'yellow';
            } else {
                element.textContent = "";
            }
            
            updateVelocityEstimate(monthVelocity.velocity, timescale);
            updateDoneByEstimate(monthVelocity.x, timescale);

            chart = initializeChart(ctx, monthRange, monthDisplayData, monthLineAnnotations, monthTrendAnnotations, scaleMax)
            updateWarningEstimate(0)

        } else {

            if (!dayVelocity.x || !dayVelocity.velocity) {
                const element = document.getElementById('not-enough-data');
                element.textContent = "Not enough data to estimate velocity.";
                element.style.color = 'yellow';
            } else {
                element.textContent = "";
            }

            updateVelocityEstimate(dayVelocity.velocity, timescale);
            updateDoneByEstimate(dayVelocity.x, timescale);

            chart = initializeChart(ctx, dayRange, dayDisplayData, dayLineAnnotations, dayTrendAnnotations, scaleMax);

            updateAnnotations(dayTaskAnnotations, dayEventAnnotations, chart, dayDisplayData);
        }

        const checkboxes = document.querySelectorAll('#task-checkboxes input, #event-checkboxes input');
        checkboxes.forEach(checkbox => {
            checkbox.disabled = (timescale !== 'day');
        });
        let length = chart.config.options.plugins.annotation.annotations.length
        let annotation = chart.options.plugins.annotation.annotations[length - 1];
        annotation.display = (timescale === 'day');
        chart.update();
    });

}

main();
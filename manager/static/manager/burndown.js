const taskboardID = Number(window.location.href.split('/').slice(-3)[0]);

const taskboardLink = document.getElementById('taskboard-link');
taskboardLink.href = `/manager/taskboard/${taskboardID}`;

async function fetchTaskJson(){
  const response = await fetch(`/api/tasks/?taskboard=${taskboardID}`)
  const tasks = await response.json()
  return tasks
}

async function fetchEventJson(){
  const response = await fetch(`/api/events/`)
  const events = await response.json()
  return events
}

async function fetchEstimateHistoryData() {
  const response = await fetch(`/api/estimate_history/?taskboard=${taskboardID}`);
  const estimate_histories = await response.json();
  return estimate_histories;
}

// Return the number of days between d1 and d2
function calculateDaysBetween(d1, d2) {
  const startDate = new Date(d1);
  const endDate = new Date(d2);
  return (endDate - startDate) / (1000 * 60 * 60 * 24);
}

function calculateSlope(t1, t2, daysBetween) {
  return (t2 - t1) / daysBetween;
}

// Return a list of dates starting from startDate plus number of days
function generateDateRange(startDate, nDays) {
  const result = [];
  for (let i = 0; i <= Math.ceil(nDays); i++) {
    const newDate = new Date(startDate);
    newDate.setDate(startDate.getDate() + i);
    result.push(newDate.toISOString().split('T')[0]);
  }
  return result;
}

// Return the list of dates from d1 to the day the trend reaches 0 based on t1 and t2.
function daysUntilZero(d1, d2, t1, t2) {
  const daysBetween = calculateDaysBetween(d1, d2);
  if (daysBetween === 0) {
    const singleDayList = [new Date(d1).toISOString().split('T')[0]];
    return singleDayList;
  }
  const slope = calculateSlope(t1, t2, daysBetween);
  document.getElementById("slope").innerText = `Average Velocity: ${-slope.toFixed(2)} hr/day`;
  const daysToZero = t1 / -slope;
  const result = generateDateRange(new Date(d1), daysToZero);
  document.getElementById("done-by").innerText = `Done-by Estimate: ${result[result.length - 1]}`;
  return result;
}

// Return a dataset where the time remaining is filled with the last known time remaining
// fill remaining dates with 0 time remaining
function fillTimeRemaining(data, total_dates) {
  const result = [];
  data.forEach((item, i) => {
    const currentDate = new Date(item.date);
    const currentTimeRemaining = item.time_remaining;
    result.push(currentTimeRemaining);
    if (i < data.length - 1) {
      const nextDate = new Date(data[i + 1].date);
      const daysDiff = (nextDate - currentDate) / (1000 * 60 * 60 * 24);
      for (let j = 1; j < daysDiff; j++) {
        result.push(currentTimeRemaining);
      }
    }
  });
  while (result.length < total_dates.length) {
    result.push(0);
  }
  return result;
}

function processEstimateHistoryData(estimateHistoryData) {
  const dates = estimateHistoryData.map(eh => eh.date);
  const timeRemaining = estimateHistoryData.map(eh => eh.time_remaining);

  const total_dates = daysUntilZero(dates[0], dates[dates.length - 1], timeRemaining[0], timeRemaining[timeRemaining.length - 1]);
  const total_time_remaining = fillTimeRemaining(estimateHistoryData, total_dates);

  let velocity_trend = [];
  if (estimateHistoryData.length > 1) {
      velocity_trend = total_time_remaining.map((_, index, array) => {
          return total_time_remaining[0] + ((total_time_remaining[total_time_remaining.length - 1] - total_time_remaining[0]) / (array.length - 1)) * index;
      });
  }

  return { total_dates, total_time_remaining, velocity_trend };
}

function processTasksData(tasksData) {
  const endDates = tasksData.map(task => new Date(task.end_date).toISOString().split('T')[0]);
  const titles = tasksData.map(task => task.title);
  const taskAnnotations = endDates.map((endDate, index) => ({
      type: 'line',
      mode: 'vertical',
      scaleID: 'x',
      value: endDate,
      borderColor: 'rgba(255, 0, 0, 0.5)',
      borderWidth: 1,
      borderDash: [5, 5],
      label: {
          content: titles[index],
          enabled: true,
          position: 'top'
      },
      display: true
  }));

  return taskAnnotations;
}

function processEventData(eventData) {
  const endDates = eventData.map(event => new Date(event.end_date).toISOString().split('T')[0]);
  const titles = eventData.map(event => event.title);
  const taskAnnotations = endDates.map((endDate, index) => ({
      type: 'line',
      mode: 'vertical',
      scaleID: 'x',
      value: endDate,
      borderColor: 'rgba(255, 255, 0, 0.5)',
      borderWidth: 1,
      borderDash: [5, 5],
      label: {
          content: titles[index],
          enabled: true,
          position: 'top'
      },
      display: true
  }));

  return taskAnnotations;
}

const todayAnnotation = {
  type: 'line',
  mode: 'vertical',
  scaleID: 'x',
  value: new Date().toISOString().split('T')[0],
  borderColor: 'rgba(0, 0, 255, 0.5)',
  borderWidth: 2,
  label: {
      content: 'Today',
      enabled: true,
      position: 'top'
  },
  display: true
};

// Initialize chart
function initializeChart(ctx, total_dates, total_time_remaining, velocity_trend, taskAnnotations, eventAnnotations) {
  return new Chart(ctx, {
      type: 'bar',
      data: {
          labels: total_dates,
          datasets: [
              {
                  label: 'Time Remaining',
                  data: total_time_remaining,
                  borderWidth: 1,
              },
              {
                  label: 'Velocity Trend',
                  data: velocity_trend,
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
                  annotations: [...taskAnnotations, ...eventAnnotations, todayAnnotation]
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

    const { total_dates, total_time_remaining, velocity_trend } = processEstimateHistoryData(estimateHistoryData);
    const taskAnnotations = processTasksData(tasksData);
    const eventAnnotations = processEventData(eventData, total_dates);

    const ctx = document.getElementById('myChart');
    const chart = initializeChart(ctx, total_dates, total_time_remaining, velocity_trend, taskAnnotations, eventAnnotations);

    const checkboxContainer = document.getElementById('task-checkboxes');
    createCheckboxes(checkboxContainer, tasksData, 'task', () => updateAnnotations(taskAnnotations, eventAnnotations, chart));

    const eventCheckboxContainer = document.getElementById('event-checkboxes');
    createCheckboxes(eventCheckboxContainer, eventData, 'event', () => updateAnnotations(taskAnnotations, eventAnnotations, chart));

  })
  .catch(error => {
    console.error('Error fetching data:', error);
  });

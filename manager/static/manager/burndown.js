const taskboardID = Number(window.location.href.split('/').slice(-3)[0]);
const taskboardLink = document.getElementById('taskboard-link');
taskboardLink.href = `/manager/taskboard/${taskboardID}`;

function calculateDaysBetween(d1, d2) {
  const startDate = new Date(d1);
  const endDate = new Date(d2);
  return (endDate - startDate) / (1000 * 60 * 60 * 24);
}

function calculateSlope(t1, t2, daysBetween) {
  return (t2 - t1) / daysBetween;
}

function generateDateRange(startDate, daysToZero) {
  const result = [];
  for (let i = 0; i <= Math.ceil(daysToZero); i++) {
    const newDate = new Date(startDate);
    newDate.setDate(startDate.getDate() + i);
    result.push(newDate.toISOString().split('T')[0]);
  }
  return result;
}

function daysUntilZero(d1, d2, t1, t2) {
  const daysBetween = calculateDaysBetween(d1, d2);
  const slope = calculateSlope(t1, t2, daysBetween);
  document.getElementById("slope").innerText = `Average Velocity: ${-slope.toFixed(2)} hr/day`;
  const daysToZero = t1 / -slope;
  const result = generateDateRange(new Date(d1), daysToZero);
  document.getElementById("done-by").innerText = `Done-by Estimate: ${result[result.length - 1]}`;
  return result;
}

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

async function fetchEventJson(){
  const response = await fetch('/api/tasks/')
  const events = await response.json()
  return events
}

async function fetchEstimateHistoryData() {
  const response = await fetch('/api/estimate_history/');
  const estimate_histories = await response.json();
  return estimate_histories;
}

Promise.all([fetchEventJson(), fetchEstimateHistoryData()])
  .then(([tasksData, estimateHistoryData]) => {

    // Process tasksData
    const endDates = tasksData.map(task => {
      const date = new Date(task.end_date);
      return date.toISOString().split('T')[0];
    });
    const titles = tasksData.map(task => task.title);

    // Process estimateHistoryData
    const dates = estimateHistoryData.map(eh => eh.date);
    const timeRemaining = estimateHistoryData.map(eh => eh.time_remaining);

    const total_dates = daysUntilZero(dates[0], dates[dates.length - 1], timeRemaining[0], timeRemaining[timeRemaining.length - 1]);
    const total_time_remaining = fillTimeRemaining(estimateHistoryData, total_dates);

    const velocity_trend = total_time_remaining.map((_, index, array) => {
      return total_time_remaining[0] + ((total_time_remaining[total_time_remaining.length - 1] - total_time_remaining[0]) / (array.length - 1)) * index;
    });

    const annotations = endDates.map((endDate, index) => ({
      type: 'line',
      mode: 'vertical',
      scaleID: 'x',
      value: endDate,
      borderColor: 'red',
      borderWidth: 1,
      label: {
        content: titles[index],
        enabled: true,
        position: 'top'
      }
    }));

    const ctx = document.getElementById('myChart');
    new Chart(ctx, {
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
            borderWidth: 1,
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
  })
  .catch(error => {
    console.error('Error fetching data:', error);
  });

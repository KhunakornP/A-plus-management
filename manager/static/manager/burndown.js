const taskboardId = document.querySelector('.row[data-taskboard-id]').dataset.taskboardId;

const url = `/manager/taskboard/${taskboardId}/burndown/data/`;

function daysUntilZero(d1, d2, t1, t2) {
  const startDate = new Date(d1);
  const endDate = new Date(d2);
  const daysBetween = (endDate - startDate) / (1000 * 60 * 60 * 24);
  const slope = (t2 - t1) / daysBetween;
  document.getElementById("slope").innerText = `Average Velocity: ${-slope} hr/day`;
  const daysToZero = t1 / -slope;
  const result = [];
  for (let i = 0; i <= Math.ceil(daysToZero); i++) {
    const newDate = new Date(startDate);
    newDate.setDate(startDate.getDate() + i);
    result.push(newDate.toISOString().split('T')[0]);
  }
  document.getElementById("done-by").innerText = `Done-by Estimate: ${result[result.length-1]}`;
  return result;
}

function fillTimeRemaining(data, total_dates) {
  const result = [];
  for (let i = 0; i < data.length; i++) {
    const currentDate = new Date(data[i].date);
    const currentTimeRemaining = data[i].time_remaining;
    result.push(currentTimeRemaining);
    if (i < data.length - 1) {
      const nextDate = new Date(data[i + 1].date);
      const daysDiff = (nextDate - currentDate) / (1000 * 60 * 60 * 24);
      for (let j = 1; j < daysDiff; j++) {
          result.push(currentTimeRemaining);
      }
    }
  }
  while (result.length < total_dates.length) {
      result.push(0);
  }
  return result;
}

fetch(url)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
    const date = data.map(item => item.date);
    const firstD = date[0];
    const lastD = date[date.length - 1];

    const time_remaining = data.map(item => item.time_remaining);
    const firstTR = time_remaining[0];
    const lastTR = time_remaining[time_remaining.length - 1];

    const total_dates = daysUntilZero(firstD, lastD, firstTR, lastTR)
    const total_time_remaining = fillTimeRemaining(data, total_dates);

    const firstTTR = total_time_remaining[0];
    const lastTTR = total_time_remaining[total_time_remaining.length - 1];
    const velocity_trend = total_time_remaining.map((_, index, array) => {
      return firstTTR + ((lastTTR - firstTTR) / (array.length - 1)) * index;
    });

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
        }
      }
      });
    })
    .catch(error => {
        console.error('Error fetching burndown data:', error);
    });
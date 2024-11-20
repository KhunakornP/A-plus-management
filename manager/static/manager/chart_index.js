const SEVEN_DAYS = 7 * 24 * 60 * 60 * 1000
const userID = JSON.parse(document.getElementById('user_id').textContent)
const response = await fetch(`/api/tasks/?user=${userID}`);
const tasks = await response.json();
const today = new Date();
const prevWeek = new Date(today.getTime() - SEVEN_DAYS).toISOString().slice(0, 10);
const todayString = today.toISOString();
const toDoCount = tasks.filter((task) => task.status === 'TODO').length;
const inProgressCount = tasks.filter((task) => task.status === 'IN PROGRESS').length;
const doneCount = tasks.filter((task) => task.status === 'DONE').length;
const lateCount = tasks.filter((task) => task.end_date <= todayString && task.status !== 'DONE').length;

async function fetchRecentVelocity(taskboardID) {
    const response = await fetch(`/api/velocity/?taskboard=${taskboardID}&start=${prevWeek}&mode=average`);
    const Velocity = await response.json();
    return Velocity
}

const taskboardVelocities = document.querySelectorAll('[id^="tb-"]');
for (let i = 0; i < taskboardVelocities.length; i++) {
    let velocity = await fetchRecentVelocity(taskboardVelocities[i].id.split('-').slice(-1)[0])
    if (velocity > 0){
    taskboardVelocities[i].innerHTML = `<div>Recent velocity: ${velocity}</div>`;
    } else {
    taskboardVelocities[i].innerHTML = `<div>Recent velocity: 0</div>`;
    }
}


const ctx = document.getElementById('overview-chart');

const data = [{
    data: [toDoCount, doneCount, lateCount, inProgressCount],
    backgroundColor: [
        "#228B22",
        "#5f255f",
        "#d21243",
        "#B27200"
    ],
    borderColor: "#fff"
}];

const options = {
    responsive: true,
    maintainAspectRatio: false,
    tooltips: {
        enabled: false
    },
    plugins: {
        legend: {
           onClick: null
        },
        datalabels: {
            formatter: (value, ctx) => {
                const datapoints = ctx.chart.data.datasets[0].data
                const total = datapoints.reduce((total, datapoint) => total + datapoint, 0)
                const percentage = value / total * 100
                if (percentage > 0){
                return percentage.toFixed(2) + "%";
                } else {
                return ''
                }
            },
            color: '#fff',
        }
    }
};

const myChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: ['TODO', 'Finished', 'Late', 'In Progress'],
        datasets: data
    },
    options: options,
    plugins: [ChartDataLabels],
});
const userID = JSON.parse(document.getElementById('user_id').textContent)
const response = await fetch(`/api/tasks/?user=${userID}`);
const tasks = await response.json();
const today = new Date();
const todayString = today.toISOString();
const toDoCount = tasks.filter((task) => task.status === 'TODO').length;
const inProgressCount = tasks.filter((task) => task.status === 'IN PROGRESS').length;
const doneCount = tasks.filter((task) => task.status === 'DONE').length;
const lateCount = tasks.filter((task) => task.end_date <= todayString).length;



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
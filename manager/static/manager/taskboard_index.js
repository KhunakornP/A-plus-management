async function fetchTaskboardJSON() {
  const response = await fetch('/manager/api/taskboard/');
  const taskboards = await response.json();
  return taskboards;
}

fetchTaskboardJSON().then(x => {
  console.log(x)
})

function formatLocalISO(dateUTC) {
  // formats UTC time to local time
  const dateTime = new Date(dateUTC);
  const timeZoneOffSet = dateTime.getTimezoneOffset() * 60 * 1000;
  let dateTimeLocal = dateTime - timeZoneOffSet;
  dateTimeLocal = new Date(dateTimeLocal);
  let iso = dateTimeLocal.toISOString();
  iso = iso.split('.')[0];
  iso = iso.replace('T', ' ');
  return iso;
}

function getValidDateISOString(dateLocalStr) {
  // formats local time to UTC time.
  // returns ISO string of that date, today midnight if no values are provided
  if (dateLocalStr !== '') {
    return new Date(dateLocalStr).toISOString();
  }
  let defaultDate = new Date();
  defaultDate.setHours(0, 0, 0, 0);
  defaultDate.setDate(defaultDate.getDate() + 1);
  return defaultDate.toISOString();
}

function getValidEstimatedTime(time) {
  if (time === '') {
    return 0;
  }
  return Number(time);
}

async function processAndAppend(children, parent, func) {
  if (parent !== null) {
    for (const child of children) {
      parent.appendChild(func(child));
    }
  }
}

function toggleInputFields(toggleables, on) {
  if (on) {
    for (const toggleable of toggleables) {
      toggleable.removeAttribute('readonly');
      toggleable.classList.remove('form-control-plaintext');
      toggleable.classList.add('form-control');
    }
  } else {
    for (const toggleable of toggleables) {
      toggleable.setAttribute('readonly', true);
      toggleable.classList.remove('form-control');
      toggleable.classList.add('form-control-plaintext');
    }
  }
}

export {
  formatLocalISO,
  getValidDateISOString,
  getValidEstimatedTime,
  processAndAppend,
  toggleInputFields
};

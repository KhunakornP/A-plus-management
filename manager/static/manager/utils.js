const MINUTE_TO_MILLISECOND = 60 * 1000;
const MILLISECOND_TO_DAY = 1 / (1000 * 60 * 60 * 24);

function formatLocalISO(dateUTC) {
  // formats UTC time to local time
  const dateTime = new Date(dateUTC);
  const timeZoneOffSet = dateTime.getTimezoneOffset() * MINUTE_TO_MILLISECOND;
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

function getTimeDiff(dateStr) {
  const dueDate = new Date(formatLocalISO(dateStr));
  const today = new Date();
  const timeDiff = (dueDate - today) * MILLISECOND_TO_DAY;
  return timeDiff;
}

function taskNearDueDate(dateStr) {
  const timeDiff = getTimeDiff(dateStr);
  if (0 < timeDiff && timeDiff <= 3) {
    return true;
  }
  return false;
}

function taskPassedDueDate(dateStr) {
  const timeDiff = getTimeDiff(dateStr);
  if (0 >= timeDiff) {
    return true;
  }
  return false;
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
  toggleInputFields,
  taskNearDueDate,
  taskPassedDueDate,
};

function formatLocalISOFromString(dateUTCString) {
  console.log(dateUTCString)
  const dateTime = new Date(dateUTCString);
  const timeZoneOffSet = dateTime.getTimezoneOffset() * 60 * 1000;
  let dateTimeLocal = dateTime - timeZoneOffSet;
  dateTimeLocal = new Date(dateTimeLocal);
  let iso = dateTimeLocal.toISOString();
  iso = iso.split('.')[0];
  iso = iso.replace('T', ' ');
  return iso;
}

export {formatLocalISOFromString}
import { formatLocalISO, getValidDateISOString, getValidEstimatedTime } from '../utils.js'

describe('formatLocalISO', () => {
  it('Can convert UTC time to Local time from string', () =>{
    const utcTime = '2024-10-15T02:00:00.000000Z';
    const formattedTime = formatLocalISO(utcTime);
    expect(new Date(formattedTime)).toEqual(new Date(utcTime));
  })
  
  it('Can convert UTC time to Local time from Date object', () =>{
    const utcTime = new Date('2024-10-15T02:00:00.000000Z');
    const formattedTime = formatLocalISO(utcTime);
    expect(new Date(formattedTime)).toEqual(utcTime);
  })
})

describe('getValidEstimatedTime', () => {
  it('return 0 if the input is an empty string', () => {
    expect(getValidEstimatedTime('')).toEqual(0);
  });
  it('return a Number object if input a string number', () => {
    expect(getValidEstimatedTime('3')).toEqual(3);
  });
});

describe('getValidDateISOString', () => {
  it('return a valid ISO string from date object', () => {
    const date = new Date()
    expect(getValidDateISOString(date)).toEqual(date.toISOString())
  })
  it('returns today midnight if an empty string is provided', () => {
    const answer = getValidDateISOString("");
    const today_midnight = new Date()
    today_midnight.setDate(today_midnight.getDate() + 1)
    today_midnight.setHours(0,0,0,0)
    expect(answer).toEqual(today_midnight.toISOString())
  })
})

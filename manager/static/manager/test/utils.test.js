import {
  formatLocalISO,
  getValidDateISOString,
  getValidEstimatedTime,
  taskNearDueDate,
  taskPassedDueDate,
} from '../utils.js';

describe('formatLocalISO', () => {
  it('Can convert UTC time to Local time from string', () => {
    const utcTime = '2024-10-15T02:00:00.000000Z';
    const formattedTime = formatLocalISO(utcTime);
    expect(new Date(formattedTime)).toEqual(new Date(utcTime));
  });

  it('Can convert UTC time to Local time from Date object', () => {
    const utcTime = new Date('2024-10-15T02:00:00.000000Z');
    const formattedTime = formatLocalISO(utcTime);
    expect(new Date(formattedTime)).toEqual(utcTime);
  });
});

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
    const date = new Date();
    expect(getValidDateISOString(date)).toEqual(date.toISOString());
  });
  it('returns today midnight if an empty string is provided', () => {
    const answer = getValidDateISOString('');
    const todayMidnight = new Date();
    todayMidnight.setDate(todayMidnight.getDate() + 1);
    todayMidnight.setHours(0, 0, 0, 0);
    expect(answer).toEqual(todayMidnight.toISOString());
  });
});

describe('taskNearDueDate', () => {
  it('returns true if the task is within 3 days of due date', () => {
    const today = new Date();
    const dueDate = today.setDate(today.getDate() + 3);
    const answer = taskNearDueDate(dueDate);
    expect(answer).toBeTruthy();
  });
  it('returns false if the task has already passed due date', () => {
    const today = new Date();
    const dueDate = today.setDate(today.getDate() - 1);
    const answer = taskNearDueDate(dueDate);
    expect(answer).toBeFalsy();
  });
  it('returns true if the task is exactly at due date but not at due time yet', () => {
    const today = new Date();
    const dueDate = today.setSeconds(today.getSeconds() + 1);
    const answer = taskNearDueDate(dueDate);
    expect(answer).toBeTruthy();
  });
  it('returns false if the task is exactly at due time', () => {
    const today = new Date();
    const answer = taskNearDueDate(today);
    expect(answer).toBeFalsy();
  });
});

describe('taskPassedDueDate', () => {
  it('returns true if the task is exactly at due time', () => {
    const today = new Date();
    const answer = taskPassedDueDate(today);
    expect(answer).toBeTruthy();
  });
  it('returns false if the task is not at due time yet', () => {
    const today = new Date();
    const dueDate = today.setSeconds(today.getSeconds() + 1);
    const answer = taskPassedDueDate(dueDate);
    expect(answer).toBeFalsy();
  });
});

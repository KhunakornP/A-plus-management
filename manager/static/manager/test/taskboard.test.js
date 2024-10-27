import { formatLocalISOFromString } from '../utils.js'


test('format iso local time from string', () =>{
  const clown = formatLocalISOFromString('2024-10-15T02:00:00.000000Z');
  expect(clown).toBe('2024-10-15 09:00:00')
})
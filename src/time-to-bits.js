/**
 * Mi Band 9 Binary Dot Clock time model.
 * Pure JS: easy to port to a watchface expression/script engine.
 */

function toBits(value, width) {
  return Array.from({ length: width }, (_, index) =>
    (value & (1 << (width - index - 1))) !== 0 ? 1 : 0
  );
}

function getDisplayState(date = new Date(), batteryPercent = null) {
  const rawHour = date.getHours();
  const hour12 = rawHour % 12 || 12;
  const minute = date.getMinutes();
  const chargingNeeded = batteryPercent !== null && batteryPercent <= 20;

  return {
    amPm: rawHour >= 12 ? 1 : 0, // 0 = AM, 1 = PM
    chargingNeeded,
    amPmVisible: chargingNeeded ? 1 : (rawHour >= 12 ? 1 : 0),
    amPmColor: chargingNeeded ? '#FF3B30' : '#FFFFFF',
    hour12,
    minute,
    hourBits: toBits(hour12, 4),
    minuteBits: toBits(minute, 6),
    second: date.getSeconds(),
    secondProgress: date.getSeconds() / 59,
    slots: [chargingNeeded ? 1 : (rawHour >= 12 ? 1 : 0), ...toBits(hour12, 4), ...toBits(minute, 6)],
  };
}

if (typeof module !== 'undefined') module.exports = { getDisplayState, toBits };

/**
 * Mi Band 9 Binary Dot Clock time model.
 * Pure JS: easy to port to a watchface expression/script engine.
 */

function toBits(value, width) {
  return Array.from({ length: width }, (_, index) =>
    (value & (1 << (width - index - 1))) !== 0 ? 1 : 0
  );
}

function toDisplayBits(value, width) {
  // The elongated face is read from the bottom edge (right edge in the
  // corresponding horizontal/90-degree view), while the data stays MSB-first.
  return toBits(value, width).reverse();
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
    hourBits: toDisplayBits(hour12, 4),
    minuteBits: toDisplayBits(minute, 6),
    second: date.getSeconds(),
    secondProgress: date.getSeconds() / 59,
    slots: [chargingNeeded ? 1 : (rawHour >= 12 ? 1 : 0), ...toDisplayBits(hour12, 4), ...toDisplayBits(minute, 6)],
  };
}

if (typeof module !== 'undefined') module.exports = { getDisplayState, toBits, toDisplayBits };

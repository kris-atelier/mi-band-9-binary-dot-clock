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

function weatherColor(weatherType) {
  const type = String(weatherType ?? '').toLowerCase();
  if (/rain|drizzle|shower|비|소나기/.test(type)) return '#248BFF';
  if (/snow|눈/.test(type)) return '#BFE8FF';
  if (/storm|thunder|뇌우|번개/.test(type)) return '#8A5CFF';
  if (/cloud|overcast|흐림|구름/.test(type)) return '#777777';
  if (/clear|sun|맑음/.test(type)) return '#FFD43B';
  return '#FFFFFF';
}

function temperatureColor(temperature) {
  if (temperature === null || temperature === undefined || Number.isNaN(Number(temperature))) return '#FFFFFF';
  const value = Number(temperature);
  if (value <= 0) return '#248BFF';
  if (value <= 10) return '#65D9FF';
  if (value <= 20) return '#42D17A';
  if (value <= 30) return '#FFAA33';
  return '#FF4D4D';
}

function getDisplayState(date = new Date(), batteryPercent = null, weatherType = null, temperature = null) {
  const rawHour = date.getHours();
  const hour12 = rawHour % 12 || 12;
  const minute = date.getMinutes();
  const chargingNeeded = batteryPercent !== null && batteryPercent <= 20;
  const weatherVisible = weatherType !== null && weatherType !== undefined && weatherType !== '';

  return {
    amPm: rawHour >= 12 ? 1 : 0, // 0 = AM, 1 = PM
    chargingNeeded,
    amPmVisible: chargingNeeded ? 1 : (rawHour >= 12 ? 1 : 0),
    amPmColor: chargingNeeded ? '#FF3B30' : (weatherVisible ? weatherColor(weatherType) : '#FFFFFF'),
    weatherType,
    weatherColor: weatherColor(weatherType),
    temperature,
    temperatureColor: temperatureColor(temperature),
    hour12,
    minute,
    hourBits: toDisplayBits(hour12, 4),
    minuteBits: toDisplayBits(minute, 6),
    second: date.getSeconds(),
    secondProgress: date.getSeconds() / 59,
    slots: [chargingNeeded ? 1 : (rawHour >= 12 ? 1 : 0), ...toDisplayBits(hour12, 4), ...toDisplayBits(minute, 6)],
  };
}

if (typeof module !== 'undefined') module.exports = { getDisplayState, toBits, toDisplayBits, weatherColor, temperatureColor };

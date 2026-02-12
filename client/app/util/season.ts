import { type Season } from "../types/season";

function isSeason(value: string): value is Season {
  const match = /^(\d{4})-(\d{2})$/.exec(value);
  if (!match) return false;

  const year = Number(match[1]);
  const suffix = match[2];
  const expected = String((year + 1) % 100).padStart(2, "0");

  return year >= 1970 && suffix === expected;
}

/**
 * 文字列を Season 型に変換します.
 */
export function toSeason(value: string): Season {
  if (!isSeason(value)) {
    throw new Error("Season must be YYYY-YY where YY = (YYYY+1)%100 and YYYY >= 1970");
  }
  return value as Season;
}

export function generateSeasons(startYear = 1970, date = new Date()): Season[] {
  const currentStartYear = date.getMonth() + 1 >= 9 ? date.getFullYear() : date.getFullYear() - 1;
  return Array.from({ length: currentStartYear - startYear + 1 }, (_, i) => {
    const y = startYear + i;
    return toSeason(`${y}-${String(y + 1).slice(-2)}`);
  }).reverse();
}

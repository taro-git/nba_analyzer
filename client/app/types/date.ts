import dayjs, { type Dayjs } from "dayjs";
import timezone from "dayjs/plugin/timezone";
import utc from "dayjs/plugin/utc";

dayjs.extend(utc);
dayjs.extend(timezone);

const DAY_MS = 86400000;

/**
 * 曜日を定義します.
 */
export const Day = {
  Sun: "Sun",
  Mon: "Mon",
  Tue: "Tue",
  Wed: "Wed",
  Thu: "Thu",
  Fri: "Fri",
  Sat: "Sat",
} as const;

/**
 * 曜日を定義します.
 */
export type Day = (typeof Day)[keyof typeof Day];

/**
 * 日時を表すクラスです.
 */
export class Date {
  private _epochMs: number;

  constructor(date?: Dayjs) {
    const d = (date ?? dayjs()).startOf("day");
    this._epochMs = d.valueOf();
  }

  /**
   * タイムゾーン付き日時をセットします.
   * 時刻は 00:00:00 になります.
   */
  set date(value: Dayjs) {
    if (!value.isValid()) {
      throw new Error("Invalid date passed to setter");
    }
    this._epochMs = value.startOf("day").valueOf();
  }

  /**
   * 日数を指定し、現在保持している日時に日数×24時間を加算します.
   */
  addDays(days: number): void {
    this._epochMs += days * DAY_MS;
  }

  /**
   * 日数を指定し、現在保持している日時に日数を加算した日時の UTC ISO を返します.
   */
  getAddedUtcIso(days?: number): string {
    const d = new globalThis.Date(this._epochMs + (days ?? 0) * DAY_MS);
    return d.toISOString().replace(/\.\d{3}Z$/, "Z");
  }

  /**
   * 日数を指定し、現在保持している日時に日数を加算した日時の日付文字列を返します.
   */
  getAddedDateString(days?: number): string {
    const d = new globalThis.Date(this._epochMs + (days ?? 0) * DAY_MS);
    return `${d.getFullYear()}-${d.getMonth() + 1}-${d.getDate()}`;
  }

  /**
   * 現在保持している日時に日数を加算した日時を Dayjs インスタンスとして返します.
   */
  getAddedDayjs(days?: number): Dayjs {
    return dayjs(this._epochMs + (days ?? 0) * DAY_MS);
  }

  /**
   * 現在保持している日時に日数を加算した日時のエポック秒を返します.
   */
  getAddedEpochSec(days?: number): number {
    return Math.floor((this._epochMs + (days ?? 0) * DAY_MS) / 1000);
  }

  /**
   * 現在保持している日時に日数を加算した日時の年を返します.
   */
  getAddedYear(days?: number): number {
    return new globalThis.Date(this._epochMs + (days ?? 0) * DAY_MS).getFullYear();
  }

  /**
   * 現在保持している日時に日数を加算した日時の月を返します.
   */
  getAddedMonth(days?: number): number {
    return new globalThis.Date(this._epochMs + (days ?? 0) * DAY_MS).getMonth() + 1;
  }

  /**
   * 現在保持している日時に日数を加算した日時の日付を返します.
   */
  getAddedDate(days?: number): number {
    return new globalThis.Date(this._epochMs + (days ?? 0) * DAY_MS).getDate();
  }

  /**
   * 現在保持している日時に日数を加算した日時の曜日を返します.
   */
  getAddedDay(days?: number): Day {
    switch (new globalThis.Date(this._epochMs + (days ?? 0) * DAY_MS).getDay()) {
      case 0:
        return Day.Sun;
      case 1:
        return Day.Mon;
      case 2:
        return Day.Tue;
      case 3:
        return Day.Wed;
      case 4:
        return Day.Thu;
      case 5:
        return Day.Fri;
      default:
        return Day.Sat;
    }
  }
}

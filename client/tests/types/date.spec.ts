import dayjs from "dayjs";
import { describe, expect, it } from "vitest";

import { Date as CustomDate, Day } from "../../app/types/date";

describe("Date class", () => {
  const base = dayjs("2026-02-24T10:30:00+09:00");
  const baseStart = "2026-02-23T15:00:00Z";
  const nextDayStart = "2026-02-24T15:00:00Z";

  it("initializes with startOf day", () => {
    const d = new CustomDate(base);
    expect(d.getAddedUtcIso()).toBe(baseStart);
  });

  it("uses current date when no argument provided", () => {
    const d = new CustomDate();
    expect(typeof d.getAddedEpochSec()).toBe("number");
  });

  it("setter updates date", () => {
    const d = new CustomDate(base);

    d.date = dayjs("2026-03-01T15:00:00+09:00");

    expect(d.getAddedYear()).toBe(2026);
    expect(d.getAddedMonth()).toBe(3);
    expect(d.getAddedDate()).toBe(1);
  });

  it("setter throws for invalid date", () => {
    const d = new CustomDate(base);

    expect(() => {
      d.date = dayjs("invalid");
    }).toThrow();
  });

  it("addDays mutates internal date", () => {
    const d = new CustomDate(base);

    d.addDays(5);

    expect(d.getAddedDate()).toBe(1);
    expect(d.getAddedMonth()).toBe(3);
  });

  it("getAddedUtcIso returns correct iso", () => {
    const d = new CustomDate(base);

    expect(d.getAddedUtcIso()).toBe(baseStart);
    expect(d.getAddedUtcIso(1)).toBe(nextDayStart);
  });

  it("getAddedDateString returns correct format", () => {
    const d = new CustomDate(base);

    expect(d.getAddedDateString()).toBe("2026-2-24");
    expect(d.getAddedDateString(1)).toBe("2026-2-25");
  });

  it("getAddedDayjs returns Dayjs instance", () => {
    const d = new CustomDate(base);

    const result = d.getAddedDayjs();

    expect(dayjs.isDayjs(result)).toBe(true);
    expect(result.date()).toBe(24);
  });

  it("getAddedEpochSec returns correct epoch", () => {
    const d = new CustomDate(base);

    const epoch = d.getAddedEpochSec();

    expect(typeof epoch).toBe("number");
    expect(epoch).toBe(Math.floor(new globalThis.Date(baseStart).getTime() / 1000));
  });

  it("getAddedYear works with offset", () => {
    const d = new CustomDate(dayjs("2026-12-31"));

    expect(d.getAddedYear(1)).toBe(2027);
  });

  it("getAddedMonth works with offset", () => {
    const d = new CustomDate(dayjs("2026-01-31"));

    expect(d.getAddedMonth(1)).toBe(2);
  });

  it("getAddedDate works with offset", () => {
    const d = new CustomDate(base);

    expect(d.getAddedDate()).toBe(24);
    expect(d.getAddedDate(2)).toBe(26);
  });

  it("getAddedDay returns correct weekday", () => {
    const d = new CustomDate(dayjs("2026-02-24"));

    expect(d.getAddedDay()).toBe(Day.Tue);
    expect(d.getAddedDay(1)).toBe(Day.Wed);
    expect(d.getAddedDay(2)).toBe(Day.Thu);
  });
});

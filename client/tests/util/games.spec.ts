import { describe, expect, it } from "vitest";

import { Periods } from "../../app/types/gameDetail";
import { convertFromElapsedMsToGameClock, toPeriod } from "../../app/util/games";

describe("convertFromElapsedMsToGameClock", () => {
  const REGULATION_SECONDS = 12 * 60; // 12 minutes per quarter
  const OVERTIME_SECONDS = 5 * 60; // 5 minutes per overtime

  describe("firstQuarter", () => {
    it("returns correct clock at start of quarter", () => {
      const result = convertFromElapsedMsToGameClock(0, Periods.firstQuarter, REGULATION_SECONDS, OVERTIME_SECONDS);
      expect(result.regulation).toBe(1);
      expect(result.minutes).toBe("12");
      expect(result.seconds).toBe("00");
      expect(result.string).toBe("1Q 12:00");
    });

    it("returns correct clock in middle of quarter", () => {
      const result = convertFromElapsedMsToGameClock(
        6 * 60 * 1000,
        Periods.firstQuarter,
        REGULATION_SECONDS,
        OVERTIME_SECONDS,
      );
      expect(result.regulation).toBe(1);
      expect(result.minutes).toBe("06");
      expect(result.seconds).toBe("00");
      expect(result.string).toBe("1Q 06:00");
    });

    it("returns correct clock at end of quarter", () => {
      const result = convertFromElapsedMsToGameClock(
        12 * 60 * 1000 - 1000,
        Periods.firstQuarter,
        REGULATION_SECONDS,
        OVERTIME_SECONDS,
      );
      expect(result.regulation).toBe(1);
      expect(result.minutes).toBe("00");
      expect(result.seconds).toBe("01");
      expect(result.string).toBe("1Q 00:01");
    });
  });

  describe("secondQuarter", () => {
    it("returns correct clock at start of quarter", () => {
      const result = convertFromElapsedMsToGameClock(
        12 * 60 * 1000,
        Periods.secondQuarter,
        REGULATION_SECONDS,
        OVERTIME_SECONDS,
      );
      expect(result.regulation).toBe(2);
      expect(result.minutes).toBe("12");
      expect(result.seconds).toBe("00");
      expect(result.string).toBe("2Q 12:00");
    });

    it("returns correct clock in middle of quarter", () => {
      const result = convertFromElapsedMsToGameClock(
        18 * 60 * 1000,
        Periods.secondQuarter,
        REGULATION_SECONDS,
        OVERTIME_SECONDS,
      );
      expect(result.regulation).toBe(2);
      expect(result.minutes).toBe("06");
      expect(result.seconds).toBe("00");
      expect(result.string).toBe("2Q 06:00");
    });
  });

  describe("thirdQuarter", () => {
    it("returns correct clock at start of quarter", () => {
      const result = convertFromElapsedMsToGameClock(
        24 * 60 * 1000,
        Periods.thirdQuarter,
        REGULATION_SECONDS,
        OVERTIME_SECONDS,
      );
      expect(result.regulation).toBe(3);
      expect(result.minutes).toBe("12");
      expect(result.seconds).toBe("00");
      expect(result.string).toBe("3Q 12:00");
    });

    it("returns correct clock in middle of quarter", () => {
      const result = convertFromElapsedMsToGameClock(
        30 * 60 * 1000,
        Periods.thirdQuarter,
        REGULATION_SECONDS,
        OVERTIME_SECONDS,
      );
      expect(result.regulation).toBe(3);
      expect(result.minutes).toBe("06");
      expect(result.seconds).toBe("00");
      expect(result.string).toBe("3Q 06:00");
    });
  });

  describe("fourthQuarter", () => {
    it("returns correct clock at start of quarter", () => {
      const result = convertFromElapsedMsToGameClock(
        36 * 60 * 1000,
        Periods.fourthQuarter,
        REGULATION_SECONDS,
        OVERTIME_SECONDS,
      );
      expect(result.regulation).toBe(4);
      expect(result.minutes).toBe("12");
      expect(result.seconds).toBe("00");
      expect(result.string).toBe("4Q 12:00");
    });

    it("returns correct clock in middle of quarter", () => {
      const result = convertFromElapsedMsToGameClock(
        42 * 60 * 1000,
        Periods.fourthQuarter,
        REGULATION_SECONDS,
        OVERTIME_SECONDS,
      );
      expect(result.regulation).toBe(4);
      expect(result.minutes).toBe("06");
      expect(result.seconds).toBe("00");
      expect(result.string).toBe("4Q 06:00");
    });
  });

  describe("firstHalf", () => {
    it("returns correct clock in first quarter", () => {
      const result = convertFromElapsedMsToGameClock(
        6 * 60 * 1000,
        Periods.firstHalf,
        REGULATION_SECONDS,
        OVERTIME_SECONDS,
      );
      expect(result.regulation).toBe(1);
      expect(result.minutes).toBe("06");
      expect(result.seconds).toBe("00");
      expect(result.string).toBe("1Q 06:00");
    });

    it("returns correct clock in second quarter", () => {
      const result = convertFromElapsedMsToGameClock(
        18 * 60 * 1000,
        Periods.firstHalf,
        REGULATION_SECONDS,
        OVERTIME_SECONDS,
      );
      expect(result.regulation).toBe(2);
      expect(result.minutes).toBe("06");
      expect(result.seconds).toBe("00");
      expect(result.string).toBe("2Q 06:00");
    });
  });

  describe("secondHalf", () => {
    it("returns correct clock in third quarter", () => {
      const result = convertFromElapsedMsToGameClock(
        30 * 60 * 1000,
        Periods.secondHalf,
        REGULATION_SECONDS,
        OVERTIME_SECONDS,
      );
      expect(result.regulation).toBe(3);
      expect(result.minutes).toBe("06");
      expect(result.seconds).toBe("00");
      expect(result.string).toBe("3Q 06:00");
    });

    it("returns correct clock in fourth quarter", () => {
      const result = convertFromElapsedMsToGameClock(
        42 * 60 * 1000,
        Periods.secondHalf,
        REGULATION_SECONDS,
        OVERTIME_SECONDS,
      );
      expect(result.regulation).toBe(4);
      expect(result.minutes).toBe("06");
      expect(result.seconds).toBe("00");
      expect(result.string).toBe("4Q 06:00");
    });
  });

  describe("regulation", () => {
    it("returns correct clock in first quarter", () => {
      const result = convertFromElapsedMsToGameClock(
        6 * 60 * 1000,
        Periods.regulation,
        REGULATION_SECONDS,
        OVERTIME_SECONDS,
      );
      expect(result.regulation).toBe(1);
      expect(result.minutes).toBe("06");
      expect(result.seconds).toBe("00");
      expect(result.string).toBe("1Q 06:00");
    });

    it("returns correct clock in fourth quarter", () => {
      const result = convertFromElapsedMsToGameClock(
        42 * 60 * 1000,
        Periods.regulation,
        REGULATION_SECONDS,
        OVERTIME_SECONDS,
      );
      expect(result.regulation).toBe(4);
      expect(result.minutes).toBe("06");
      expect(result.seconds).toBe("00");
      expect(result.string).toBe("4Q 06:00");
    });
  });

  describe("overTime", () => {
    it("returns correct clock in first overtime", () => {
      const result = convertFromElapsedMsToGameClock(
        48 * 60 * 1000 + 2.5 * 60 * 1000,
        Periods.overTime,
        REGULATION_SECONDS,
        OVERTIME_SECONDS,
      );
      expect(result.overTime).toBe(1);
      expect(result.minutes).toBe("02");
      expect(result.seconds).toBe("30");
      expect(result.string).toBe("1OT 02:30");
    });

    it("returns correct clock in second overtime", () => {
      const result = convertFromElapsedMsToGameClock(
        48 * 60 * 1000 + 7.5 * 60 * 1000,
        Periods.overTime,
        REGULATION_SECONDS,
        OVERTIME_SECONDS,
      );
      expect(result.overTime).toBe(2);
      expect(result.minutes).toBe("02");
      expect(result.seconds).toBe("30");
      expect(result.string).toBe("2OT 02:30");
    });

    it("returns correct clock at start of overtime", () => {
      const result = convertFromElapsedMsToGameClock(
        48 * 60 * 1000,
        Periods.overTime,
        REGULATION_SECONDS,
        OVERTIME_SECONDS,
      );
      expect(result.overTime).toBe(1);
      expect(result.minutes).toBe("05");
      expect(result.seconds).toBe("00");
      expect(result.string).toBe("1OT 05:00");
    });
  });

  describe("all", () => {
    it("returns regulation clock when in regulation time", () => {
      const result = convertFromElapsedMsToGameClock(30 * 60 * 1000, Periods.all, REGULATION_SECONDS, OVERTIME_SECONDS);
      expect(result.regulation).toBe(3);
      expect(result.minutes).toBe("06");
      expect(result.seconds).toBe("00");
      expect(result.string).toBe("3Q 06:00");
    });

    it("returns overtime clock when in overtime", () => {
      const result = convertFromElapsedMsToGameClock(
        48 * 60 * 1000 + 2.5 * 60 * 1000,
        Periods.all,
        REGULATION_SECONDS,
        OVERTIME_SECONDS,
      );
      expect(result.overTime).toBe(1);
      expect(result.minutes).toBe("02");
      expect(result.seconds).toBe("30");
      expect(result.string).toBe("1OT 02:30");
    });

    it("returns regulation clock at end of regulation", () => {
      const result = convertFromElapsedMsToGameClock(48 * 60 * 1000, Periods.all, REGULATION_SECONDS, OVERTIME_SECONDS);
      expect(result.regulation).toBe(4);
      expect(result.minutes).toBe("00");
      expect(result.seconds).toBe("00");
      expect(result.string).toBe("4Q 00:00");
    });
  });
});

describe("toPeriod", () => {
  it("returns valid period as-is", () => {
    expect(toPeriod(Periods.firstQuarter)).toBe(Periods.firstQuarter);
    expect(toPeriod(Periods.secondQuarter)).toBe(Periods.secondQuarter);
    expect(toPeriod(Periods.thirdQuarter)).toBe(Periods.thirdQuarter);
    expect(toPeriod(Periods.fourthQuarter)).toBe(Periods.fourthQuarter);
    expect(toPeriod(Periods.firstHalf)).toBe(Periods.firstHalf);
    expect(toPeriod(Periods.secondHalf)).toBe(Periods.secondHalf);
    expect(toPeriod(Periods.regulation)).toBe(Periods.regulation);
    expect(toPeriod(Periods.overTime)).toBe(Periods.overTime);
    expect(toPeriod(Periods.all)).toBe(Periods.all);
  });

  it("throws for invalid period", () => {
    expect(() => toPeriod("invalid")).toThrow("Invalid period: invalid");
    expect(() => toPeriod("1Q")).toThrow();
    expect(() => toPeriod("")).toThrow();
  });
});

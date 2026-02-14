import { describe, expect, it } from "vitest";

import { generateSeasons, toSeason } from "../../app/util/season";

describe("toSeason", () => {
  describe("valid season should be returned as-is", () => {
    it("currentry season", () => {
      expect(toSeason("2023-24")).toBe("2023-24");
    });

    it("handles century boundary correctly", () => {
      expect(toSeason("1999-00")).toBe("1999-00");
    });
  });

  it("throws if format is invalid", () => {
    expect(() => toSeason("2023/24")).toThrow();
    expect(() => toSeason("23-24")).toThrow();
    expect(() => toSeason("abcd-ef")).toThrow();
  });

  it("throws if suffix does not match next year", () => {
    expect(() => toSeason("2023-25")).toThrow();
  });

  it("throws if year is less than 1970", () => {
    expect(() => toSeason("1969-70")).toThrow();
  });
});

describe("generateSeasons", () => {
  it("generates seasons from startYear to current season (after September)", () => {
    const seasons = generateSeasons(2022, new Date("2024-10-01"));
    expect(seasons).toEqual(["2024-25", "2023-24", "2022-23"]);
  });

  it("generates seasons using previous year if before September", () => {
    const seasons = generateSeasons(2022, new Date("2024-05-01"));
    expect(seasons).toEqual(["2023-24", "2022-23"]);
  });

  it("default startYear is 1970", () => {
    const seasons = generateSeasons(undefined, new Date("1971-10-01"));
    expect(seasons).toEqual(["1971-72", "1970-71"]);
  });

  it("returns empty array if startYear is greater than currentStartYear", () => {
    const seasons = generateSeasons(2030, new Date("2024-10-01"));
    expect(seasons).toEqual([]);
  });

  it("returns empty array if currentStartYear is less than 1970", () => {
    const seasons = generateSeasons(undefined, new Date("1969-10-01"));
    expect(seasons).toEqual([]);
  });
});

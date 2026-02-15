import { describe, expect, it } from "vitest";

import { RegularSeasonTeamsApi } from "../../app/api/teams.api";
import { Conferences, Divisions } from "../../app/types/leagueStructure";

class testWrapperClass extends RegularSeasonTeamsApi {
  public testResIsIRes(data: unknown): boolean {
    return this.resIsIRes(data);
  }
}

describe("RegularSeasonTeamsApi.resIsIRes", () => {
  const validTeams = [
    {
      teamId: 1,
      teamName: "Test",
      teamTricode: "TST",
      teamLogo: "",
      conference: Conferences.East,
      division: Divisions.Atlantic,
      rank: 1,
      win: 10,
      lose: 5,
    },
  ];

  it("returns true for valid IRegularSeasonTeams object", () => {
    const valid = {
      season: "2023-24",
      teams: validTeams,
    };

    expect(new testWrapperClass().testResIsIRes(valid)).toBe(true);
  });

  it("returns false for null", () => {
    expect(new testWrapperClass().testResIsIRes(null)).toBe(false);
  });

  it("returns false if season is missing", () => {
    expect(new testWrapperClass().testResIsIRes({ teams: [] })).toBe(false);
  });

  it("returns false if season is not string", () => {
    expect(new testWrapperClass().testResIsIRes({ season: 2023, teams: [] })).toBe(false);
  });

  it("returns false if season format is invalid", () => {
    expect(new testWrapperClass().testResIsIRes({ season: "2023/24", teams: [] })).toBe(false);
    expect(new testWrapperClass().testResIsIRes({ season: "23-24", teams: [] })).toBe(false);
  });

  it("returns false if season suffix does not match next year", () => {
    expect(new testWrapperClass().testResIsIRes({ season: "2023-25", teams: [] })).toBe(false);
  });

  it("returns false if season year is less than 1970", () => {
    expect(new testWrapperClass().testResIsIRes({ season: "1969-70", teams: [] })).toBe(false);
  });

  it("returns false if teams is missing", () => {
    expect(new testWrapperClass().testResIsIRes({ season: "2023-24" })).toBe(false);
  });

  it("returns false if teams is not an array", () => {
    expect(new testWrapperClass().testResIsIRes({ season: "2023-24", teams: {} })).toBe(false);
  });

  it("returns true even if teams array is empty", () => {
    expect(new testWrapperClass().testResIsIRes({ season: "2023-24", teams: [] })).toBe(true);
  });
});

import { describe, expect, it } from "vitest";

import { Conferences, Divisions } from "../../app/types/leagueStructure";
import type { RegularSeasonTeam } from "../../app/types/teams";
import { teamsByConference, teamsByDivision } from "../../app/util/teams";

function createTeam(overrides: Partial<RegularSeasonTeam>): RegularSeasonTeam {
  return {
    teamId: 1,
    teamName: "Test Team",
    teamTricode: "TST",
    teamLogo: "",
    conference: Conferences.East,
    division: Divisions.Atlantic,
    rank: 1,
    win: 10,
    lose: 5,
    gb: 0,
    rate: ".667",
    gp: 15,
    ...overrides,
  };
}

describe("teamsByConference", () => {
  it("groups by conference", () => {
    const teams: RegularSeasonTeam[] = [
      createTeam({ teamId: 1, conference: Conferences.East }),
      createTeam({ teamId: 2, conference: Conferences.West }),
      createTeam({ teamId: 3, conference: Conferences.East }),
      createTeam({ teamId: 4, conference: Conferences.West }),
    ];

    const result = teamsByConference(teams);

    expect(result[Conferences.East].map((t) => t.teamId)).toEqual([1, 3]);
    expect(result[Conferences.West].map((t) => t.teamId)).toEqual([2, 4]);
  });

  it("does not mix conferences when sorting", () => {
    const teams: RegularSeasonTeam[] = [
      createTeam({ teamId: 1, conference: Conferences.East, rank: 3 }),
      createTeam({ teamId: 2, conference: Conferences.East, rank: 1 }),
      createTeam({ teamId: 3, conference: Conferences.East, rank: 2 }),
      createTeam({ teamId: 4, conference: Conferences.East, rank: 4 }),
    ];

    const result = teamsByConference(teams);

    expect(result[Conferences.East].map((t) => t.rank)).toEqual([1, 2, 3, 4]);
  });

  it("sorts teams by rank ascending within each conference", () => {
    const teams: RegularSeasonTeam[] = [
      createTeam({ teamId: 1, conference: Conferences.East, rank: 3 }),
      createTeam({ teamId: 2, conference: Conferences.East, rank: 2 }),
      createTeam({ teamId: 3, conference: Conferences.West, rank: 1 }),
      createTeam({ teamId: 4, conference: Conferences.East, rank: 1 }),
      createTeam({ teamId: 5, conference: Conferences.West, rank: 3 }),
      createTeam({ teamId: 6, conference: Conferences.West, rank: 2 }),
    ];

    const result = teamsByConference(teams);

    expect(result[Conferences.East].map((t) => t.rank)).toEqual([1, 2, 3]);
    expect(result[Conferences.West].map((t) => t.rank)).toEqual([1, 2, 3]);
  });
});

describe("teamsByDivision", () => {
  it("groups teams by division", () => {
    const teams: RegularSeasonTeam[] = [
      createTeam({ teamId: 1, division: Divisions.Atlantic }),
      createTeam({ teamId: 2, division: Divisions.Pacific }),
      createTeam({ teamId: 3, division: Divisions.Atlantic }),
      createTeam({ teamId: 4, division: Divisions.Pacific }),
    ];

    const result = teamsByDivision(teams);

    expect(result[Divisions.Atlantic].map((t) => t.teamId)).toEqual([1, 3]);
    expect(result[Divisions.Pacific].map((t) => t.teamId)).toEqual([2, 4]);
  });

  it("does not mix divisions when sorting", () => {
    const teams: RegularSeasonTeam[] = [
      createTeam({ teamId: 1, division: Divisions.Central, rank: 3 }),
      createTeam({ teamId: 2, division: Divisions.Central, rank: 1 }),
      createTeam({ teamId: 3, division: Divisions.Central, rank: 2 }),
      createTeam({ teamId: 4, division: Divisions.Central, rank: 4 }),
    ];

    const result = teamsByDivision(teams);

    expect(result[Divisions.Central].map((t) => t.rank)).toEqual([1, 2, 3, 4]);
  });

  it("sorts teams by rank ascending within each division", () => {
    const teams: RegularSeasonTeam[] = [
      createTeam({ teamId: 1, division: Divisions.Atlantic, rank: 3 }),
      createTeam({ teamId: 2, division: Divisions.Atlantic, rank: 2 }),
      createTeam({ teamId: 3, division: Divisions.Pacific, rank: 1 }),
      createTeam({ teamId: 4, division: Divisions.Atlantic, rank: 1 }),
      createTeam({ teamId: 5, division: Divisions.Pacific, rank: 3 }),
      createTeam({ teamId: 6, division: Divisions.Pacific, rank: 2 }),
    ];

    const result = teamsByDivision(teams);

    expect(result[Divisions.Atlantic].map((t) => t.rank)).toEqual([1, 2, 3]);
    expect(result[Divisions.Pacific].map((t) => t.rank)).toEqual([1, 2, 3]);
  });
});

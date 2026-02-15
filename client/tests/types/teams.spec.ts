import { describe, expect, it } from "vitest";

import { type IRegularSeasonTeams } from "../../app/api/schemas/teams";
import { Conferences, Divisions } from "../../app/types/leagueStructure";
import { RegularSeasonTeams } from "../../app/types/teams";
import { toSeason } from "../../app/util/season";

function createApiTeam(overrides: Partial<IRegularSeasonTeams["teams"][number]>) {
  return {
    teamId: 1,
    teamName: "Test",
    teamTricode: "TST",
    teamLogo: "",
    conference: Conferences.East,
    division: Divisions.Atlantic,
    rank: 1,
    win: 10,
    lose: 5,
    ...overrides,
  };
}

describe("RegularSeasonTeams", () => {
  it("sets season correctly via toSeason", () => {
    const data: IRegularSeasonTeams = {
      season: toSeason("2023-24"),
      teams: [],
    };

    const result = new RegularSeasonTeams(data);

    expect(result.season).toBe("2023-24");
    expect(result.teams.length).toBe(0);
  });

  it("calculates gb correctly within each conference", () => {
    const data: IRegularSeasonTeams = {
      season: toSeason("2023-24"),
      teams: [
        createApiTeam({ teamId: 1, conference: Conferences.East, win: 50, lose: 20 }), // best East (diff=30)
        createApiTeam({ teamId: 2, conference: Conferences.East, win: 48, lose: 22 }), // diff=26 → gb=2
        createApiTeam({ teamId: 3, conference: Conferences.West, win: 60, lose: 10 }), // best West (diff=50)
        createApiTeam({ teamId: 4, conference: Conferences.West, win: 58, lose: 12 }), // diff=46 → gb=2
      ],
    };

    const result = new RegularSeasonTeams(data);

    const eastBest = result.teams.find((t) => t.teamId === 1)!;
    const eastSecond = result.teams.find((t) => t.teamId === 2)!;
    const westBest = result.teams.find((t) => t.teamId === 3)!;
    const westSecond = result.teams.find((t) => t.teamId === 4)!;

    expect(eastBest.gb).toBe(0);
    expect(westBest.gb).toBe(0);
    expect(eastSecond.gb).toBe(2);
    expect(westSecond.gb).toBe(2);
  });

  it("calculates rate and gp correctly", () => {
    const data: IRegularSeasonTeams = {
      season: toSeason("2023-24"),
      teams: [createApiTeam({ win: 30, lose: 20 })],
    };

    const result = new RegularSeasonTeams(data);
    const team = result.teams[0];

    expect(team.gp).toBe(50);
    expect(team.rate).toBe(".600"); // 30/50 = 0.600
  });

  it("sorts by rank ascending", () => {
    const data: IRegularSeasonTeams = {
      season: toSeason("2023-24"),
      teams: [
        createApiTeam({ teamId: 1, rank: 3 }),
        createApiTeam({ teamId: 2, rank: 1 }),
        createApiTeam({ teamId: 3, rank: 2 }),
        createApiTeam({ teamId: 4, rank: 4 }),
      ],
    };

    const result = new RegularSeasonTeams(data);

    expect(result.teams.map((t) => t.rank)).toEqual([1, 2, 3, 4]);
  });

  it("if rank is equal, sorts by win percentage descending", () => {
    const data: IRegularSeasonTeams = {
      season: toSeason("2023-24"),
      teams: [
        createApiTeam({ teamId: 1, rank: 1, win: 30, lose: 20 }), // .667
        createApiTeam({ teamId: 2, rank: 1, win: 40, lose: 20 }), // .600
      ],
    };

    const result = new RegularSeasonTeams(data);

    expect(result.teams.map((t) => t.teamId)).toEqual([2, 1]);
  });

  it("returns default if data is undefined", () => {
    const result = new RegularSeasonTeams(undefined);

    expect(result.season).toBe("1970-71");
    expect(result.teams).toEqual([]);
  });
});

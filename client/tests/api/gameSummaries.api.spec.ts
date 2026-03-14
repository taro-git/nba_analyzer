import { describe, expect, it } from "vitest";

import { GameSummariesApi } from "../../app/api/gameSummaries.api";
import { IGameCategory, IGameStatus } from "../../app/api/schemas/gameSummaries";

class TestWrapperClass extends GameSummariesApi {
  public testResIsIRes(data: unknown): boolean {
    return this.resIsIRes(data);
  }
}

describe("GameSummariesApi.resIsIRes", () => {
  const api = new TestWrapperClass();

  const validHomeTeam = {
    teamId: 1,
    teamName: "Test1",
    teamTricode: "TS1",
    teamLogo: "",
  };

  const validAwayTeam = {
    teamId: 2,
    teamName: "Test2",
    teamTricode: "TS2",
    teamLogo: "",
  };

  const validPreseasonGameSummary = {
    gameId: "1",
    status: IGameStatus.Scheduled,
    category: IGameCategory.Preseason,
    startDatetime: "2026-02-24T08:00:00+09:00",
    elapsedSec: 0,
    homeTeam: validHomeTeam,
    awayTeam: validAwayTeam,
    homeTeamScore: 0,
    awayTeamScore: 0,
  };

  const validRegularSeasonGameSummary = {
    ...validPreseasonGameSummary,
    gameId: "2",
    status: IGameStatus.Live,
    category: IGameCategory.RegularSeason,
  };

  const validNBACupGameSummary = {
    ...validPreseasonGameSummary,
    gameId: "3",
    status: IGameStatus.Final,
    category: IGameCategory.NBACup,
  };

  const validPlayoffsGameSummary = {
    ...validPreseasonGameSummary,
    gameId: "4",
    status: IGameStatus.Final,
    category: IGameCategory.Playoffs,
  };

  const validArray = [
    validPreseasonGameSummary,
    validRegularSeasonGameSummary,
    validNBACupGameSummary,
    validPlayoffsGameSummary,
  ];

  it("returns true for valid IGameSummary array", () => {
    expect(api.testResIsIRes(validArray)).toBe(true);
  });

  it("returns false for null", () => {
    expect(api.testResIsIRes(null)).toBe(false);
  });

  it("returns false if not array", () => {
    expect(api.testResIsIRes(validPreseasonGameSummary)).toBe(false);
  });

  const baseInvalidCases = [
    ["gameId missing", (o: Record<string, unknown>) => delete o.gameId],
    ["gameId invalid", (o: Record<string, unknown>) => (o.gameId = 1)],
    ["status missing", (o: Record<string, unknown>) => delete o.status],
    ["status invalid", (o: Record<string, unknown>) => (o.status = "Invalid")],
    ["category missing", (o: Record<string, unknown>) => delete o.category],
    ["category invalid", (o: Record<string, unknown>) => (o.category = "Invalid")],
    ["startDatetime missing", (o: Record<string, unknown>) => delete o.startDatetime],
    ["startDatetime invalid", (o: Record<string, unknown>) => (o.startDatetime = 1)],
    ["elapsedSec missing", (o: Record<string, unknown>) => delete o.elapsedSec],
    ["elapsedSec invalid", (o: Record<string, unknown>) => (o.elapsedSec = "0")],
    ["homeTeam missing", (o: Record<string, unknown>) => delete o.homeTeam],
    ["homeTeam null", (o: Record<string, unknown>) => (o.homeTeam = null)],
    ["awayTeam missing", (o: Record<string, unknown>) => delete o.awayTeam],
    ["awayTeam null", (o: Record<string, unknown>) => (o.awayTeam = null)],
    ["homeTeamScore missing", (o: Record<string, unknown>) => delete o.homeTeamScore],
    ["homeTeamScore invalid", (o: Record<string, unknown>) => (o.homeTeamScore = "0")],
    ["awayTeamScore missing", (o: Record<string, unknown>) => delete o.awayTeamScore],
    ["awayTeamScore invalid", (o: Record<string, unknown>) => (o.awayTeamScore = "0")],
  ] as const;

  baseInvalidCases.forEach(([name, mutate]) => {
    it(`returns false if ${name}`, () => {
      const obj = { ...validPreseasonGameSummary };
      mutate(obj);

      expect(api.testResIsIRes([obj])).toBe(false);
    });
  });

  const teamFieldInvalidCases = [
    ["teamId missing", (t: Record<string, unknown>) => delete t.teamId],
    ["teamId invalid", (t: Record<string, unknown>) => (t.teamId = "1")],
    ["teamName missing", (t: Record<string, unknown>) => delete t.teamName],
    ["teamName invalid", (t: Record<string, unknown>) => (t.teamName = 1)],
    ["teamTricode missing", (t: Record<string, unknown>) => delete t.teamTricode],
    ["teamTricode invalid", (t: Record<string, unknown>) => (t.teamTricode = 1)],
    ["teamLogo missing", (t: Record<string, unknown>) => delete t.teamLogo],
    ["teamLogo invalid", (t: Record<string, unknown>) => (t.teamLogo = 1)],
  ] as const;

  teamFieldInvalidCases.forEach(([name, mutate]) => {
    it(`returns false if homeTeam ${name}`, () => {
      const team = { ...validHomeTeam };
      mutate(team);

      const obj = { ...validPreseasonGameSummary, homeTeam: team };

      expect(api.testResIsIRes([obj])).toBe(false);
    });

    it(`returns false if awayTeam ${name}`, () => {
      const team = { ...validAwayTeam };
      mutate(team);

      const obj = { ...validPreseasonGameSummary, awayTeam: team };

      expect(api.testResIsIRes([obj])).toBe(false);
    });
  });
});

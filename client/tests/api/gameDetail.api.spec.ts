import { describe, expect, it } from "vitest";

import { GameDetailApi } from "../../app/api/gameDetail.api";
import { IGameCategory, IGameStatus } from "../../app/api/schemas/gameSummaries";

class TestWrapperClass extends GameDetailApi {
  public testResIsIRes(data: unknown): boolean {
    return this.resIsIRes(data);
  }
}

describe("GameDetailApi.resIsIRes", () => {
  const api = new TestWrapperClass();

  const validTeam = {
    teamId: 1,
    teamName: "Test Team",
    teamTricode: "TST",
    teamLogo: "https://example.com/logo.svg",
  };

  const validStatics = {
    elapsedMs: 0,
    sec: 0,
    points: 0,
    offenceRebounds: 0,
    diffenceRebounds: 0,
    assists: 0,
    steals: 0,
    blocks: 0,
    fieldGoalAttempts: 0,
    fieldGoalMade: 0,
    threePointAttempts: 0,
    threePointMade: 0,
    freeThrowAttempts: 0,
    freeThrowMade: 0,
    turnovers: 0,
    blockedShotsReceived: 0,
    personalFouls: 0,
    technicalFouls: 0,
    foulsDrawn: 0,
    plus: 0,
    plusMinus: 0,
  };

  const validGamePlayer = {
    playerId: 101,
    teamId: 1,
    fullName: "Test Player",
    abbreviation: "T. Player",
    position: "G",
    dateOfBirth: "2000-01-01",
    draftYear: 2020,
    jearsyNum: "1",
    isHome: true,
    isActive: true,
    isStarter: true,
    statics: [validStatics],
  };

  const validPlay = {
    actionNumber: 1,
    elapsedMs: 60000,
    teamId: 1,
    playerId: 101,
    description: "Made shot",
    homeScore: 2,
    awayScore: 0,
  };

  const validTeamStats = {
    statics: [validStatics],
    players: [validGamePlayer],
  };

  const validGameDetail = {
    gameId: "0012400001",
    status: IGameStatus.Final,
    category: IGameCategory.RegularSeason,
    startDatetime: "2026-02-24T08:00:00+09:00",
    elapsedSec: 2880,
    homeTeam: validTeam,
    awayTeam: { ...validTeam, teamId: 2 },
    homeTeamScore: 100,
    awayTeamScore: 95,
    playoffLabel: null,
    playByPlay: [validPlay],
    homeTeamStats: validTeamStats,
    awayTeamStats: { ...validTeamStats, players: [{ ...validGamePlayer, playerId: 201, isHome: false }] },
  };

  it("returns true for valid game detail", () => {
    expect(api.testResIsIRes(validGameDetail)).toBe(true);
  });

  it("returns false for null", () => {
    expect(api.testResIsIRes(null)).toBe(false);
  });

  it("returns false for non-object", () => {
    expect(api.testResIsIRes("string")).toBe(false);
    expect(api.testResIsIRes(123)).toBe(false);
  });

  it("returns false if playByPlay is missing", () => {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const { playByPlay, ...rest } = validGameDetail;
    expect(api.testResIsIRes(rest)).toBe(false);
  });

  it("returns false if playByPlay is not array", () => {
    expect(api.testResIsIRes({ ...validGameDetail, playByPlay: {} })).toBe(false);
  });

  it("returns false if playByPlay contains invalid play", () => {
    const invalidPlay = { ...validPlay, actionNumber: "1" };
    expect(api.testResIsIRes({ ...validGameDetail, playByPlay: [invalidPlay] })).toBe(false);
  });

  describe("IPlay validation", () => {
    it("returns false if play.actionNumber is missing", () => {
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      const { actionNumber, ...rest } = validPlay;
      expect(api.testResIsIRes({ ...validGameDetail, playByPlay: [rest] })).toBe(false);
    });

    it("returns false if play.actionNumber is not number", () => {
      expect(api.testResIsIRes({ ...validGameDetail, playByPlay: [{ ...validPlay, actionNumber: "1" }] })).toBe(false);
    });

    it("returns false if play.elapsedMs is missing", () => {
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      const { elapsedMs, ...rest } = validPlay;
      expect(api.testResIsIRes({ ...validGameDetail, playByPlay: [rest] })).toBe(false);
    });

    it("returns false if play.elapsedMs is not number", () => {
      expect(api.testResIsIRes({ ...validGameDetail, playByPlay: [{ ...validPlay, elapsedMs: "60000" }] })).toBe(false);
    });

    it("returns false if play.teamId is missing", () => {
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      const { teamId, ...rest } = validPlay;
      expect(api.testResIsIRes({ ...validGameDetail, playByPlay: [rest] })).toBe(false);
    });

    it("returns true if play.teamId is null", () => {
      expect(api.testResIsIRes({ ...validGameDetail, playByPlay: [{ ...validPlay, teamId: null }] })).toBe(true);
    });

    it("returns false if play.playerId is missing", () => {
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      const { playerId, ...rest } = validPlay;
      expect(api.testResIsIRes({ ...validGameDetail, playByPlay: [rest] })).toBe(false);
    });

    it("returns true if play.playerId is null", () => {
      expect(api.testResIsIRes({ ...validGameDetail, playByPlay: [{ ...validPlay, playerId: null }] })).toBe(true);
    });

    it("returns false if play.description is missing", () => {
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      const { description, ...rest } = validPlay;
      expect(api.testResIsIRes({ ...validGameDetail, playByPlay: [rest] })).toBe(false);
    });

    it("returns false if play.homeScore is missing", () => {
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      const { homeScore, ...rest } = validPlay;
      expect(api.testResIsIRes({ ...validGameDetail, playByPlay: [rest] })).toBe(false);
    });

    it("returns true if play.homeScore is null", () => {
      expect(api.testResIsIRes({ ...validGameDetail, playByPlay: [{ ...validPlay, homeScore: null }] })).toBe(true);
    });

    it("returns false if play.awayScore is missing", () => {
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      const { awayScore, ...rest } = validPlay;
      expect(api.testResIsIRes({ ...validGameDetail, playByPlay: [rest] })).toBe(false);
    });

    it("returns true if play.awayScore is null", () => {
      expect(api.testResIsIRes({ ...validGameDetail, playByPlay: [{ ...validPlay, awayScore: null }] })).toBe(true);
    });
  });

  describe("IStatics validation", () => {
    it("returns false if statics.elapsedMs is missing", () => {
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      const { elapsedMs, ...rest } = validStatics;
      const invalidTeamStats = { ...validTeamStats, statics: [rest] };
      expect(api.testResIsIRes({ ...validGameDetail, homeTeamStats: invalidTeamStats })).toBe(false);
    });

    it("returns false if statics.sec is missing", () => {
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      const { sec, ...rest } = validStatics;
      const invalidTeamStats = { ...validTeamStats, statics: [rest] };
      expect(api.testResIsIRes({ ...validGameDetail, homeTeamStats: invalidTeamStats })).toBe(false);
    });

    it("returns false if statics.points is missing", () => {
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      const { points, ...rest } = validStatics;
      const invalidTeamStats = { ...validTeamStats, statics: [rest] };
      expect(api.testResIsIRes({ ...validGameDetail, homeTeamStats: invalidTeamStats })).toBe(false);
    });

    it("returns true if statics.blockedShotsReceived is null", () => {
      const statsWithNull = { ...validStatics, blockedShotsReceived: null };
      const teamStatsWithNull = { ...validTeamStats, statics: [statsWithNull] };
      expect(api.testResIsIRes({ ...validGameDetail, homeTeamStats: teamStatsWithNull })).toBe(true);
    });

    it("returns true if statics.technicalFouls is null", () => {
      const statsWithNull = { ...validStatics, technicalFouls: null };
      const teamStatsWithNull = { ...validTeamStats, statics: [statsWithNull] };
      expect(api.testResIsIRes({ ...validGameDetail, homeTeamStats: teamStatsWithNull })).toBe(true);
    });

    it("returns true if statics.foulsDrawn is null", () => {
      const statsWithNull = { ...validStatics, foulsDrawn: null };
      const teamStatsWithNull = { ...validTeamStats, statics: [statsWithNull] };
      expect(api.testResIsIRes({ ...validGameDetail, homeTeamStats: teamStatsWithNull })).toBe(true);
    });

    it("returns true if statics.plus is null", () => {
      const statsWithNull = { ...validStatics, plus: null };
      const teamStatsWithNull = { ...validTeamStats, statics: [statsWithNull] };
      expect(api.testResIsIRes({ ...validGameDetail, homeTeamStats: teamStatsWithNull })).toBe(true);
    });
  });

  describe("IGamePlayer validation", () => {
    it("returns false if gamePlayer.playerId is missing", () => {
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      const { playerId, ...rest } = validGamePlayer;
      const invalidTeamStats = { ...validTeamStats, players: [rest] };
      expect(api.testResIsIRes({ ...validGameDetail, homeTeamStats: invalidTeamStats })).toBe(false);
    });

    it("returns false if gamePlayer.fullName is missing", () => {
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      const { fullName, ...rest } = validGamePlayer;
      const invalidTeamStats = { ...validTeamStats, players: [rest] };
      expect(api.testResIsIRes({ ...validGameDetail, homeTeamStats: invalidTeamStats })).toBe(false);
    });

    it("returns true if gamePlayer.teamId is null", () => {
      const playerWithNull = { ...validGamePlayer, teamId: null };
      const teamStatsWithNull = { ...validTeamStats, players: [playerWithNull] };
      expect(api.testResIsIRes({ ...validGameDetail, homeTeamStats: teamStatsWithNull })).toBe(true);
    });

    it("returns true if gamePlayer.position is null", () => {
      const playerWithNull = { ...validGamePlayer, position: null };
      const teamStatsWithNull = { ...validTeamStats, players: [playerWithNull] };
      expect(api.testResIsIRes({ ...validGameDetail, homeTeamStats: teamStatsWithNull })).toBe(true);
    });

    it("returns true if gamePlayer.dateOfBirth is null", () => {
      const playerWithNull = { ...validGamePlayer, dateOfBirth: null };
      const teamStatsWithNull = { ...validTeamStats, players: [playerWithNull] };
      expect(api.testResIsIRes({ ...validGameDetail, homeTeamStats: teamStatsWithNull })).toBe(true);
    });

    it("returns true if gamePlayer.draftYear is null", () => {
      const playerWithNull = { ...validGamePlayer, draftYear: null };
      const teamStatsWithNull = { ...validTeamStats, players: [playerWithNull] };
      expect(api.testResIsIRes({ ...validGameDetail, homeTeamStats: teamStatsWithNull })).toBe(true);
    });

    it("returns false if gamePlayer.statics is missing", () => {
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      const { statics, ...rest } = validGamePlayer;
      const invalidTeamStats = { ...validTeamStats, players: [rest] };
      expect(api.testResIsIRes({ ...validGameDetail, homeTeamStats: invalidTeamStats })).toBe(false);
    });

    it("returns false if gamePlayer.statics is not array", () => {
      const invalidTeamStats = { ...validTeamStats, players: [{ ...validGamePlayer, statics: {} }] };
      expect(api.testResIsIRes({ ...validGameDetail, homeTeamStats: invalidTeamStats })).toBe(false);
    });

    it("returns false if gamePlayer.statics contains invalid statics", () => {
      const invalidStatics = { ...validStatics, points: "0" };
      const invalidTeamStats = { ...validTeamStats, players: [{ ...validGamePlayer, statics: [invalidStatics] }] };
      expect(api.testResIsIRes({ ...validGameDetail, homeTeamStats: invalidTeamStats })).toBe(false);
    });
  });

  describe("ITeamStats validation", () => {
    it("returns false if homeTeamStats is missing", () => {
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      const { homeTeamStats, ...rest } = validGameDetail;
      expect(api.testResIsIRes(rest)).toBe(false);
    });

    it("returns false if awayTeamStats is missing", () => {
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      const { awayTeamStats, ...rest } = validGameDetail;
      expect(api.testResIsIRes(rest)).toBe(false);
    });

    it("returns false if teamStats.statics is missing", () => {
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      const { statics, ...rest } = validTeamStats;
      expect(api.testResIsIRes({ ...validGameDetail, homeTeamStats: rest })).toBe(false);
    });

    it("returns false if teamStats.statics is not array", () => {
      expect(api.testResIsIRes({ ...validGameDetail, homeTeamStats: { ...validTeamStats, statics: {} } })).toBe(false);
    });

    it("returns false if teamStats.players is missing", () => {
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      const { players, ...rest } = validTeamStats;
      expect(api.testResIsIRes({ ...validGameDetail, homeTeamStats: rest })).toBe(false);
    });

    it("returns false if teamStats.players is not array", () => {
      expect(api.testResIsIRes({ ...validGameDetail, homeTeamStats: { ...validTeamStats, players: {} } })).toBe(false);
    });
  });

  it("returns true for empty playByPlay array", () => {
    expect(api.testResIsIRes({ ...validGameDetail, playByPlay: [] })).toBe(true);
  });

  it("returns true for empty players array", () => {
    const emptyPlayersStats = { ...validTeamStats, players: [] };
    expect(api.testResIsIRes({ ...validGameDetail, homeTeamStats: emptyPlayersStats })).toBe(true);
  });

  it("returns false if not valid IGameSummary", () => {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const { gameId, ...rest } = validGameDetail;
    expect(api.testResIsIRes(rest)).toBe(false);
  });
});

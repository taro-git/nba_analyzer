import { describe, expect, it } from "vitest";

import { IGameCategory, IGameStatus } from "../../app/api/schemas/gameSummaries";
import { GameDetail, Periods } from "../../app/types/gameDetail";

describe("GameDetail", () => {
  const validTeam = {
    teamId: 1,
    teamName: "Home Team",
    teamTricode: "HOM",
    teamLogo: "https://example.com/home.svg",
  };

  const awayTeam = {
    teamId: 2,
    teamName: "Away Team",
    teamTricode: "AWY",
    teamLogo: "https://example.com/away.svg",
  };

  const createStatics = (elapsedMs: number, sec: number) => ({
    elapsedMs,
    sec,
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
  });

  const createPlayer = (playerId: number, isHome: boolean, isStarter: boolean) => ({
    playerId,
    teamId: isHome ? 1 : 2,
    fullName: `Player ${playerId}`,
    abbreviation: `P${playerId}`,
    position: "G",
    dateOfBirth: "2000-01-01",
    draftYear: 2020,
    jearsyNum: `${playerId}`,
    isHome,
    isActive: true,
    isStarter,
    statics: [createStatics(0, 0), createStatics(720000, 360)],
  });

  const validData = {
    gameId: "0012400001",
    status: IGameStatus.Final,
    category: IGameCategory.RegularSeason,
    startDatetime: "2026-02-24T08:00:00+09:00",
    elapsedSec: 2880,
    homeTeam: validTeam,
    awayTeam: awayTeam,
    homeTeamScore: 100,
    awayTeamScore: 95,
    playoffLabel: null,
    playByPlay: [
      {
        actionNumber: 1,
        elapsedMs: 60000,
        teamId: 1,
        playerId: 101,
        description: "Made shot",
        homeScore: 2,
        awayScore: 0,
      },
    ],
    homeTeamStats: {
      statics: [createStatics(0, 0), createStatics(720000, 3600)],
      players: [createPlayer(101, true, true), createPlayer(102, true, false)],
    },
    awayTeamStats: {
      statics: [createStatics(0, 0), createStatics(720000, 3600)],
      players: [createPlayer(201, false, true), createPlayer(202, false, false)],
    },
  };

  it("constructs with all properties from GameSummary", () => {
    const detail = new GameDetail(validData);

    expect(detail.gameId).toBe("0012400001");
    expect(detail.status).toBe(IGameStatus.Final);
    expect(detail.category).toBe(IGameCategory.RegularSeason);
    expect(detail.homeTeamScore).toBe(100);
    expect(detail.awayTeamScore).toBe(95);
  });

  it("constructs playByPlay array", () => {
    const detail = new GameDetail(validData);

    expect(detail.playByPlay).toHaveLength(1);
    expect(detail.playByPlay[0].actionNumber).toBe(1);
    expect(detail.playByPlay[0].description).toBe("Made shot");
  });

  it("constructs elapsedMilliSecounds array sorted", () => {
    const detail = new GameDetail(validData);

    expect(detail.elapsedMilliSecounds).toEqual([0, 720000]);
    expect(detail.elapsedMilliSecounds[0]).toBeLessThan(detail.elapsedMilliSecounds[1]);
  });

  it("constructs homePlayers record", () => {
    const detail = new GameDetail(validData);

    expect(Object.keys(detail.homePlayers)).toHaveLength(2);
    expect(detail.homePlayers[101]).toBeDefined();
    expect(detail.homePlayers[101].fullName).toBe("Player 101");
    expect(detail.homePlayers[101].isStarter).toBe(true);
    expect(detail.homePlayers[102]).toBeDefined();
    expect(detail.homePlayers[102].isStarter).toBe(false);
  });

  it("constructs awayPlayers record", () => {
    const detail = new GameDetail(validData);

    expect(Object.keys(detail.awayPlayers)).toHaveLength(2);
    expect(detail.awayPlayers[201]).toBeDefined();
    expect(detail.awayPlayers[201].fullName).toBe("Player 201");
    expect(detail.awayPlayers[202]).toBeDefined();
  });

  it("constructs stats record for players", () => {
    const detail = new GameDetail(validData);

    expect(detail.stats[101]).toBeDefined();
    expect(detail.stats[101][0]).toBeDefined();
    expect(detail.stats[101][720000]).toBeDefined();
    expect(detail.stats[102]).toBeDefined();
    expect(detail.stats[201]).toBeDefined();
    expect(detail.stats[202]).toBeDefined();
  });

  it("constructs stats record for teams", () => {
    const detail = new GameDetail(validData);

    expect(detail.stats[1]).toBeDefined(); // home team
    expect(detail.stats[2]).toBeDefined(); // away team
    expect(detail.stats[1][0]).toBeDefined();
    expect(detail.stats[1][720000]).toBeDefined();
  });

  it("sorts stats by elapsedMs", () => {
    const detail = new GameDetail(validData);

    const homeTeamStats = Object.keys(detail.stats[1]).map(Number);
    expect(homeTeamStats[0]).toBeLessThan(homeTeamStats[1]);
  });

  it("homeTableData returns data for home players and team", () => {
    const detail = new GameDetail(validData);

    const tableData = detail.homeTableData(0, 720000);

    // 2 players + 1 team = 3 rows
    expect(tableData).toHaveLength(3);
    expect(tableData[0].isHome).toBe(true);
    expect(tableData[1].isHome).toBe(true);
    expect(tableData[2].isHome).toBe(true);
    expect(tableData[2].isTeam).toBe(true);
  });

  it("awayTableData returns data for away players and team", () => {
    const detail = new GameDetail(validData);

    const tableData = detail.awayTableData(0, 720000);

    // 2 players + 1 team = 3 rows
    expect(tableData).toHaveLength(3);
    expect(tableData[0].isHome).toBe(false);
    expect(tableData[1].isHome).toBe(false);
    expect(tableData[2].isHome).toBe(false);
    expect(tableData[2].isTeam).toBe(true);
  });

  it("homeTableData sorts starters first", () => {
    const detail = new GameDetail(validData);

    const tableData = detail.homeTableData(0, 720000);

    // First player should be starter (101), second should be non-starter (102)
    expect(tableData[0].isStarter).toBe(true);
    expect(tableData[1].isStarter).toBe(false);
  });

  it("homeTableData calculates minutes correctly", () => {
    const detail = new GameDetail(validData);

    const tableData = detail.homeTableData(0, 720000);

    // sec difference: 360 - 0 = 360 seconds = 6 minutes
    expect(tableData[0].minutes).toBe(6);
  });

  it("homeTableData calculates percentages correctly", () => {
    const dataWithStats = {
      ...validData,
      homeTeamStats: {
        ...validData.homeTeamStats,
        players: [
          {
            ...createPlayer(101, true, true),
            statics: [
              createStatics(0, 0),
              {
                ...createStatics(720000, 360),
                fieldGoalMade: 5,
                fieldGoalAttempts: 10,
                threePointMade: 2,
                threePointAttempts: 5,
                freeThrowMade: 3,
                freeThrowAttempts: 4,
              },
            ],
          },
          createPlayer(102, true, false),
        ],
      },
    };

    const detail = new GameDetail(dataWithStats);
    const tableData = detail.homeTableData(0, 720000);

    expect(tableData[0].fialdGoalPercentage).toBe(50);
    expect(tableData[0].threePointPercentage).toBe(40);
    expect(tableData[0].freeThrowPercentage).toBe(75);
  });

  it("homeTableData handles zero attempts for percentages", () => {
    const detail = new GameDetail(validData);

    const tableData = detail.homeTableData(0, 720000);

    expect(tableData[0].fialdGoalPercentage).toBe(0);
    expect(tableData[0].threePointPercentage).toBe(0);
    expect(tableData[0].freeThrowPercentage).toBe(0);
  });

  it("homeTableData calculates efficiency correctly", () => {
    const dataWithStats = {
      ...validData,
      homeTeamStats: {
        ...validData.homeTeamStats,
        players: [
          {
            ...createPlayer(101, true, true),
            statics: [
              createStatics(0, 0),
              {
                ...createStatics(720000, 360),
                points: 10,
                offenceRebounds: 2,
                diffenceRebounds: 3,
                assists: 4,
                steals: 1,
                blocks: 1,
                fieldGoalMade: 4,
                fieldGoalAttempts: 8,
                freeThrowMade: 2,
                freeThrowAttempts: 2,
                turnovers: 2,
              },
            ],
          },
          createPlayer(102, true, false),
        ],
      },
    };

    const detail = new GameDetail(dataWithStats);
    const tableData = detail.homeTableData(0, 720000);

    // efficiency = points + rebounds + assists + steals + blocks + FGM + FTM - FGA - FTA - TO
    // = 10 + 5 + 4 + 1 + 1 + 4 + 2 - 8 - 2 - 2 = 15
    expect(tableData[0].efficiency).toBe(15);
  });

  it("filters out inactive players", () => {
    const dataWithInactive = {
      ...validData,
      homeTeamStats: {
        ...validData.homeTeamStats,
        players: [
          createPlayer(101, true, true),
          { ...createPlayer(102, true, false), isActive: false },
          createPlayer(103, true, false),
        ],
      },
    };

    const detail = new GameDetail(dataWithInactive);
    const tableData = detail.homeTableData(0, 720000);

    // 2 active players + 1 team = 3 rows
    expect(tableData).toHaveLength(3);
  });
});

describe("Periods enum", () => {
  it("exports all period values", () => {
    expect(Periods.firstQuarter).toBe("1st Quarter");
    expect(Periods.secondQuarter).toBe("2nd Quarter");
    expect(Periods.firstHalf).toBe("1st Half");
    expect(Periods.thirdQuarter).toBe("3rd Quarter");
    expect(Periods.fourthQuarter).toBe("4th Quarter");
    expect(Periods.secondHalf).toBe("2nd Half");
    expect(Periods.regulation).toBe("Regulation");
    expect(Periods.overTime).toBe("Over Time");
    expect(Periods.all).toBe("All Periods");
  });
});

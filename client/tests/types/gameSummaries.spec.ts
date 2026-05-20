import dayjs from "dayjs";
import { describe, expect, it } from "vitest";

import { IGameCategory, IGameStatus } from "../../app/api/schemas/gameSummaries";
import { GameCategory, GameStatus, GameSummary } from "../../app/types/gameSummaries";

describe("GameSummary", () => {
  const validTeam = {
    teamId: 1,
    teamName: "Test Team",
    teamTricode: "TST",
    teamLogo: "https://example.com/logo.svg",
  };

  const validData = {
    gameId: "0012400001",
    status: IGameStatus.Scheduled,
    category: IGameCategory.RegularSeason,
    startDatetime: "2026-02-24T08:00:00+09:00",
    elapsedSec: 0,
    homeTeam: validTeam,
    awayTeam: { ...validTeam, teamId: 2, teamName: "Away Team" },
    homeTeamScore: 100,
    awayTeamScore: 95,
    playoffLabel: null,
  };

  it("constructs with all properties", () => {
    const summary = new GameSummary(validData);

    expect(summary.gameId).toBe("0012400001");
    expect(summary.status).toBe(IGameStatus.Scheduled);
    expect(summary.category).toBe(IGameCategory.RegularSeason);
    expect(dayjs.isDayjs(summary.startDatetime)).toBe(true);
    expect(summary.startDatetime.toISOString()).toBe(dayjs("2026-02-24T08:00:00+09:00").toISOString());
    expect(summary.elapsedSec).toBe(0);
    expect(summary.homeTeam).toEqual(validTeam);
    expect(summary.awayTeam).toEqual({ ...validTeam, teamId: 2, teamName: "Away Team" });
    expect(summary.homeTeamScore).toBe(100);
    expect(summary.awayTeamScore).toBe(95);
    expect(summary.playoffLabel).toBe(null);
  });

  it("constructs with playoff label", () => {
    const playoffData = {
      ...validData,
      category: IGameCategory.Playoffs,
      playoffLabel: "East Conference Finals Game 1",
    };

    const summary = new GameSummary(playoffData);

    expect(summary.category).toBe(IGameCategory.Playoffs);
    expect(summary.playoffLabel).toBe("East Conference Finals Game 1");
  });

  it("constructs with Live status", () => {
    const liveData = {
      ...validData,
      status: IGameStatus.Live,
      elapsedSec: 1440,
    };

    const summary = new GameSummary(liveData);

    expect(summary.status).toBe(IGameStatus.Live);
    expect(summary.elapsedSec).toBe(1440);
  });

  it("constructs with Final status", () => {
    const finalData = {
      ...validData,
      status: IGameStatus.Final,
      elapsedSec: 2880,
    };

    const summary = new GameSummary(finalData);

    expect(summary.status).toBe(IGameStatus.Final);
    expect(summary.elapsedSec).toBe(2880);
  });

  it("constructs with all game categories", () => {
    const categories = [
      IGameCategory.Preseason,
      IGameCategory.RegularSeason,
      IGameCategory.NBACup,
      IGameCategory.PlayInTournament,
      IGameCategory.AllStar,
    ];

    categories.forEach((category) => {
      const data = { ...validData, category };
      const summary = new GameSummary(data);
      expect(summary.category).toBe(category);
    });
  });

  it("converts startDatetime string to Dayjs object", () => {
    const summary = new GameSummary(validData);

    expect(dayjs.isDayjs(summary.startDatetime)).toBe(true);
    expect(summary.startDatetime.year()).toBe(2026);
    expect(summary.startDatetime.month()).toBe(1); // 0-indexed, so 1 = February
    expect(summary.startDatetime.date()).toBe(24);
  });

  it("preserves team objects", () => {
    const summary = new GameSummary(validData);

    expect(summary.homeTeam.teamId).toBe(1);
    expect(summary.homeTeam.teamName).toBe("Test Team");
    expect(summary.homeTeam.teamTricode).toBe("TST");
    expect(summary.homeTeam.teamLogo).toBe("https://example.com/logo.svg");

    expect(summary.awayTeam.teamId).toBe(2);
    expect(summary.awayTeam.teamName).toBe("Away Team");
  });

  it("handles zero scores", () => {
    const zeroScoreData = {
      ...validData,
      homeTeamScore: 0,
      awayTeamScore: 0,
    };

    const summary = new GameSummary(zeroScoreData);

    expect(summary.homeTeamScore).toBe(0);
    expect(summary.awayTeamScore).toBe(0);
  });
});

describe("GameStatus export", () => {
  it("exports GameStatus enum", () => {
    expect(GameStatus.Scheduled).toBe("Scheduled");
    expect(GameStatus.Live).toBe("Live");
    expect(GameStatus.Final).toBe("Final");
  });
});

describe("GameCategory export", () => {
  it("exports GameCategory enum", () => {
    expect(GameCategory.Preseason).toBe("Preseason");
    expect(GameCategory.RegularSeason).toBe("Regular Season");
    expect(GameCategory.Playoffs).toBe("Playoffs");
    expect(GameCategory.NBACup).toBe("NBA Cup");
    expect(GameCategory.PlayInTournament).toBe("Play-In Tournament");
    expect(GameCategory.AllStar).toBe("All Star");
  });
});

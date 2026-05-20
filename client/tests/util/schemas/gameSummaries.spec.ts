import { describe, expect, it } from "vitest";

import { IGameCategory, IGameStatus } from "../../../app/api/schemas/gameSummaries";
import { isIGameSummary } from "../../../app/util/schemas/gameSummaries";

describe("isIGameSummary", () => {
  const validTeam = {
    teamId: 1,
    teamName: "Test Team",
    teamTricode: "TST",
    teamLogo: "https://example.com/logo.svg",
  };

  const validGameSummary = {
    gameId: "0012400001",
    status: IGameStatus.Scheduled,
    category: IGameCategory.RegularSeason,
    startDatetime: "2026-02-24T08:00:00+09:00",
    elapsedSec: 0,
    homeTeam: validTeam,
    awayTeam: { ...validTeam, teamId: 2 },
    homeTeamScore: 0,
    awayTeamScore: 0,
    playoffLabel: null,
  };

  it("returns true for valid game summary", () => {
    expect(isIGameSummary(validGameSummary)).toBe(true);
  });

  it("returns true for all valid statuses", () => {
    expect(isIGameSummary({ ...validGameSummary, status: IGameStatus.Scheduled })).toBe(true);
    expect(isIGameSummary({ ...validGameSummary, status: IGameStatus.Live })).toBe(true);
    expect(isIGameSummary({ ...validGameSummary, status: IGameStatus.Final })).toBe(true);
  });

  it("returns true for all valid categories", () => {
    expect(isIGameSummary({ ...validGameSummary, category: IGameCategory.Preseason })).toBe(true);
    expect(isIGameSummary({ ...validGameSummary, category: IGameCategory.RegularSeason })).toBe(true);
    expect(isIGameSummary({ ...validGameSummary, category: IGameCategory.NBACup })).toBe(true);
    expect(isIGameSummary({ ...validGameSummary, category: IGameCategory.PlayInTournament })).toBe(true);
    expect(isIGameSummary({ ...validGameSummary, category: IGameCategory.AllStar })).toBe(true);
  });

  it("returns true for playoffs with playoffLabel", () => {
    expect(
      isIGameSummary({
        ...validGameSummary,
        category: IGameCategory.Playoffs,
        playoffLabel: "East Conference Finals Game 1",
      }),
    ).toBe(true);
  });

  it("returns false for null", () => {
    expect(isIGameSummary(null)).toBe(false);
  });

  it("returns false for undefined", () => {
    expect(isIGameSummary(undefined)).toBe(false);
  });

  it("returns false for non-object", () => {
    expect(isIGameSummary("string")).toBe(false);
    expect(isIGameSummary(123)).toBe(false);
    expect(isIGameSummary(true)).toBe(false);
  });

  it("returns false if gameId is missing", () => {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const { gameId, ...rest } = validGameSummary;
    expect(isIGameSummary(rest)).toBe(false);
  });

  it("returns false if gameId is not string", () => {
    expect(isIGameSummary({ ...validGameSummary, gameId: 123 })).toBe(false);
  });

  it("returns false if status is missing", () => {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const { status, ...rest } = validGameSummary;
    expect(isIGameSummary(rest)).toBe(false);
  });

  it("returns false if status is invalid", () => {
    expect(isIGameSummary({ ...validGameSummary, status: "Invalid" })).toBe(false);
  });

  it("returns false if category is missing", () => {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const { category, ...rest } = validGameSummary;
    expect(isIGameSummary(rest)).toBe(false);
  });

  it("returns false if category is invalid", () => {
    expect(isIGameSummary({ ...validGameSummary, category: "Invalid" })).toBe(false);
  });

  it("returns false if startDatetime is missing", () => {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const { startDatetime, ...rest } = validGameSummary;
    expect(isIGameSummary(rest)).toBe(false);
  });

  it("returns false if startDatetime is not string", () => {
    expect(isIGameSummary({ ...validGameSummary, startDatetime: 123 })).toBe(false);
  });

  it("returns false if elapsedSec is missing", () => {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const { elapsedSec, ...rest } = validGameSummary;
    expect(isIGameSummary(rest)).toBe(false);
  });

  it("returns false if elapsedSec is not number", () => {
    expect(isIGameSummary({ ...validGameSummary, elapsedSec: "0" })).toBe(false);
  });

  it("returns false if homeTeam is missing", () => {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const { homeTeam, ...rest } = validGameSummary;
    expect(isIGameSummary(rest)).toBe(false);
  });

  it("returns false if homeTeam is null", () => {
    expect(isIGameSummary({ ...validGameSummary, homeTeam: null })).toBe(false);
  });

  it("returns false if homeTeam.teamId is missing", () => {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const { teamId, ...rest } = validTeam;
    expect(isIGameSummary({ ...validGameSummary, homeTeam: rest })).toBe(false);
  });

  it("returns false if homeTeam.teamId is not number", () => {
    expect(isIGameSummary({ ...validGameSummary, homeTeam: { ...validTeam, teamId: "1" } })).toBe(false);
  });

  it("returns false if homeTeam.teamName is missing", () => {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const { teamName, ...rest } = validTeam;
    expect(isIGameSummary({ ...validGameSummary, homeTeam: rest })).toBe(false);
  });

  it("returns false if homeTeam.teamName is not string", () => {
    expect(isIGameSummary({ ...validGameSummary, homeTeam: { ...validTeam, teamName: 123 } })).toBe(false);
  });

  it("returns false if homeTeam.teamTricode is missing", () => {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const { teamTricode, ...rest } = validTeam;
    expect(isIGameSummary({ ...validGameSummary, homeTeam: rest })).toBe(false);
  });

  it("returns false if homeTeam.teamTricode is not string", () => {
    expect(isIGameSummary({ ...validGameSummary, homeTeam: { ...validTeam, teamTricode: 123 } })).toBe(false);
  });

  it("returns false if homeTeam.teamLogo is missing", () => {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const { teamLogo, ...rest } = validTeam;
    expect(isIGameSummary({ ...validGameSummary, homeTeam: rest })).toBe(false);
  });

  it("returns false if homeTeam.teamLogo is not string", () => {
    expect(isIGameSummary({ ...validGameSummary, homeTeam: { ...validTeam, teamLogo: 123 } })).toBe(false);
  });

  it("returns false if awayTeam is missing", () => {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const { awayTeam, ...rest } = validGameSummary;
    expect(isIGameSummary(rest)).toBe(false);
  });

  it("returns false if awayTeam is null", () => {
    expect(isIGameSummary({ ...validGameSummary, awayTeam: null })).toBe(false);
  });

  it("returns false if homeTeamScore is missing", () => {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const { homeTeamScore, ...rest } = validGameSummary;
    expect(isIGameSummary(rest)).toBe(false);
  });

  it("returns false if homeTeamScore is not number", () => {
    expect(isIGameSummary({ ...validGameSummary, homeTeamScore: "0" })).toBe(false);
  });

  it("returns false if awayTeamScore is missing", () => {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const { awayTeamScore, ...rest } = validGameSummary;
    expect(isIGameSummary(rest)).toBe(false);
  });

  it("returns false if awayTeamScore is not number", () => {
    expect(isIGameSummary({ ...validGameSummary, awayTeamScore: "0" })).toBe(false);
  });

  it("returns false if playoffLabel is missing", () => {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const { playoffLabel, ...rest } = validGameSummary;
    expect(isIGameSummary(rest)).toBe(false);
  });

  it("returns false if playoffs don't have playoffLabel", () => {
    expect(isIGameSummary({ ...validGameSummary, category: IGameCategory.Playoffs, playoffLabel: null })).toBe(false);
  });

  it("returns false if non-playoffs have playoffLabel", () => {
    expect(isIGameSummary({ ...validGameSummary, category: IGameCategory.Preseason, playoffLabel: "Some Label" })).toBe(
      false,
    );
    expect(
      isIGameSummary({ ...validGameSummary, category: IGameCategory.RegularSeason, playoffLabel: "Some Label" }),
    ).toBe(false);
    expect(isIGameSummary({ ...validGameSummary, category: IGameCategory.NBACup, playoffLabel: "Some Label" })).toBe(
      false,
    );
    expect(
      isIGameSummary({ ...validGameSummary, category: IGameCategory.PlayInTournament, playoffLabel: "Some Label" }),
    ).toBe(false);
    expect(isIGameSummary({ ...validGameSummary, category: IGameCategory.AllStar, playoffLabel: "Some Label" })).toBe(
      false,
    );
  });

  it("returns false if playoffLabel is not string or null", () => {
    expect(isIGameSummary({ ...validGameSummary, playoffLabel: 123 })).toBe(false);
    expect(isIGameSummary({ ...validGameSummary, playoffLabel: true })).toBe(false);
  });
});

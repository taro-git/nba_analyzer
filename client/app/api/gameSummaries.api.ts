import { GameSummary } from "../types/gameSummaries";
import { BaseApi } from "./base.api";
import { type GameSummariesQuery, type IGameSummary } from "./schemas/gameSummaries";
import { type ITeam } from "./schemas/teams";

export class GameSummariesApi extends BaseApi<undefined, GameSummariesQuery, IGameSummary[], GameSummary[]> {
  protected Response = (iGameSummaries: IGameSummary[]) => iGameSummaries.map((item) => new GameSummary(item));

  private isITeam(data: unknown): data is ITeam {
    return (
      typeof data === "object" &&
      data !== null &&
      "teamId" in data &&
      typeof data.teamId === "number" &&
      "teamName" in data &&
      typeof data.teamName === "string" &&
      "teamTricode" in data &&
      typeof data.teamTricode === "string" &&
      "teamLogo" in data &&
      typeof data.teamLogo === "string"
    );
  }

  protected resIsIRes(data: unknown): data is IGameSummary[] {
    return (
      Array.isArray(data) &&
      data.every(
        (item) =>
          typeof item === "object" &&
          item !== null &&
          "gameId" in item &&
          typeof item.gameId === "string" &&
          "status" in item &&
          (item.status === "Scheduled" || item.status === "Live" || item.status === "Final") &&
          "category" in item &&
          (item.category === "Preseason" ||
            item.category === "Regular Season" ||
            item.category === "Playoffs" ||
            item.category === "NBA Cup" ||
            item.category === "Play-In Tournament" ||
            item.category === "All Star") &&
          "startDatetime" in item &&
          typeof item.startDatetime === "string" &&
          "elapsedSec" in item &&
          typeof item.elapsedSec === "number" &&
          "homeTeam" in item &&
          this.isITeam(item.homeTeam) &&
          "awayTeam" in item &&
          this.isITeam(item.awayTeam) &&
          "homeTeamScore" in item &&
          typeof item.homeTeamScore === "number" &&
          "awayTeamScore" in item &&
          typeof item.awayTeamScore === "number" &&
          "playoffLabel" in item &&
          ((item.playoffLabel === null && item.category !== "Playoffs") ||
            (typeof item.playoffLabel === "string" && item.category === "Playoffs")),
      )
    );
  }
}

/**
 * ゲームサマリーを操作する API クラス.
 */
export const gameSummariesApi = new GameSummariesApi("game-summaries");

import { GameDetail } from "../types/gameDetail";
import { isIGameSummary } from "../util/schemas/gameSummaries";
import { BaseApi } from "./base.api";
import { type IGameDetail, type IPlay, type IStatics, type ITeamStats } from "./schemas/gameDetail";
import { type IGamePlayer } from "./schemas/players";

export class GameDetailApi extends BaseApi<undefined, undefined, IGameDetail, GameDetail> {
  protected Response = (iGameDetail: IGameDetail) => new GameDetail(iGameDetail);

  private isIPlay(data: unknown): data is IPlay {
    if (typeof data !== "object" || data === null) return false;
    return (
      "actionNumber" in data &&
      typeof data.actionNumber === "number" &&
      "elapsedMs" in data &&
      typeof data.elapsedMs === "number" &&
      "teamId" in data &&
      (typeof data.teamId === "number" || data.teamId === null) &&
      "playerId" in data &&
      (typeof data.playerId === "number" || data.playerId === null) &&
      "description" in data &&
      typeof data.description === "string" &&
      "homeScore" in data &&
      (typeof data.homeScore === "number" || data.homeScore === null) &&
      "awayScore" in data &&
      (typeof data.awayScore === "number" || data.awayScore === null)
    );
  }

  private isIStatics(data: unknown): data is IStatics {
    if (typeof data !== "object" || data === null) return false;
    return (
      "elapsedMs" in data &&
      typeof data.elapsedMs === "number" &&
      "sec" in data &&
      typeof data.sec === "number" &&
      "points" in data &&
      typeof data.points === "number" &&
      "offenceRebounds" in data &&
      typeof data.offenceRebounds === "number" &&
      "diffenceRebounds" in data &&
      typeof data.diffenceRebounds === "number" &&
      "assists" in data &&
      typeof data.assists === "number" &&
      "steals" in data &&
      typeof data.steals === "number" &&
      "blocks" in data &&
      typeof data.blocks === "number" &&
      "fieldGoalAttempts" in data &&
      typeof data.fieldGoalAttempts === "number" &&
      "fieldGoalMade" in data &&
      typeof data.fieldGoalMade === "number" &&
      "threePointAttempts" in data &&
      typeof data.threePointAttempts === "number" &&
      "threePointMade" in data &&
      typeof data.threePointMade === "number" &&
      "freeThrowAttempts" in data &&
      typeof data.freeThrowAttempts === "number" &&
      "freeThrowMade" in data &&
      typeof data.freeThrowMade === "number" &&
      "turnovers" in data &&
      typeof data.turnovers === "number" &&
      "blockedShotsReceived" in data &&
      (typeof data.blockedShotsReceived === "number" || data.blockedShotsReceived === null) &&
      "personalFouls" in data &&
      typeof data.personalFouls === "number" &&
      "technicalFouls" in data &&
      (typeof data.technicalFouls === "number" || data.technicalFouls === null) &&
      "foulsDrawn" in data &&
      (typeof data.foulsDrawn === "number" || data.foulsDrawn === null) &&
      "plus" in data &&
      (typeof data.plus === "number" || data.plus === null) &&
      "plusMinus" in data &&
      typeof data.plusMinus === "number"
    );
  }

  private isIGamePlayer(data: unknown): data is IGamePlayer {
    if (typeof data !== "object" || data === null) return false;
    return (
      "playerId" in data &&
      typeof data.playerId === "number" &&
      "teamId" in data &&
      (typeof data.teamId === "number" || data.teamId === null) &&
      "fullName" in data &&
      typeof data.fullName === "string" &&
      "abbreviation" in data &&
      typeof data.abbreviation === "string" &&
      "position" in data &&
      (typeof data.position === "string" || data.position === null) &&
      "dateOfBirth" in data &&
      (typeof data.dateOfBirth === "string" || data.dateOfBirth === null) &&
      "draftYear" in data &&
      (typeof data.draftYear === "number" || data.draftYear === null) &&
      "jearsyNum" in data &&
      typeof data.jearsyNum === "string" &&
      "isHome" in data &&
      typeof data.isHome === "boolean" &&
      "isActive" in data &&
      typeof data.isActive === "boolean" &&
      "isStarter" in data &&
      typeof data.isStarter === "boolean"
    );
  }

  private isITeamStats(data: unknown): data is ITeamStats {
    if (typeof data !== "object" || data === null) return false;
    return (
      "statics" in data &&
      Array.isArray(data.statics) &&
      data.statics.every((item) => this.isIStatics(item)) &&
      "players" in data &&
      Array.isArray(data.players) &&
      data.players.every(
        (item) =>
          this.isIGamePlayer(item) &&
          "statics" in item &&
          Array.isArray(item.statics) &&
          item.statics.every((item) => this.isIStatics(item)),
      )
    );
  }

  protected resIsIRes(data: unknown): data is IGameDetail {
    if (typeof data !== "object" || data === null) return false;
    return (
      isIGameSummary(data) &&
      "playByPlay" in data &&
      Array.isArray(data.playByPlay) &&
      data.playByPlay.every((item) => this.isIPlay(item)) &&
      "homeTeamStats" in data &&
      this.isITeamStats(data.homeTeamStats) &&
      "awayTeamStats" in data &&
      this.isITeamStats(data.awayTeamStats)
    );
  }
}

/**
 * ゲーム詳細を操作する API クラス.
 */
export const gameDetailApi = new GameDetailApi();

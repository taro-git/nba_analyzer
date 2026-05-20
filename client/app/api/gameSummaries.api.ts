import { GameSummary } from "../types/gameSummaries";
import { isIGameSummary } from "../util/schemas/gameSummaries";
import { BaseApi } from "./base.api";
import { type GameSummariesQuery, type IGameSummary } from "./schemas/gameSummaries";

export class GameSummariesApi extends BaseApi<undefined, GameSummariesQuery, IGameSummary[], GameSummary[]> {
  protected Response = (iGameSummaries: IGameSummary[]) => iGameSummaries.map((item) => new GameSummary(item));

  protected resIsIRes(data: unknown): data is IGameSummary[] {
    return Array.isArray(data) && data.every((item) => isIGameSummary(item));
  }
}

/**
 * ゲームサマリーを操作する API クラス.
 */
export const gameSummariesApi = new GameSummariesApi("game-summaries");

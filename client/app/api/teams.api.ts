import { RegularSeasonTeams } from "../types/teams";
import { BaseApi } from "./base.api";
import { type IRegularSeasonTeams } from "./schemas/teams";

class RegularSeasonTeamsApi extends BaseApi<undefined, undefined, IRegularSeasonTeams, RegularSeasonTeams> {
  protected Response = RegularSeasonTeams;

  protected resIsIRes(data: unknown): data is IRegularSeasonTeams {
    return typeof data === "object" && data !== null && "season" in data && "teams" in data;
  }
}

/**
 * レギュラーシーズンのチーム成績一覧を操作する API クラス.
 */
export const regularSeasonTeamsApi = new RegularSeasonTeamsApi();

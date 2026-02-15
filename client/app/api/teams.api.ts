import { RegularSeasonTeams } from "../types/teams";
import { isSeason } from "../util/season";
import { BaseApi } from "./base.api";
import { type IRegularSeasonTeams } from "./schemas/teams";

export class RegularSeasonTeamsApi extends BaseApi<undefined, undefined, IRegularSeasonTeams, RegularSeasonTeams> {
  protected Response = RegularSeasonTeams;

  protected resIsIRes(data: unknown): data is IRegularSeasonTeams {
    return (
      typeof data === "object" &&
      data !== null &&
      "season" in data &&
      typeof data.season === "string" &&
      isSeason(data.season) &&
      "teams" in data &&
      Array.isArray(data.teams)
    );
  }
}

/**
 * レギュラーシーズンのチーム成績一覧を操作する API クラス.
 */
export const regularSeasonTeamsApi = new RegularSeasonTeamsApi();

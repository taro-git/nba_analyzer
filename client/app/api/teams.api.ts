import { RegularSeasonTeamStandings } from "../types/teams";
import { BaseApi } from "./base.api";
import { type IRegularSeasonTeamStandings } from "./schemas/teams";

class RegularSeasonTeamStandingsApi extends BaseApi<
  undefined,
  undefined,
  IRegularSeasonTeamStandings,
  RegularSeasonTeamStandings
> {
  protected Response = RegularSeasonTeamStandings;

  protected resIsIRes(data: unknown): data is IRegularSeasonTeamStandings {
    return typeof data === "object" && data !== null && "season" in data && "teams" in data;
  }
}

/**
 * レギュラーシーズンのチーム成績一覧を操作する API クラス.
 */
export const regularSeasonTeamStandingsApi = new RegularSeasonTeamStandingsApi();

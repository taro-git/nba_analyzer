import { type Conferences, type Divisions } from "../../types/leagueStructure";
import { type Season } from "../../types/season";

/**
 * API から受け取るチームの基本情報を表す schema です.
 */
export interface ITeam {
  teamId: number;
  teamName: string;
  teamTricode: string;
  teamLogo: string;
}

/**
 * API から受け取るチームの成績を表す schema です.
 */
export interface IRegularSeasonTeam extends ITeam {
  conference: Conferences;
  division: Divisions;
  rank: number;
  win: number;
  lose: number;
}

/**
 * API から受け取るレギュラーシーズンのチーム成績一覧を表す schema です.
 */
export interface IRegularSeasonTeams {
  season: Season;
  teams: IRegularSeasonTeam[];
}

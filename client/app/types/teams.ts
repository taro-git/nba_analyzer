import { type IRegularSeasonTeams } from "../api/schemas/teams";
import { toSeason } from "../util/season";
import { Conferences, type Divisions } from "./leagueStructure";
import { type Season } from "./season";

export interface RegularSeasonTeam {
  teamId: number;
  teamName: string;
  teamTricode: string;
  teamLogo: string;
  conference: Conferences;
  division: Divisions;
  rank: number;
  win: number;
  lose: number;
  gb: number;
  rate: string;
  gp: number;
}

/**
 * レギュラーシーズンのチーム成績一覧を表すクラスです.
 */
export class RegularSeasonTeams {
  season: Season;
  teams: RegularSeasonTeam[];

  constructor(data?: IRegularSeasonTeams) {
    this.season = toSeason(data?.season ?? "1970-71");
    const eastBestDiffWinLose =
      data?.teams
        .filter((team) => team.conference === Conferences.East)
        .map((team) => team.win - team.lose)
        .sort((a, b) => b - a)[0] ?? 0;
    const westBestDiffWinLose =
      data?.teams
        .filter((team) => team.conference === Conferences.West)
        .map((team) => team.win - team.lose)
        .sort((a, b) => b - a)[0] ?? 0;
    this.teams =
      data?.teams
        .map((team) => {
          const bestDiffWinLose = team.conference === Conferences.East ? eastBestDiffWinLose : westBestDiffWinLose;
          return {
            teamId: team.teamId,
            teamName: team.teamName,
            teamTricode: team.teamTricode,
            teamLogo: team.teamLogo,
            conference: team.conference,
            division: team.division,
            rank: team.rank,
            win: team.win,
            lose: team.lose,
            gb: (bestDiffWinLose + team.lose - team.win) / 2,
            rate: (team.win / (team.win + team.lose)).toFixed(3).slice(1, 5),
            gp: team.win + team.lose,
          };
        })
        .sort((a, b) => (a.rank != b.rank ? a.rank - b.rank : b.win / b.gp - a.win / a.gp)) ?? [];
  }
}

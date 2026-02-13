import { type IRegularSeasonTeams } from "../api/schemas/teams";
import { toSeason } from "../util/season";
import { Conferences, type Divisions } from "./leagueStructure";
import { type Season } from "./season";

interface RegularSeasonTeam {
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
            gb: -(team.win - team.lose - bestDiffWinLose) / 2,
            rate: (team.win / (team.win + team.lose)).toFixed(3).slice(1, 5),
            gp: team.win + team.lose,
          };
        })
        .sort((a, b) => (a.rank != b.rank ? a.rank - b.rank : b.win / b.gp - a.win / a.gp)) ?? [];
  }

  get teamsByConference(): Record<Conferences, RegularSeasonTeam[]> {
    const grouped = this.teams.reduce(
      (acc, team) => {
        (acc[team.conference] ??= []).push(team);
        return acc;
      },
      {} as Record<Conferences, RegularSeasonTeam[]>,
    );

    for (const conference of Object.keys(grouped) as Conferences[]) {
      grouped[conference].sort((a, b) => a.rank - b.rank);
    }

    return grouped;
  }

  get teamsByDivision(): Record<Divisions, RegularSeasonTeam[]> {
    const grouped = this.teams.reduce(
      (acc, team) => {
        (acc[team.division] ??= []).push(team);
        return acc;
      },
      {} as Record<Divisions, RegularSeasonTeam[]>,
    );

    for (const division of Object.keys(grouped) as Divisions[]) {
      grouped[division].sort((a, b) => a.rank - b.rank);
    }

    return grouped;
  }
}

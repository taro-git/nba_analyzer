import { type IRegularSeasonTeamStandings } from "../api/schemas/teams";
import { toSeason } from "../util/season";
import { Conferences, type Divisions } from "./leagueStructure";
import { type Season } from "./season";

interface TeamStanding {
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
export class RegularSeasonTeamStandings {
  season: Season;
  teamStandings: TeamStanding[];

  constructor(data?: IRegularSeasonTeamStandings) {
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
    this.teamStandings =
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

  get teamStandingsByConference(): Record<Conferences, TeamStanding[]> {
    const grouped = this.teamStandings.reduce(
      (acc, team) => {
        (acc[team.conference] ??= []).push(team);
        return acc;
      },
      {} as Record<Conferences, TeamStanding[]>,
    );

    for (const conference of Object.keys(grouped) as Conferences[]) {
      grouped[conference].sort((a, b) => a.rank - b.rank);
    }

    return grouped;
  }

  get teamStandingsByDivision(): Record<Divisions, TeamStanding[]> {
    const grouped = this.teamStandings.reduce(
      (acc, team) => {
        (acc[team.division] ??= []).push(team);
        return acc;
      },
      {} as Record<Divisions, TeamStanding[]>,
    );

    for (const division of Object.keys(grouped) as Divisions[]) {
      grouped[division].sort((a, b) => a.rank - b.rank);
    }

    return grouped;
  }
}

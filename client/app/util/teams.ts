import { type Conferences, type Divisions } from "../types/leagueStructure";
import { type RegularSeasonTeam } from "../types/teams";

/**
 * レギュラーシーズンのチーム一覧をカンファレンスごとにグループ分けして返します.
 */
export function teamsByConference(teams: RegularSeasonTeam[]): Record<Conferences, RegularSeasonTeam[]> {
  const grouped = teams.reduce(
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

/**
 * レギュラーシーズンのチーム一覧をディビジョンごとにグループ分けして返します.
 */
export function teamsByDivision(teams: RegularSeasonTeam[]): Record<Divisions, RegularSeasonTeam[]> {
  const grouped = teams.reduce(
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

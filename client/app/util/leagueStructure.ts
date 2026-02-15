import { Conferences, Divisions } from "../types/leagueStructure";

/**
 * ディビジョンに対応したカンファレンスを返します.
 */
export function ConferenceFromDivisions(division: Divisions): Conferences {
  switch (division) {
    case Divisions.Atlantic:
    case Divisions.Central:
    case Divisions.SouthEast:
      return Conferences.East;
    case Divisions.NorthWest:
    case Divisions.Pacific:
    case Divisions.SouthWest:
      return Conferences.West;
  }
}

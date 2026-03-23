import { type ITeam } from "./teams";

export const IGameStatus = {
  Scheduled: "Scheduled",
  Live: "Live",
  Final: "Final",
} as const;

export type IGameStatus = (typeof IGameStatus)[keyof typeof IGameStatus];

export const IGameCategory = {
  Preseason: "Preseason",
  RegularSeason: "Regular Season",
  Playoffs: "Playoffs",
  NBACup: "NBA Cup",
  PlayInTournament: "Play-In Tournament",
  AllStar: "All Star",
} as const;

export type IGameCategory = (typeof IGameStatus)[keyof typeof IGameStatus];

/**
 * API から受け取るゲームサマリーを表す schema です.
 */
export interface IGameSummary {
  gameId: string;
  status: IGameStatus;
  category: IGameCategory;
  startDatetime: string;
  elapsedSec: number;
  homeTeam: ITeam;
  awayTeam: ITeam;
  homeTeamScore: number;
  awayTeamScore: number;
  playoffLabel?: string;
}

/**
 * GET リクエストのクエリパラメータを表す schema です.
 */
export type GameSummariesQuery = {
  from_utc: string;
  to_utc?: string;
};

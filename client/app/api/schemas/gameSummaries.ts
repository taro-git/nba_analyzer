import { type ITeam } from "./teams";

const IGameStatus = {
  Scheduled: "Scheduled",
  Live: "Live",
  Final: "Final",
} as const;

type IGameStatus = (typeof IGameStatus)[keyof typeof IGameStatus];

const IGameCategory = {
  Preseason: "Preseason",
  RegularSeason: "Regular Season",
  Playoffs: "Playoffs",
  NBACup: "NBA Cup",
} as const;

type IGameCategory = (typeof IGameStatus)[keyof typeof IGameStatus];

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
}

/**
 * GET リクエストのクエリパラメータを表す schema です.
 */
export type GameSummariesQuery = {
  from_utc: string;
  to_utc?: string;
};

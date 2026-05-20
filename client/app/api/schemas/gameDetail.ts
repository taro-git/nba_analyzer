import { type IGameSummary } from "./gameSummaries";
import { type IGamePlayer } from "./players";

export interface IPlay {
  actionNumber: number;
  elapsedMs: number;
  teamId: number | null;
  playerId: number | null;
  description: string;
  homeScore: number | null;
  awayScore: number | null;
}

export interface IStatics {
  elapsedMs: number;
  sec: number;
  points: number;
  offenceRebounds: number;
  diffenceRebounds: number;
  assists: number;
  steals: number;
  blocks: number;
  fieldGoalAttempts: number;
  fieldGoalMade: number;
  threePointAttempts: number;
  threePointMade: number;
  freeThrowAttempts: number;
  freeThrowMade: number;
  turnovers: number;
  blockedShotsReceived: number | null;
  personalFouls: number;
  technicalFouls: number | null;
  foulsDrawn: number | null;
  plus: number | null;
  plusMinus: number;
}

interface IPlayerStats extends IGamePlayer {
  statics: IStatics[];
}

export interface ITeamStats {
  statics: IStatics[];
  players: IPlayerStats[];
}

export interface IGameDetail extends IGameSummary {
  playByPlay: IPlay[];
  homeTeamStats: ITeamStats;
  awayTeamStats: ITeamStats;
}

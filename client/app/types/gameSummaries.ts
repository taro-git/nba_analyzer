import dayjs, { type Dayjs } from "dayjs";

import { IGameCategory, IGameStatus, type IGameSummary } from "../api/schemas/gameSummaries";
import { type Team } from "./teams";

export const GameStatus = IGameStatus;
export type GameStatus = IGameStatus;

export const GameCategory = IGameCategory;
export type GameCategory = IGameCategory;

export class GameSummary {
  gameId: string;
  status: GameStatus;
  category: GameCategory;
  startDatetime: Dayjs;
  elapsedSec: number;
  homeTeam: Team;
  awayTeam: Team;
  homeTeamScore: number;
  awayTeamScore: number;

  constructor(data: IGameSummary) {
    this.gameId = data.gameId;
    this.status = data.status;
    this.category = data.category;
    this.startDatetime = dayjs(data.startDatetime);
    this.elapsedSec = data.elapsedSec;
    this.homeTeam = data.homeTeam;
    this.awayTeam = data.awayTeam;
    this.homeTeamScore = data.homeTeamScore;
    this.awayTeamScore = data.awayTeamScore;
  }
}

import { type IGameSummary } from "../api/schemas/gameSummaries";
import { type Team } from "./teams";

export class GameSummary {
  gameId: string;
  status: string;
  category: string;
  startDatetime: Date;
  elapsedSec: number;
  homeTeam: Team;
  awayTeam: Team;
  homeTeamScore: number;
  awayTeamScore: number;

  constructor(data: IGameSummary) {
    this.gameId = data.gameId;
    this.status = data.status;
    this.category = data.category;
    this.startDatetime = new Date(data.startDatetime);
    this.elapsedSec = data.elapsedSec;
    this.homeTeam = data.homeTeam;
    this.awayTeam = data.awayTeam;
    this.homeTeamScore = data.homeTeamScore;
    this.awayTeamScore = data.awayTeamScore;
  }
}

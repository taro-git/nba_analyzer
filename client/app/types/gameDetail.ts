import { type IGameDetail, type IPlay, type IStatics } from "../api/schemas/gameDetail";
import { type IGamePlayer } from "../api/schemas/players";
import { NBA_REGULATION_PERIOD_SECONDS } from "../conf";
import { GameSummary } from "./gameSummaries";
import { type Team } from "./teams";

type Play = IPlay;
type Statics = IStatics;
type PlayerId = number;
type TeamId = number;
type ElapseMs = number;
type GamePlayer = IGamePlayer;

export interface TableData {
  isTeam: boolean;
  jearsyNum?: string;
  playerName?: string;
  isStarter?: boolean;
  isActive?: boolean;
  isHome: boolean;
  isOnCourt?: boolean;
  minutes: number;
  points: number;
  assists: number;
  rebounds: number;
  steals: number;
  blocks: number;
  fieldGoalMade: number;
  fieldGoalAttempts: number;
  fialdGoalPercentage: number;
  threePointMade: number;
  threePointAttempts: number;
  threePointPercentage: number;
  freeThrowMade: number;
  freeThrowAttempts: number;
  freeThrowPercentage: number;
  offenceRebounds: number;
  diffenceRebounds: number;
  turnovers: number;
  blockedShotsReceived: number | null;
  personalFouls: number;
  technicalFouls: number | null;
  foulsDrawn: number | null;
  efficiency: number;
  plus: number | null;
  plusMinus: number;
}

export class GameDetail extends GameSummary {
  playByPlay: Play[];
  elapsedMilliSecounds: number[];
  homeTeam: Team;
  awayTeam: Team;
  homePlayers: Record<PlayerId, GamePlayer>;
  awayPlayers: Record<PlayerId, GamePlayer>;
  stats: Record<PlayerId | TeamId, Record<ElapseMs, Statics>>;
  hasStatsData: boolean;

  private convertFromBooleanToNumber(value: boolean): number {
    return value ? 1 : 0;
  }

  constructor(data: IGameDetail) {
    super(data);
    this.playByPlay = data.playByPlay;

    // Check if stats data exists
    this.hasStatsData = data.homeTeamStats.statics.length > 0 && data.awayTeamStats.statics.length > 0;

    if (!this.hasStatsData) {
      // Initialize with empty data when stats are not available
      this.elapsedMilliSecounds = [];
      this.homeTeam = data.homeTeam;
      this.awayTeam = data.awayTeam;
      this.homePlayers = {};
      this.awayPlayers = {};
      this.stats = {};
      return;
    }

    const homeElapsedMsSet = new Set(data.homeTeamStats.statics.map((statics) => statics.elapsedMs));
    this.elapsedMilliSecounds = [
      ...new Set(
        data.awayTeamStats.statics
          .map((statics) => statics.elapsedMs)
          .filter((elapsedMs) => homeElapsedMsSet.has(elapsedMs)),
      ),
    ].sort((a, b) => a - b);

    this.homeTeam = data.homeTeam;
    this.awayTeam = data.awayTeam;

    this.homePlayers = data.homeTeamStats.players.reduce<Record<PlayerId, GamePlayer>>((acc, cur) => {
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      const { statics: _unused, ...rest } = cur;
      acc[cur.playerId] = rest;
      return acc;
    }, {});
    this.awayPlayers = data.awayTeamStats.players.reduce<Record<PlayerId, GamePlayer>>((acc, cur) => {
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      const { statics: _unused, ...rest } = cur;
      acc[cur.playerId] = rest;
      return acc;
    }, {});

    const players = [...data.homeTeamStats.players, ...data.awayTeamStats.players];
    this.stats = players.reduce<Record<PlayerId | TeamId, Record<ElapseMs, Statics>>>((acc, cur) => {
      acc[cur.playerId] = cur.statics
        .sort((a, b) => a.elapsedMs - b.elapsedMs)
        .reduce<Record<ElapseMs, Statics>>((acc, cur) => {
          acc[cur.elapsedMs] = cur;
          return acc;
        }, {});
      return acc;
    }, {});
    this.stats[data.homeTeam.teamId] = data.homeTeamStats.statics
      .sort((a, b) => a.elapsedMs - b.elapsedMs)
      .reduce<Record<ElapseMs, Statics>>((acc, cur) => {
        acc[cur.elapsedMs] = cur;
        return acc;
      }, {});
    this.stats[data.awayTeam.teamId] = data.awayTeamStats.statics
      .sort((a, b) => a.elapsedMs - b.elapsedMs)
      .reduce<Record<ElapseMs, Statics>>((acc, cur) => {
        acc[cur.elapsedMs] = cur;
        return acc;
      }, {});
  }

  private calcEfficiency(
    points: number,
    rebounds: number,
    assists: number,
    steals: number,
    blocks: number,
    fieldGoalAttempts: number,
    fieldGoalMade: number,
    freeThrowAttempts: number,
    freeThrowMade: number,
    turnovers: number,
  ): number {
    return (
      points +
      rebounds +
      assists +
      steals +
      blocks +
      fieldGoalMade +
      freeThrowMade -
      fieldGoalAttempts -
      freeThrowAttempts -
      turnovers
    );
  }

  private createTableData(id: number, fromElapsedMs: number, toElapsedMs: number, isHome: boolean): TableData {
    const isTeam = id === this.homeTeam.teamId || id === this.awayTeam.teamId;
    const player = isTeam ? undefined : { ...this.homePlayers, ...this.awayPlayers }[id];
    const fromIndex = this.elapsedMilliSecounds.findIndex((v) => v >= fromElapsedMs);
    const toIndex = this.elapsedMilliSecounds.findIndex((v) => v >= toElapsedMs);
    if (fromIndex === -1) new Error("fromElapsedMs is out of elapsedMilliSecounds range");
    const lastElapsedMs = fromIndex > 0 ? this.elapsedMilliSecounds[fromIndex - 1] : this.elapsedMilliSecounds[0];
    const lastStats = this.stats[id][lastElapsedMs];
    const currentStats = this.stats[id][toElapsedMs];
    const points = currentStats.points - lastStats.points;
    const assists = currentStats.assists - lastStats.assists;
    const offenceRebounds = currentStats.offenceRebounds - lastStats.offenceRebounds;
    const diffenceRebounds = currentStats.diffenceRebounds - lastStats.diffenceRebounds;
    const rebounds = offenceRebounds + diffenceRebounds;
    const steals = currentStats.steals - lastStats.steals;
    const blocks = currentStats.blocks - lastStats.blocks;
    const fieldGoalMade = currentStats.fieldGoalMade - lastStats.fieldGoalMade;
    const fieldGoalAttempts = currentStats.fieldGoalAttempts - lastStats.fieldGoalAttempts;
    const threePointMade = currentStats.threePointMade - lastStats.threePointMade;
    const threePointAttempts = currentStats.threePointAttempts - lastStats.threePointAttempts;
    const freeThrowMade = currentStats.freeThrowMade - lastStats.freeThrowMade;
    const freeThrowAttempts = currentStats.freeThrowAttempts - lastStats.freeThrowAttempts;
    const turnovers = currentStats.turnovers - lastStats.turnovers;
    return {
      isTeam: isTeam,
      jearsyNum: player?.jearsyNum,
      playerName: player?.abbreviation,
      isStarter: player?.isStarter,
      isActive: player?.isActive,
      isHome: isHome,
      isOnCourt: isTeam
        ? undefined
        : toIndex === -1 || toIndex === 0
          ? player?.isStarter
          : this.stats[id][toElapsedMs].sec !== this.stats[id][this.elapsedMilliSecounds[toIndex - 1]].sec,
      minutes: Math.round(((currentStats.sec - lastStats.sec) / 60) * 10) / 10,
      points: points,
      assists: assists,
      rebounds: rebounds,
      steals: steals,
      blocks: blocks,
      fieldGoalMade: fieldGoalMade,
      fieldGoalAttempts: fieldGoalAttempts,
      fialdGoalPercentage: fieldGoalAttempts <= 0 ? 0 : Math.round((fieldGoalMade / fieldGoalAttempts) * 100 * 10) / 10,
      threePointMade: threePointMade,
      threePointAttempts: threePointAttempts,
      threePointPercentage:
        threePointAttempts <= 0 ? 0 : Math.round((threePointMade / threePointAttempts) * 100 * 10) / 10,
      freeThrowMade: freeThrowMade,
      freeThrowAttempts: freeThrowAttempts,
      freeThrowPercentage: freeThrowAttempts <= 0 ? 0 : Math.round((freeThrowMade / freeThrowAttempts) * 100 * 10) / 10,
      offenceRebounds: currentStats.offenceRebounds - lastStats.offenceRebounds,
      diffenceRebounds: currentStats.diffenceRebounds - lastStats.diffenceRebounds,
      turnovers: turnovers,
      blockedShotsReceived:
        currentStats.blockedShotsReceived === null || lastStats.blockedShotsReceived === null
          ? null
          : currentStats.blockedShotsReceived - lastStats.blockedShotsReceived,
      personalFouls: currentStats.personalFouls - lastStats.personalFouls,
      technicalFouls:
        currentStats.technicalFouls === null || lastStats.technicalFouls === null
          ? null
          : currentStats.technicalFouls - lastStats.technicalFouls,
      foulsDrawn:
        currentStats.foulsDrawn === null || lastStats.foulsDrawn === null
          ? null
          : currentStats.foulsDrawn - lastStats.foulsDrawn,
      efficiency: this.calcEfficiency(
        points,
        rebounds,
        assists,
        steals,
        blocks,
        fieldGoalAttempts,
        fieldGoalMade,
        freeThrowAttempts,
        freeThrowMade,
        turnovers,
      ),
      plus: currentStats.plus === null || lastStats.plus === null ? null : currentStats.plus - lastStats.plus,
      plusMinus: currentStats.plusMinus - lastStats.plusMinus,
    };
  }

  /**
   * 試合経過時間の範囲を指定してホームチームのテーブルデータ一覧を返します.
   */
  homeTableData(fromElapsedMs: number, toElapsedMs: number): TableData[] {
    if (!this.hasStatsData) {
      return [];
    }
    const playerIds = Object.values(this.homePlayers)
      .filter((p) => p.isActive)
      .sort((a, b) => this.convertFromBooleanToNumber(b.isStarter) - this.convertFromBooleanToNumber(a.isStarter))
      .sort((a, b) => this.convertFromBooleanToNumber(b.isActive) - this.convertFromBooleanToNumber(a.isActive))
      .map((p) => p.playerId);
    return [...playerIds, this.homeTeam.teamId].map((id) => this.createTableData(id, fromElapsedMs, toElapsedMs, true));
  }

  /**
   * 試合経過時間の範囲を指定してアウェイチームのテーブルデータ一覧を返します.
   */
  awayTableData(fromElapsedMs: number, toElapsedMs: number): TableData[] {
    if (!this.hasStatsData) {
      return [];
    }
    const playerIds = Object.values(this.awayPlayers)
      .filter((p) => p.isActive)
      .sort((a, b) => this.convertFromBooleanToNumber(b.isStarter) - this.convertFromBooleanToNumber(a.isStarter))
      .sort((a, b) => this.convertFromBooleanToNumber(b.isActive) - this.convertFromBooleanToNumber(a.isActive))
      .map((p) => p.playerId);
    return [...playerIds, this.awayTeam.teamId].map((id) =>
      this.createTableData(id, fromElapsedMs, toElapsedMs, false),
    );
  }
}

/**
 * ピリオドの区切り方を定義します.
 */
export const Periods = {
  firstQuarter: "1st Quarter",
  secondQuarter: "2nd Quarter",
  firstHalf: "1st Half",
  thirdQuarter: "3rd Quarter",
  fourthQuarter: "4th Quarter",
  secondHalf: "2nd Half",
  regulation: "Regulation",
  overTime: "Over Time",
  all: "All Periods",
} as const;

/**
 * ピリオドの区切り方を定義します.
 */
export type Periods = (typeof Periods)[keyof typeof Periods];

type PeriodRange = {
  minElapsedMs?: number;
  maxElapsedMs?: number;
};

export const periodRanges: Record<Periods, PeriodRange> = {
  [Periods.firstQuarter]: { maxElapsedMs: NBA_REGULATION_PERIOD_SECONDS * 1000 },
  [Periods.secondQuarter]: {
    minElapsedMs: NBA_REGULATION_PERIOD_SECONDS * 1000,
    maxElapsedMs: NBA_REGULATION_PERIOD_SECONDS * 2 * 1000,
  },
  [Periods.firstHalf]: { maxElapsedMs: NBA_REGULATION_PERIOD_SECONDS * 2 * 1000 },
  [Periods.thirdQuarter]: {
    minElapsedMs: NBA_REGULATION_PERIOD_SECONDS * 2 * 1000,
    maxElapsedMs: NBA_REGULATION_PERIOD_SECONDS * 3 * 1000,
  },
  [Periods.fourthQuarter]: {
    minElapsedMs: NBA_REGULATION_PERIOD_SECONDS * 3 * 1000,
    maxElapsedMs: NBA_REGULATION_PERIOD_SECONDS * 4 * 1000,
  },
  [Periods.secondHalf]: {
    minElapsedMs: NBA_REGULATION_PERIOD_SECONDS * 2 * 1000,
    maxElapsedMs: NBA_REGULATION_PERIOD_SECONDS * 4 * 1000,
  },
  [Periods.regulation]: { maxElapsedMs: NBA_REGULATION_PERIOD_SECONDS * 4 * 1000 },
  [Periods.overTime]: { minElapsedMs: NBA_REGULATION_PERIOD_SECONDS * 4 * 1000 },
  [Periods.all]: {},
};

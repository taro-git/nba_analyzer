/**
 * プレイヤーのポジションを定義します.
 */
export const IPosition = {
  PointGuard: "PG",
  ShootingGuard: "SG",
  SmallForward: "SF",
  PowerForward: "PF",
  Center: "C",
} as const;

/**
 * プレイヤーのポジションを定義します.
 */
export type IPosition = (typeof IPosition)[keyof typeof IPosition];

/**
 * API から受け取る選手情報を表す schema です.
 */
interface IPlayer {
  playerId: number;
  teamId: number | null;
  fullName: string;
  abbreviation: string;
  position: IPosition | null;
  dateOfBirth: string | null;
  draftYear: number | null;
}

/**
 * API から受け取る試合に紐づく選手情報を表す schema です.
 */
export interface IGamePlayer extends IPlayer {
  jearsyNum: string;
  isHome: boolean;
  isActive: boolean;
  isStarter: boolean;
}

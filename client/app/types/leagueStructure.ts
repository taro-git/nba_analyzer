/**
 * シーズン種別を定義します.
 */
export const SeasonTypes = {
  Regular: "regular-seasons",
  Playoffs: "playoffs",
} as const;

/**
 * シーズン種別を定義します.
 */
export type SeasonTypes = (typeof SeasonTypes)[keyof typeof SeasonTypes];

/**
 * チームのカテゴライズ方法を定義します.
 */
export const TeamCategories = {
  All: "all",
  Conference: "conference",
  Division: "division",
} as const;

/**
 * チームのカテゴライズ方法を定義します.
 */
export type TeamCategories = (typeof TeamCategories)[keyof typeof TeamCategories];

/**
 * リーグのカンファレンスを定義します.
 */
export const Conferences = {
  East: "East",
  West: "West",
} as const;

/**
 * リーグのカンファレンスを定義します.
 */
export type Conferences = (typeof Conferences)[keyof typeof Conferences];

/**
 * リーグのディビジョンを定義します.
 */
export const Divisions = {
  Atlantic: "Atlantic",
  Central: "Central",
  SouthEast: "SouthEast",
  NorthWest: "NorthWest",
  Pacific: "Pacific",
  SouthWest: "SouthWest",
} as const;

/**
 * リーグのディビジョンを定義します.
 */
export type Divisions = (typeof Divisions)[keyof typeof Divisions];

/**
 * ディビジョンに対応したカンファレンスを返します.
 */
export const ConferenceFromDivisions: (division: Divisions) => Conferences = (division: Divisions) => {
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
};

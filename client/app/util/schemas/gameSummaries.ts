import { type IGameSummary } from "../../api/schemas/gameSummaries";
import { type ITeam } from "../../api/schemas/teams";

function isITeam(data: unknown): data is ITeam {
  if (typeof data !== "object" || data === null) return false;
  return (
    "teamId" in data &&
    typeof data.teamId === "number" &&
    "teamName" in data &&
    typeof data.teamName === "string" &&
    "teamTricode" in data &&
    typeof data.teamTricode === "string" &&
    "teamLogo" in data &&
    typeof data.teamLogo === "string"
  );
}

export function isIGameSummary(data: unknown): data is IGameSummary {
  if (typeof data !== "object" || data === null) return false;
  return (
    "gameId" in data &&
    typeof data.gameId === "string" &&
    "status" in data &&
    (data.status === "Scheduled" || data.status === "Live" || data.status === "Final") &&
    "category" in data &&
    (data.category === "Preseason" ||
      data.category === "Regular Season" ||
      data.category === "Playoffs" ||
      data.category === "NBA Cup" ||
      data.category === "Play-In Tournament" ||
      data.category === "All Star") &&
    "startDatetime" in data &&
    typeof data.startDatetime === "string" &&
    "elapsedSec" in data &&
    typeof data.elapsedSec === "number" &&
    "homeTeam" in data &&
    isITeam(data.homeTeam) &&
    "awayTeam" in data &&
    isITeam(data.awayTeam) &&
    "homeTeamScore" in data &&
    typeof data.homeTeamScore === "number" &&
    "awayTeamScore" in data &&
    typeof data.awayTeamScore === "number" &&
    "playoffLabel" in data &&
    ((data.playoffLabel === null && data.category !== "Playoffs") ||
      (typeof data.playoffLabel === "string" && data.category === "Playoffs"))
  );
}

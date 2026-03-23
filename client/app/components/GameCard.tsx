import { Avatar, Box, Paper, Typography, useColorScheme } from "@mui/material";

import dayjs from "dayjs";
import utc from "dayjs/plugin/utc";
import { useMemo } from "react";
import { Link } from "react-router";

import { BASE_URL } from "../routes";
import { theme } from "../routes/layout";
import { GameStatus, type GameSummary } from "../types/gameSummaries";
import { type Team } from "../types/teams";

dayjs.extend(utc);

type Props = {
  gameSummary: GameSummary;
  showScore?: boolean;
};

/**
 * チーム表示
 */
function TeamBlock({ team }: { team: Team }) {
  return (
    <Box textAlign="center">
      <Avatar src={team.teamLogo} sx={{ width: "4rem", height: "4rem", margin: "0 auto", borderRadius: 0 }} />
      <Typography fontSize="0.75rem">{team.teamTricode}</Typography>
    </Box>
  );
}

/**
 * スコア表示
 */
function Score({ value }: { value: number }) {
  return (
    <Typography fontSize="1.8rem" fontWeight="bold">
      {value ?? 0}
    </Typography>
  );
}

export default function GameCard({ gameSummary, showScore = true }: Props) {
  const { systemMode } = useColorScheme();

  const palette = useMemo(() => {
    return systemMode === "light" ? theme.colorSchemes.light?.palette : theme.colorSchemes.dark?.palette;
  }, [systemMode]);

  /**
   * ステータス文字列
   */
  const statusText = () => {
    const date = gameSummary.startDatetime;

    switch (gameSummary.status) {
      case GameStatus.Scheduled: {
        return `Scheduled at ${dayjs(date).local().format("HH:mm")}`;
      }

      case GameStatus.Live: {
        const elapsedMin = Math.floor(gameSummary.elapsedSec / 60);
        const quarter = Math.floor(elapsedMin / 12 + 1);
        const min = elapsedMin % 12;
        const sec = gameSummary.elapsedSec % 60;
        return `Live ${quarter}Q ${min.toString().padStart(2, "0")}:${sec.toString().padStart(2, "0")}`;
      }

      case GameStatus.Final:
        return "Final";
    }
  };

  /**
   * サブステータス文字列
   */
  const subStatusText = () => {
    if (gameSummary.playoffLabel) return gameSummary.playoffLabel;
    return gameSummary.category;
  };

  return (
    <Paper
      component={Link}
      to={`/${BASE_URL}/games/${gameSummary.gameId}`}
      sx={{
        width: "85%",
        height: "9rem",
        borderRadius: 2,
        bgcolor: palette?.getContrastText("monotone"),
        "&:hover": {
          bgcolor: palette?.getContrastText(""),
        },
        my: "1rem",
        mx: "1.5rem",
        p: "0.5rem",
      }}
      elevation={5}
    >
      <Typography textAlign="center" fontWeight="bold" fontSize="1.25rem" mb="0.25rem">
        {statusText()}
      </Typography>
      <Typography textAlign="center" fontSize="0.75rem">
        {subStatusText()}
      </Typography>
      <Box display="flex" alignItems="center" justifyContent="space-between" px="0rem">
        <TeamBlock team={gameSummary.awayTeam} />
        {showScore && <Score value={gameSummary.awayTeamScore} />}
        <Typography fontSize="1.8rem">-</Typography>
        {showScore && <Score value={gameSummary.homeTeamScore} />}
        <TeamBlock team={gameSummary.homeTeam} />
      </Box>
    </Paper>
  );
}

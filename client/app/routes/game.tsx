import type { SelectChangeEvent } from "@mui/material";
import { Grid, MenuItem, Paper, Select, useColorScheme } from "@mui/material";
import Slider from "@mui/material/Slider";

import { type ColDef, type ValueGetterParams } from "ag-grid-community";
import chroma from "chroma-js";
import { useMemo, useRef, useState } from "react";

import { gameDetailApi } from "../api/gameDetail.api";
import { gameSummariesApi } from "../api/gameSummaries.api";
import CustomTable from "../components/CustomTable";
import FullWidthTab, { type TabItem } from "../components/FullWidthTab";
import GameCard from "../components/GameCard";
import { TEAM_COLOR } from "../conf";
import { theme } from "../routes/layout";
import { type GameDetail, periodRanges, Periods, type TableData } from "../types/gameDetail";
import { type GameSummary } from "../types/gameSummaries";
import { convertFromElapsedMsToGameClock, toPeriod } from "../util/games";
import { type Route } from "./+types/game";

/**
 * Game 詳細画面のクライアントローダーを定義します.
 */
export async function clientLoader({
  params,
}: Route.ClientLoaderArgs): Promise<{ gameDetail: GameDetail; headToheadGames: GameSummary[] }> {
  gameDetailApi.path = `/games/${params.gameId}`;
  const gameDetail = await gameDetailApi.get();
  const headToheadGames = await gameSummariesApi.get({
    team_ids: [gameDetail.homeTeam.teamId, gameDetail.awayTeam.teamId],
  });
  return { gameDetail, headToheadGames };
}

/**
 * Game 画面を定義します.
 */
export default function Game({ loaderData }: Route.ComponentProps) {
  // ----------------------------------------------------------------------
  // Initial
  // ----------------------------------------------------------------------

  // ----------------------------------------------------------------------
  // Loadings
  // ----------------------------------------------------------------------
  const gameDetail = loaderData.gameDetail;
  const headToheadGames = loaderData.headToheadGames;
  const elapsedMillisecounds: number[] = gameDetail.elapsedMilliSecounds;

  // ----------------------------------------------------------------------
  // States
  // ----------------------------------------------------------------------
  const [elapsedMsRange, setElapsedMsRange] = useState<number[]>(
    elapsedMillisecounds.length > 0 ? Array(2).fill(Math.min(...elapsedMillisecounds)) : [0, 0],
  );
  const [periods, setPeriods] = useState<Periods>(Periods.regulation);

  // ----------------------------------------------------------------------
  // Refs
  // ----------------------------------------------------------------------
  const currentHeadToHeadRef = useRef<HTMLDivElement | null>(null);

  // ----------------------------------------------------------------------
  // Events
  // ----------------------------------------------------------------------
  const periodsOnChange = (event: SelectChangeEvent) => {
    setElapsedMsRange(
      Array(2).fill(
        Math.max(
          ...elapsedMillisecounds.filter(
            (elapsedMs) =>
              elapsedMs <=
              (periodRanges[toPeriod(event.target.value)].minElapsedMs ?? Math.min(...elapsedMillisecounds)),
          ),
        ),
      ),
    );
    setPeriods(toPeriod(event.target.value));
  };

  const elapsedMsRangeOnChange = (_: Event, newValue: number | number[]) => {
    if (!Array.isArray(newValue) || newValue.length !== 2) {
      new Error("Invalid value");
    } else {
      setElapsedMsRange(newValue.map((v) => Math.max(...elapsedMillisecounds.filter((elapsedMs) => elapsedMs <= v))));
    }
  };

  const onTabChange = (selectedItemIndex: number) => {
    if (selectedItemIndex === tabItems.findIndex((t) => t.label === "Head-to-Head")) {
      requestAnimationFrame(() => {
        currentHeadToHeadRef.current?.scrollIntoView({ block: "start", behavior: "smooth" });
      });
    }
  };

  // ----------------------------------------------------------------------
  // Views
  // ----------------------------------------------------------------------
  const systemMode = useColorScheme().systemMode;
  const palette = useMemo(() => {
    return systemMode === "light" ? theme.colorSchemes.light?.palette : theme.colorSchemes.dark?.palette;
  }, [systemMode]);
  const homeTeamColor =
    gameDetail.homeTeam.teamTricode in TEAM_COLOR
      ? TEAM_COLOR[gameDetail.homeTeam.teamTricode]
      : (palette?.primary.main ?? "#ffffff");
  const awayTeamColor =
    gameDetail.awayTeam.teamTricode in TEAM_COLOR
      ? TEAM_COLOR[gameDetail.awayTeam.teamTricode]
      : (palette?.primary.main ?? "#ffffff");
  const gameColor = chroma
    .mix(homeTeamColor, awayTeamColor, 0.5)
    .mix(palette?.text.primary ?? "#ffffff", 0.8)
    .hex("rgb");

  const statsTableHeaderNames: Partial<Record<keyof TableData, string>> = {
    minutes: "MIN",
    points: "PTS",
    assists: "AST",
    rebounds: "REB",
    steals: "STL",
    blocks: "BLK",
    fieldGoalMade: "FGM",
    fieldGoalAttempts: "FGA",
    fialdGoalPercentage: "FG%",
    threePointMade: "3PM",
    threePointAttempts: "3PA",
    threePointPercentage: "3P%",
    freeThrowMade: "FTM",
    freeThrowAttempts: "FTA",
    freeThrowPercentage: "FT%",
    offenceRebounds: "OREB",
    diffenceRebounds: "DREB",
    turnovers: "TO",
    blockedShotsReceived: "BSR",
    personalFouls: "PF",
    technicalFouls: "TF",
    foulsDrawn: "FD",
    efficiency: "EFF",
    plus: "+",
    plusMinus: "+/-",
  };

  const statsColDefs: ColDef[] = [
    {
      field: "principal",
      headerName: "Player",
      resizable: true,
      pinned: "left",
      sortable: false,
      lockPinned: true,
      cellRenderer: (params: ValueGetterParams) => {
        if (params.data.isTeam) return "Total";
        return (
          <div
            style={{
              width: "100%",
              display: "flex",
              alignItems: "center",
              gap: 3,
              textShadow: !params.data.isOnCourt
                ? undefined
                : params.data.isHome
                  ? `0 0 2px ${homeTeamColor}`
                  : `0 0 2px ${awayTeamColor}`,
            }}
          >
            <span style={{ width: "1.2rem", textAlign: "center" }}>{params.data.jearsyNum}</span>
            <span>{params.data.playerName}</span>
          </div>
        );
      },
      width: 150,
    },
    ...Object.entries(statsTableHeaderNames).map(([key, value]) => {
      return {
        field: key,
        headerName: value,
        width: 80,
      };
    }),
  ];
  const homeBoxScoreData = gameDetail.homeTableData(elapsedMsRange[0], elapsedMsRange[1]);
  const awayBoxScoreData = gameDetail.awayTableData(elapsedMsRange[0], elapsedMsRange[1]);
  const hasStatsData = gameDetail.hasStatsData;

  const gameClockComponent = hasStatsData ? (
    <div
      style={{
        height: "9rem",
        width: "100%",
        paddingLeft: "2rem",
        paddingRight: "2rem",
        display: "grid",
        justifyItems: "center",
      }}
    >
      <Select
        sx={{ height: "2.5rem", width: "100%", paddingt: "0", marginTop: "0.5rem", marginBottom: "0.5rem" }}
        id="pereods-select"
        value={periods}
        onChange={periodsOnChange}
      >
        {Object.values(Periods).map((periods) => (
          <MenuItem key={periods} value={periods}>
            {periods}
          </MenuItem>
        ))}
      </Select>
      <div style={{ height: "1.5rem", width: "100%", display: "grid", justifyItems: "center", marginTop: "1rem" }}>
        {convertFromElapsedMsToGameClock(elapsedMsRange[0], periods).string} ー{" "}
        {convertFromElapsedMsToGameClock(elapsedMsRange[1], periods).string}
      </div>
      <div style={{ height: "3rem", width: "100%" }}>
        <Slider
          min={periodRanges[periods].minElapsedMs ?? Math.min(...elapsedMillisecounds)}
          max={periodRanges[periods].maxElapsedMs ?? Math.max(...elapsedMillisecounds)}
          step={null}
          marks={elapsedMillisecounds.map((s) => ({ value: s }))}
          sx={{
            "& .MuiSlider-mark": {
              backgroundColor: "#00000000",
            },
            "& .MuiSlider-markActive": {
              backgroundColor: "#00000000",
            },
            color: gameColor,
            "& .MuiSlider-thumb": {
              backgroundColor: "currentColor",
              border: "2px solid currentColor",
              "&:focus, &:hover, &.Mui-active, &.Mui-focusVisible": {
                boxShadow: "inherit",
              },
              "&::before": {
                display: "none",
              },
            },
          }}
          value={elapsedMsRange}
          onChange={elapsedMsRangeOnChange}
        />
      </div>
    </div>
  ) : null;

  const summaryColDefs: ColDef[] = [
    { field: "away", headerName: gameDetail.awayTeam.teamTricode, sortable: false, type: "centerAligned" },
    { field: "stats", headerName: "", sortable: false, width: 30, type: "centerAligned" },
    { field: "home", headerName: gameDetail.homeTeam.teamTricode, sortable: false, type: "centerAligned" },
  ];
  const summaryTableData = hasStatsData
    ? (Object.keys(statsTableHeaderNames) as (keyof TableData)[])
        .filter((key) => key !== "minutes")
        .map((key) => {
          return {
            away: awayBoxScoreData.filter((item) => item.isTeam)[0][key],
            stats: statsTableHeaderNames[key],
            home: homeBoxScoreData.filter((item) => item.isTeam)[0][key],
          };
        })
    : [];

  const noDataComponent = (
    <div
      style={{
        height: "calc(100dvh - 26.5rem)",
        width: "100%",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontSize: "1.5rem",
        color: palette?.text.secondary,
      }}
    >
      No Data
    </div>
  );

  const tabItems: TabItem[] = [
    {
      label: "Summary",
      item: (
        <>
          {gameClockComponent}
          {hasStatsData ? (
            <CustomTable
              columnDefs={summaryColDefs}
              data={summaryTableData}
              degree={undefined}
              height={"calc(100dvh - 26.5rem)"}
              width="100%"
              headerColor={gameColor + "50"}
            />
          ) : (
            noDataComponent
          )}
        </>
      ),
      color: gameColor,
    },
    {
      label: "Box-Score",
      item: (
        <>
          {gameClockComponent}
          {hasStatsData ? (
            <div
              style={{
                height: "calc(100dvh - 26.5rem)",
                width: "100%",
                display: "grid",
                justifyItems: "center",
                alignContent: "start",
              }}
            >
              <FullWidthTab
                tabItems={[
                  {
                    label: gameDetail.awayTeam.teamTricode,
                    item: (
                      <CustomTable
                        columnDefs={statsColDefs}
                        data={awayBoxScoreData}
                        degree={undefined}
                        height={"calc(100dvh - 28rem)"}
                        headerColor={awayTeamColor + "50"}
                      />
                    ),
                    color: awayTeamColor,
                  },
                  {
                    label: gameDetail.homeTeam.teamTricode,
                    item: (
                      <CustomTable
                        columnDefs={statsColDefs}
                        data={homeBoxScoreData}
                        degree={undefined}
                        height={"calc(100dvh - 28rem)"}
                        headerColor={homeTeamColor + "50"}
                      />
                    ),
                    color: homeTeamColor,
                  },
                ]}
                defaultIndex={0}
                onChange={() => {}}
                tabShape={{ height: "1.5rem", width: "60%" }}
              />
            </div>
          ) : (
            noDataComponent
          )}
        </>
      ),
      color: gameColor,
    },
    {
      label: "Play-by-Play",
      item: (
        <>
          {gameClockComponent}
          {hasStatsData ? (
            <div
              style={{
                height: "calc(100dvh - 26.5rem)",
                width: "100%",
                display: "grid",
                justifyItems: "center",
                alignContent: "start",
                overflowY: "scroll",
              }}
            >
              {gameDetail.playByPlay.map((play, index) => {
                if (play.elapsedMs < elapsedMsRange[0] || play.elapsedMs > elapsedMsRange[1]) return null;
                const gameClock = convertFromElapsedMsToGameClock(play.elapsedMs, periods);
                const prevGameClock =
                  index !== 0
                    ? convertFromElapsedMsToGameClock(gameDetail.playByPlay[index - 1].elapsedMs, periods)
                    : undefined;
                return (
                  <div key={`play-by-play-${play.actionNumber}`} style={{ padding: "0.5rem" }}>
                    <Grid container spacing={2}>
                      <Grid>
                        <div
                          style={{
                            width: "3rem",
                            height: "5rem",
                            display: "flex",
                            flexDirection: "column",
                            alignItems: "center",
                            justifyContent: "center",
                          }}
                        >
                          {gameClock.regulation !== prevGameClock?.regulation && gameClock.regulation !== undefined ? (
                            <div> {gameClock?.regulation}Q </div>
                          ) : undefined}
                          {gameClock.overTime !== prevGameClock?.overTime && gameClock.overTime !== undefined ? (
                            <div> {gameClock?.overTime}OT </div>
                          ) : undefined}
                          {index === 0 ? (
                            true
                          ) : gameDetail.playByPlay[index - 1].elapsedMs !== play.elapsedMs ? (
                            <div>
                              {gameClock?.minutes}:{gameClock?.seconds}
                            </div>
                          ) : undefined}
                        </div>
                      </Grid>
                      <Grid>
                        <Paper
                          sx={{
                            width: "calc(90dvw - 3rem)",
                            height: "5rem",
                            padding: "0.5rem",
                            border:
                              play.teamId === gameDetail.homeTeam.teamId
                                ? "3px solid " + homeTeamColor + "88"
                                : play.teamId === gameDetail.awayTeam.teamId
                                  ? "3px solid " + awayTeamColor + "88"
                                  : "3px solid " + gameColor,
                          }}
                        >
                          <Grid container spacing={0}>
                            <Grid>
                              <div
                                style={{
                                  width: "3rem",
                                  height: "calc(4rem - 6px)",
                                  display: "flex",
                                  alignItems: "center",
                                  justifyContent: "center",
                                }}
                              >
                                <img
                                  src={
                                    play.playerId !== null
                                      ? `https://cdn.nba.com/headshots/nba/latest/260x190/${play.playerId}.png`
                                      : play.teamId === gameDetail.homeTeam.teamId
                                        ? gameDetail.homeTeam.teamLogo
                                        : play.teamId === gameDetail.awayTeam.teamId
                                          ? gameDetail.awayTeam.teamLogo
                                          : undefined
                                  }
                                />
                              </div>
                            </Grid>
                            <Grid>
                              <div
                                style={{
                                  width: "calc(90dvw - 8rem)",
                                  marginLeft: "0.5rem",
                                  height: "calc(4rem - 6px)",
                                  display: "flex",
                                  alignItems: "center",
                                }}
                              >
                                {play.description}
                              </div>
                            </Grid>
                          </Grid>
                        </Paper>
                      </Grid>
                    </Grid>
                  </div>
                );
              })}
            </div>
          ) : (
            noDataComponent
          )}
        </>
      ),
      color: gameColor,
    },
    {
      label: "Head-to-Head",
      item: (
        <>
          <div
            style={{
              height: "calc(100dvh - 17.5rem)",
              width: "100%",
              display: "grid",
              justifyItems: "center",
              alignContent: "start",
              overflowY: "scroll",
            }}
          >
            {headToheadGames
              .sort((a, b) => b.startDatetime.valueOf() - a.startDatetime.valueOf())
              .map((game) => {
                const isCurrent = game.gameId === gameDetail.gameId;
                return isCurrent ? (
                  <div
                    key={game.gameId}
                    ref={currentHeadToHeadRef}
                    style={{
                      width: "100%",
                      display: "grid",
                      justifyItems: "center",
                      alignContent: "start",
                    }}
                  >
                    <GameCard
                      key={game.gameId}
                      gameSummary={game}
                      inactive={true}
                      homeScore={hasStatsData ? homeBoxScoreData.filter((d) => d.isTeam)[0].points : undefined}
                      awayScore={hasStatsData ? awayBoxScoreData.filter((d) => d.isTeam)[0].points : undefined}
                    />
                  </div>
                ) : (
                  <GameCard key={game.gameId} gameSummary={game} />
                );
              })}
          </div>
        </>
      ),
      color: gameColor,
    },
  ];

  return (
    <>
      <div
        style={{
          height: "11rem",
          width: "100%",
          overflowY: "hidden",
          display: "grid",
          justifyItems: "center",
          alignContent: "start",
        }}
      >
        <GameCard
          key={gameDetail.gameId}
          gameSummary={gameDetail}
          homeScore={hasStatsData ? homeBoxScoreData.filter((d) => d.isTeam)[0].points : undefined}
          awayScore={hasStatsData ? awayBoxScoreData.filter((d) => d.isTeam)[0].points : undefined}
        />
      </div>
      <FullWidthTab
        tabItems={tabItems}
        defaultIndex={tabItems.findIndex((t) => t.label === "Box-Score")}
        onChange={onTabChange}
      />
    </>
  );
}

import {
  Box,
  FormControl,
  FormControlLabel,
  InputLabel,
  MenuItem,
  Radio,
  RadioGroup,
  Select,
  type SelectChangeEvent,
} from "@mui/material";
import { alpha, useTheme } from "@mui/material/styles";

import { type ColDef, type ColGroupDef, type ValueGetterParams } from "ag-grid-community";
import { type ReactNode, useState } from "react";
import { useSearchParams } from "react-router";

import { regularSeasonTeamStandingsApi } from "../api/teams.api";
import CustomTable from "../components/CustomTable";
import FullWidthTab, { type TabItem } from "../components/FullWidthTab";
import { Conferences, Divisions, SeasonTypes, TeamCategories } from "../types/leagueStructure";
import { type Season } from "../types/season";
import { type RegularSeasonTeamStandings } from "../types/teams";
import { generateSeasons, toSeason } from "../util/season";
import { type Route } from "./+types/teams";

const QueryParameterKeys = {
  Season: "season",
  SeasonType: "season-type",
} as const;

type QueryParameterKeys = (typeof QueryParameterKeys)[keyof typeof QueryParameterKeys];

interface TabItemWithQuery extends TabItem {
  query: SeasonTypes;
}

/**
 * Teams 画面のクライアントローダーを定義します.
 */
export async function clientLoader({ request }: Route.ClientLoaderArgs): Promise<RegularSeasonTeamStandings> {
  const url = new URL(request.url);
  const season = url.searchParams.get(QueryParameterKeys.Season) ?? generateSeasons()[0];
  const seasonType = url.searchParams.get(QueryParameterKeys.SeasonType) ?? SeasonTypes.Regular;
  regularSeasonTeamStandingsApi.path = `/standings/${seasonType}/${season}`;
  return await regularSeasonTeamStandingsApi.getOne();
}

/**
 * Teams 画面を定義します.
 */
export default function Teams({ loaderData }: Route.ComponentProps) {
  // ----------------------------------------------------------------------
  // Loadings
  // ----------------------------------------------------------------------
  const regularSeasonTeamStandings: RegularSeasonTeamStandings = loaderData;
  const teamsGroupedByConference = regularSeasonTeamStandings.teamStandingsByConference;
  const teamsGroupedByDivision = regularSeasonTeamStandings.teamStandingsByDivision;

  // ----------------------------------------------------------------------
  // States
  // ----------------------------------------------------------------------
  const [searchParams, setSearchParams] = useSearchParams();

  const seasons: Season[] = generateSeasons();
  const [season, setSeason] = useState<Season>(toSeason(searchParams.get(QueryParameterKeys.Season) ?? seasons[0]));

  const [groupBy, setGroupBy] = useState<TeamCategories>(TeamCategories.Conference);

  // ----------------------------------------------------------------------
  // Events
  // ----------------------------------------------------------------------
  const seasonChange = (event: SelectChangeEvent) => {
    setSeason(toSeason(event.target.value));
    setSearchParams(
      (prev) => {
        prev.set(QueryParameterKeys.Season, event.target.value);
        return prev;
      },
      { replace: true },
    );
  };

  const onChangeSeasonType = (selectedItemIndex: number) => {
    setSearchParams(
      (prev) => {
        prev.set(QueryParameterKeys.SeasonType, tabItems[selectedItemIndex].query);
        return prev;
      },
      { replace: true },
    );
  };

  const onChangeGroupBy = (event: React.ChangeEvent<HTMLInputElement, Element>) => {
    const groupBy = event.target.value as TeamCategories;
    setGroupBy(groupBy);
    setRegularSeasonContents(regularSeasonTeamStandingsView(groupBy));
  };

  // ----------------------------------------------------------------------
  // Views
  // ----------------------------------------------------------------------
  const baseStatsColDefs: ColDef[] = [
    { field: "pts", headerName: "PTS" },
    { field: "ast", headerName: "AST" },
    { field: "reb", headerName: "REB" },
    { field: "stl", headerName: "STL" },
    { field: "blk", headerName: "BLK" },
    { field: "fgM", headerName: "FGM" },
    { field: "fgA", headerName: "FGA" },
    { field: "fgP", headerName: "FG%" },
    { field: "threeM", headerName: "3PM" },
    { field: "threeA", headerName: "3PA" },
    { field: "threeP", headerName: "3P%" },
    { field: "ftM", headerName: "FTM" },
    { field: "ftA", headerName: "FTA" },
    { field: "ftP", headerName: "FT%" },
    { field: "oreb", headerName: "OREB" },
    { field: "dreb", headerName: "DREB" },
    { field: "to", headerName: "TO" },
    { field: "pf", headerName: "PF" },
    { field: "eff", headerName: "EFF" },
    { field: "pm", headerName: "+/-" },
  ];
  const columnDefs: (ColDef | ColGroupDef)[] = [
    {
      field: "team",
      headerName: "Team",
      resizable: true,
      pinned: "left",
      sortable: false,
      lockPinned: true,
      cellRenderer: (params: ValueGetterParams) => (
        <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
          <span style={{ paddingRight: 1 }}>{params.data.rank}</span>
          <img src={params.data.teamLogo} alt={params.data.teamName} width={24} height={24} />
          <span>{params.data.teamTricode}</span>
        </div>
      ),
    },
    { field: "win", headerName: "W", sortable: false },
    { field: "lose", headerName: "L", sortable: false },
    { field: "gb", headerName: "GB", sortable: false },
    { field: "rate", headerName: "W%" },
    { field: "gp", headerName: "GP", sortable: false },
    { headerName: "Stats /Game", children: baseStatsColDefs },
  ];

  const theme = useTheme();
  const regularSeasonTeamStandingsView: (groupBy: TeamCategories) => ReactNode = (groupBy) => {
    switch (groupBy) {
      case TeamCategories.All:
        return <CustomTable columnDefs={columnDefs} data={regularSeasonTeamStandings.teamStandings} />;
      case TeamCategories.Conference:
        return (
          <>
            {Object.values(Conferences).map((conference) => (
              <>
                <Box sx={{ backgroundColor: alpha(theme.palette.grey[200], 1), paddingLeft: 3 }}>{conference}</Box>
                <CustomTable columnDefs={columnDefs} data={teamsGroupedByConference[conference] ?? []} />
              </>
            ))}
          </>
        );
      case TeamCategories.Division:
        return (
          <>
            {Object.values(Divisions).map((division) => (
              <>
                <Box sx={{ backgroundColor: alpha(theme.palette.grey[200], 1), paddingLeft: 3 }}>{division}</Box>
                <CustomTable columnDefs={columnDefs} data={teamsGroupedByDivision[division] ?? []} />
              </>
            ))}
          </>
        );
    }
  };
  const [reguularSeasonContents, setRegularSeasonContents] = useState<ReactNode>(
    regularSeasonTeamStandingsView(groupBy),
  );

  const tabItems: TabItemWithQuery[] = [
    {
      label: "Regular Season",
      query: SeasonTypes.Regular,
      item: (
        <>
          <RadioGroup sx={{ paddingLeft: 3 }} row onChange={onChangeGroupBy} value={groupBy}>
            <FormControlLabel value={TeamCategories.All} control={<Radio />} label="All" />
            <FormControlLabel value={TeamCategories.Conference} control={<Radio />} label="Conference" />
            <FormControlLabel value={TeamCategories.Division} control={<Radio />} label="Division" />
          </RadioGroup>
          {reguularSeasonContents}
        </>
      ),
    },
    { label: "Playoffs", query: SeasonTypes.Playoffs, item: <>準備中</>, disabled: true },
  ];
  const defaultTabIndex = Math.max(
    0,
    tabItems.findIndex((item) => item.query === searchParams.get(QueryParameterKeys.SeasonType)),
  );

  return (
    <>
      <FormControl sx={{ width: "100%" }}>
        <InputLabel id="season-select-label">Season</InputLabel>
        <Select labelId="season-select-label" id="season-select" value={season} label="Season" onChange={seasonChange}>
          {seasons.map((season) => (
            <MenuItem key={season} value={season}>
              {season}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      <FullWidthTab tabItems={tabItems} defaultIndex={defaultTabIndex} onChange={onChangeSeasonType} />
    </>
  );
}

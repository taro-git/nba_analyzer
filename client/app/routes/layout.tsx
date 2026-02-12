import * as Icon from "@mui/icons-material";
import BottomNavigation from "@mui/material/BottomNavigation";
import BottomNavigationAction from "@mui/material/BottomNavigationAction";
import Box from "@mui/material/Box";
import CssBaseline from "@mui/material/CssBaseline";
import Paper from "@mui/material/Paper";

import * as React from "react";
import { Outlet, useNavigate } from "react-router";

/**
 * 全画面共通のレイアウト
 */
export default function Layout() {
  const [value, setValue] = React.useState(0);
  const navigate = useNavigate();
  const ref = React.useRef<HTMLDivElement>(null);

  return (
    <Box sx={{ pb: 7, pt: 2 }} ref={ref}>
      <CssBaseline />

      <Outlet />

      <Paper sx={{ position: "fixed", bottom: 0, left: 0, right: 0 }} elevation={10}>
        <BottomNavigation
          showLabels
          value={value}
          onChange={(_, newValue) => {
            setValue(newValue);
            navigate(newValue);
          }}
        >
          <BottomNavigationAction label="Teams" value="teams" icon={<Icon.Diversity2 />} />
          <BottomNavigationAction label="Players" value="players" icon={<Icon.Person />} />
          <BottomNavigationAction label="Games" value="games" icon={<Icon.SportsBasketballSharp />} />
          <BottomNavigationAction label="Analysis" value="analysis" icon={<Icon.QueryStats />} />
          <BottomNavigationAction label="Settings" value="settings" icon={<Icon.Settings />} />
        </BottomNavigation>
      </Paper>
    </Box>
  );
}

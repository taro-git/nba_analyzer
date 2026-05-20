import Box from "@mui/material/Box";
import { useColorScheme } from "@mui/material/styles";
import Tab from "@mui/material/Tab";
import Tabs from "@mui/material/Tabs";

import * as React from "react";
import { type ReactNode, useMemo } from "react";

import { theme } from "../routes/layout";

interface TabPanelProps {
  children?: React.ReactNode;
  dir?: string;
  index: number;
  selectedIndex: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, selectedIndex, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={selectedIndex !== index}
      id={`full-width-tabpanel-${index}`}
      aria-labelledby={`full-width-tab-${index}`}
      {...other}
    >
      {selectedIndex === index && <Box sx={{ p: 0, height: "100%" }}>{children}</Box>}
    </div>
  );
}

function a11yProps(index: number) {
  return {
    id: `full-width-tab-${index}`,
    "aria-controls": `full-width-tabpanel-${index}`,
  };
}

/**
 * タブコンテンツ.
 */
export interface TabItem {
  label: string;
  item: ReactNode;
  disabled?: boolean;
  color?: string;
}

/**
 * 横幅が最大値となるタブと配下のタブコンテンツを表示します.
 *
 * @param {TabItem[]} tabItems - タブコンテンツの配列.
 * @param {number} defaultIndex - デフォルトで表示するタブコンテンツのインデックス.
 * @param {(selectedItemIndex: number) => void} onChange - タブコンテンツのインデックスが変更されたときに呼び出されるコールバック関数.
 *
 * @returns {JSX.Element} - タブコンポーネント
 */
export default function FullWidthTab({
  tabItems,
  defaultIndex,
  onChange,
  tabShape,
}: {
  tabItems: TabItem[];
  defaultIndex: number;
  onChange: (selectedItemIndex: number) => void;
  tabShape?: {
    height?: number | string;
    width?: number | string;
  };
}) {
  const systemMode = useColorScheme().systemMode;
  const palette = useMemo(() => {
    return systemMode === "light" ? theme.colorSchemes.light?.palette : theme.colorSchemes.dark?.palette;
  }, [systemMode]);
  const [selectedItemIndex, setSelectedItemIndex] = React.useState(defaultIndex);
  const tabHeight = tabShape?.height ?? "3rem";
  const tabColors = tabItems.reduce<Record<number, string | undefined>>((acc, cur, index) => {
    acc[index] = cur.color;
    return acc;
  }, {});

  const handleChange = (event: React.SyntheticEvent, selectedItemIndex: number) => {
    setSelectedItemIndex(selectedItemIndex);
    onChange(selectedItemIndex);
  };

  return (
    <div style={{ width: "100%", height: "100%", display: "grid", justifyItems: "center", alignContent: "start" }}>
      <Tabs
        sx={{ width: tabShape?.width ?? "100%", minHeight: tabHeight ?? "3rem" }}
        value={selectedItemIndex}
        onChange={handleChange}
        variant="fullWidth"
        aria-label="full width tabs example"
        slotProps={{
          indicator: {
            style: {
              backgroundColor: tabColors[selectedItemIndex],
            },
          },
        }}
      >
        {tabItems.map((tab, index) => (
          <Tab
            sx={{
              height: tabHeight ?? "3rem",
              minHeight: tabHeight ?? "3rem",
              "&.Mui-selected": {
                fontWeight: "bold",
                color: tabColors[index] !== undefined ? palette?.text.primary : palette?.primary.main,
                textShadow: "0 0 2px" + tabColors[index],
              },
            }}
            key={index}
            label={tab.label}
            {...a11yProps(index)}
            disabled={tab.disabled ?? false}
          />
        ))}
      </Tabs>
      <div style={{ width: "100%", height: "100%" }}>
        {tabItems.map((tab, index) => (
          <TabPanel key={index} selectedIndex={selectedItemIndex} index={index} dir={theme.direction}>
            {tab.item}
          </TabPanel>
        ))}
      </div>
    </div>
  );
}

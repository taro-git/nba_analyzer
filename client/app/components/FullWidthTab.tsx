import Box from "@mui/material/Box";
import { useTheme } from "@mui/material/styles";
import Tab from "@mui/material/Tab";
import Tabs from "@mui/material/Tabs";

import * as React from "react";
import type { ReactNode } from "react";

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
}: {
  tabItems: TabItem[];
  defaultIndex: number;
  onChange: (selectedItemIndex: number) => void;
}) {
  const theme = useTheme();
  const [selectedItemIndex, setSelectedItemIndex] = React.useState(defaultIndex);

  const handleChange = (event: React.SyntheticEvent, selectedItemIndex: number) => {
    setSelectedItemIndex(selectedItemIndex);
    onChange(selectedItemIndex);
  };

  return (
    <Box sx={{ bgcolor: "background.paper", width: "100%", height: "100%" }}>
      <Tabs value={selectedItemIndex} onChange={handleChange} variant="fullWidth" aria-label="full width tabs example">
        {tabItems.map((tab, index) => (
          <Tab key={index} label={tab.label} {...a11yProps(index)} disabled={tab.disabled ?? false} />
        ))}
      </Tabs>
      {tabItems.map((tab, index) => (
        <TabPanel key={index} selectedIndex={selectedItemIndex} index={index} dir={theme.direction}>
          {tab.item}
        </TabPanel>
      ))}
    </Box>
  );
}

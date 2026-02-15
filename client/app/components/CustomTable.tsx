import Box from "@mui/material/Box";
import { useColorScheme } from "@mui/material/styles";

import { type ColDef, themeQuartz } from "ag-grid-community";
import { AgGridReact } from "ag-grid-react";
import { useMemo, useRef } from "react";

import { theme } from "../routes/layout";
import "./styles.css";

/**
 * nba_analyzer 向けのテーブルコンポーネントです.
 */
export default function CustomTable<Data>({
  columnDefs,
  data,
  degree,
}: {
  columnDefs: ColDef[];
  data: Data[];
  degree: "warm" | "cold" | undefined;
}) {
  const columnTypes = {
    centerAligned: {
      cellStyle: { textAlign: "center" },
    },
  };
  const gridRef = useRef<AgGridReact<Data>>(null);
  const defaultColDef: ColDef = {
    resizable: false,
    suppressHeaderMenuButton: true,
    lockPosition: true,
    lockVisible: true,
  };
  const systemMode = useColorScheme().systemMode;

  const lightTheme = themeQuartz.withParams({
    backgroundColor: theme.colorSchemes.light?.palette.getContrastText(degree ?? ""),
    textColor: theme.colorSchemes.light?.palette.text.primary,
  });
  const darkTheme = themeQuartz.withParams({
    backgroundColor: theme.colorSchemes.dark?.palette.getContrastText(degree ?? ""),
    textColor: theme.colorSchemes.dark?.palette.text.primary,
  });

  const gridTheme = useMemo(() => {
    return systemMode === "light" ? lightTheme : darkTheme;
  }, [systemMode]);
  return (
    <Box sx={{ height: "100%", width: "100%" }}>
      <AgGridReact<Data>
        key={`${data}`}
        theme={gridTheme}
        ref={gridRef}
        rowData={data}
        defaultColDef={defaultColDef}
        columnDefs={columnDefs}
        domLayout="autoHeight"
        rowHeight={28}
        headerHeight={28}
        onFirstDataRendered={(params) => {
          params.api.autoSizeAllColumns(true);
        }}
        columnTypes={columnTypes}
        autoSizeStrategy={{ type: "fitCellContents" }}
        suppressRowHoverHighlight={true}
      />
    </Box>
  );
}

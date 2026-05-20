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
  height,
  width,
  headerColor,
}: {
  columnDefs: ColDef[];
  data: Data[];
  degree: "warm" | "cold" | undefined;
  height?: number | string;
  width?: number | string;
  headerColor?: string;
}) {
  const columnTypes = {
    centerAligned: {
      cellStyle: { textAlign: "center" },
      headerClass: "ag-center-header",
    },
  };
  const gridRef = useRef<AgGridReact<Data>>(null);
  const defaultColDef: ColDef = {
    resizable: false,
    suppressHeaderMenuButton: true,
    lockPosition: true,
    lockVisible: true,
    flex: width ? 1 : undefined,
  };
  const systemMode = useColorScheme().systemMode;

  const lightTheme = themeQuartz.withParams({
    backgroundColor: theme.colorSchemes.light?.palette.getContrastText(degree ?? ""),
    textColor: theme.colorSchemes.light?.palette.text.primary,
    headerBackgroundColor: headerColor ?? undefined,
    headerColumnResizeHandleWidth: 5,
    headerColumnResizeHandleColor: theme.colorSchemes.light?.palette.text.primary,
  });
  const darkTheme = themeQuartz.withParams({
    backgroundColor: theme.colorSchemes.dark?.palette.getContrastText(degree ?? ""),
    textColor: theme.colorSchemes.dark?.palette.text.primary,
    headerBackgroundColor: headerColor ?? undefined,
    headerColumnResizeHandleWidth: 5,
    headerColumnResizeHandleColor: theme.colorSchemes.dark?.palette.text.primary,
  });

  const gridTheme = useMemo(() => {
    return systemMode === "light" ? lightTheme : darkTheme;
  }, [systemMode]);
  return (
    <Box sx={{ height: height ?? "100%", width: width ?? "100%" }}>
      <AgGridReact<Data>
        theme={gridTheme}
        ref={gridRef}
        rowData={data}
        defaultColDef={defaultColDef}
        columnDefs={columnDefs}
        domLayout={height ? undefined : "autoHeight"}
        rowHeight={28}
        headerHeight={28}
        onFirstDataRendered={(params) => {
          if (width) params.api.sizeColumnsToFit();
          if (!width) params.api.autoSizeAllColumns(true);
        }}
        columnTypes={columnTypes}
        autoSizeStrategy={width ? undefined : { type: "fitCellContents" }}
        suppressRowHoverHighlight={true}
      />
    </Box>
  );
}

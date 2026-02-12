import Box from "@mui/material/Box";

import { type ColDef } from "ag-grid-community";
import { AgGridReact } from "ag-grid-react";
import { useRef } from "react";

import "./styles.css";

/**
 * nba_analyzer 向けのテーブルコンポーネントです.
 */
export default function CustomTable<Data>({ columnDefs, data }: { columnDefs: ColDef[]; data: Data[] }) {
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
  return (
    <Box sx={{ height: "100%", width: "100%" }}>
      <AgGridReact<Data>
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
      />
    </Box>
  );
}

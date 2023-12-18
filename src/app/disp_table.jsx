import React from "react";
import { useTable } from "react-table";

const StockDataTable = ({ data }) => {
  // Extract keys (Open, High, Low, Close, Adj Close, Volume)
  const keys = Object.keys(data);

  // Extract timestamps
  const timestamps = Object.keys(data[keys[0]]);

  // Extract rows
  const rows = timestamps.map((timestamp) => {
    const row = {
      Timestamp: new Date(parseInt(timestamp)).toLocaleDateString(),
    };
    keys.forEach((key) => {
      row[key] = data[key][timestamp];
    });
    return row;
  });

  const columns = React.useMemo(() => {
    return [
      {
        Header: "Timestamp",
        accessor: "Timestamp",
      },
      ...keys.map((key) => ({
        Header: key,
        accessor: key,
      })),
    ];
  }, [keys]);

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows: tableRows,
    prepareRow,
  } = useTable({
    columns,
    data: rows,
  });

  return (
    <div style={{ overflowX: "auto" }}>
      <table {...getTableProps()} style={{ width: "100%" }}>
        <thead>
          {headerGroups.map((headerGroup) => (
            <tr key={headerGroup.id} {...headerGroup.getHeaderGroupProps()}>
              {headerGroup.headers.map((column) => (
                <th key={column.id} {...column.getHeaderProps()}>
                  {column.render("Header")}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody {...getTableBodyProps()}>
          {tableRows.map((row) => {
            prepareRow(row);
            return (
              <tr key={row.id} {...row.getRowProps()}>
                {row.cells.map((cell) => (
                  <td key={cell.column.id} {...cell.getCellProps()}>
                    {cell.render("Cell")}
                  </td>
                ))}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

export default StockDataTable;

"use client";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/registry/new-york/ui/table";
import { Badge } from "@/registry/new-york/ui/badge";
import { HexPalette, TWPalette } from "@/libs/colors";

import { useEffect, useState } from "react";

// @ts-ignore
export default function Recommendations({ data }) {
  const [dc, setDC] = useState({});
  useEffect(() => {
    console.log("asd", data);
    let decision_count: any = {};
    data.map((d) => {
      //   console.log("dc count: " + decision_count);
      decision_count[d.decision] = (decision_count[d.decision] || 0) + 1;
    });
    setDC(decision_count);
  }, []);
  // console.log("ok");
  // console.log(data);
  console.log("dc: ", dc);
  return (
    <>
      <div className="pb-4">
        {dc &&
          Object.keys(dc).map((d) => {
            console.log(`bg${TWPalette[d]}`);
            return (
              <Badge style={{ "background": HexPalette[d] }} className={``}>
                {dc[d]}
              </Badge>
            );
          })}
      </div>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Rule</TableHead>
            <TableHead>Decision</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {data.map((d) => {
            return (
              <TableRow>
                <TableCell>{d.rule_id}</TableCell>
                <TableCell
                  style={{ "color": HexPalette[d.decision] }}
                  className={`capitalize font-semibold`}
                >
                  {d.decision.toLowerCase().replaceAll("_", " ")}
                </TableCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
    </>
  );
}

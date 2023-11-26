"use client";

import { ColumnDef } from "@tanstack/react-table";
import { Badge } from "@/registry/new-york/ui/badge";
import { timeSince } from "@/libs/timeSince";
import { HexPalette, TWPalette } from "@/libs/colors";

// This type is used to define the shape of our data.
// You can use a Zod schema here if you want.
export type Payment = {
  id: string;
  amount: number;
  status: "pending" | "processing" | "success" | "failed";
  email: string;
};

export const columns: ColumnDef<Payment>[] = [
  {
    accessorKey: "id",
    header: "Id",
  },
  {
    accessorKey: "name",
    header: "Name",
  },
  {
    accessorKey: "active",
    header: "Active",
    cell: ({ row }) => {
      return (
        <div>
          <Badge
            className=""
            style={{
              "background": row.getValue("active")
                ? HexPalette["ACCEPTED"] + "D9"
                : HexPalette["REJECTED"] + "D9",
            }}
          >
            {row.getValue("active") ? "active" : "inactive"}
          </Badge>
          {/* {row.getValue("active")} */}
        </div>
      );
    },
  },
  {
    accessorKey: "desc",
    header: "Description",
  },
  {
    accessorKey: "lastUpdated",
    header: "Last Updated",
    cell: ({ row }) => {
      return (
        <div className="p-1">{timeSince(row.getValue("lastUpdated"))} ago</div>
      );
    },
  },

];

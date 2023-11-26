"use client";

import { ColumnDef } from "@tanstack/react-table";

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
    accessorKey: "LOType",
    header: "Type",
  },
  {
    accessorKey: "approvalStatus",
    header: "Status",
    cell: ({ row }) => (
        <div
            className={` border-[1px]  p-1 w-fit rounded-lg  capitalize 
        ${
                row.getValue("approvalStatus") == "PENDING" &&
                "border-orange-500 bg-orange-500/20"
            }
        ${
                row.getValue("approvalStatus") == "ACCEPTED" &&
                "border-green-500 bg-green-500/20"
            }
        ${
                row.getValue("approvalStatus") == "REJECTED" &&
                "border-red-500 bg-red-500/20"
            }
        ${
                row.getValue("approvalStatus") == "AUTO_ACCEPTED" &&
                "border-blue-400 bg-blue-400/20"
            }
        ${
                row.getValue("approvalStatus") == "AUTO_REJECTED" &&
                "border-purple-600 bg-purple-600/20"
            }
        ${
                row.getValue("approvalStatus") == "MANUAL_CHECK_REQUIRED" &&
                "border-amber-400 bg-amber-400/20"
            }
        `}
        >
          {row.getValue("approvalStatus").toLowerCase().replaceAll("_", " ")}
        </div>
    ),
  },
  {
    accessorKey: "requestedAt",
    header: "Requested At",
  },
];


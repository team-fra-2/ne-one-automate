"use client";
import {timeSince} from "@/libs/timeSince";

import {Table, TableBody, TableCell, TableRow,} from "@/registry/new-york/ui/table";

// @ts-ignore
export default function Info ({data}) {
  return (
      <>
        <Table>
          {/* <TableCaption>A list of your recent invoices.</TableCaption> */}
          <TableBody>
            <TableRow>
              <TableCell className="font-medium">Change Request ID</TableCell>
              <TableCell>{data && data["_id"]}</TableCell>
            </TableRow>
            <TableRow>
              <TableCell className="font-medium">Status</TableCell>
              <TableCell className={"capitalize"}>{data && data["approvalStatus"].toLowerCase().replaceAll("_"," ")}</TableCell>
            </TableRow>
            <TableRow>
              <TableCell className="font-medium">Revision Number</TableCell>
              <TableCell>
                {data &&
                    data["https://onerecord.iata.org/ns/api#hasChange"][
                        "https://onerecord.iata.org/ns/api#hasRevision"
                        ]}
              </TableCell>
            </TableRow>
            <TableRow>
              <TableCell className="font-medium">Requested By</TableCell>
              <TableCell>
                {data &&
                    data["https://onerecord.iata.org/ns/api#isRequestedBy"]["@id"]}
              </TableCell>
            </TableRow>
            <TableRow>
              <TableCell className="font-medium">Requested At</TableCell>
              <TableCell>
                {data && (
                    <>
                      {timeSince(
                          data["https://onerecord.iata.org/ns/api#isRequestedAt"]
                      )}{" "}
                      ago
                      <div className="text-xs mt-1">
                        ({data["https://onerecord.iata.org/ns/api#isRequestedAt"]})
                      </div>
                    </>
                )}
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </>
  );
}

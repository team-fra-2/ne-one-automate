"use client";

import { useParams } from "next/navigation";
import React, { useState, useEffect } from "react";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/registry/new-york/ui/card";
import { Button } from "@/registry/new-york/ui/button";
import Info from "./info";
import Diff from "./diff";
import { siteConfig } from "@/config/site";
import Recommendations from "@/app/change-requests/[id]/recommendations";

export default function Page() {
  const [data, setData] = useState(null);

  const { id } = useParams() || {};

  useEffect(() => {
    if (id === null) return;
    fetch(`${siteConfig.backend}/change-requests/${id}`)
      .then((d) => {
        return d.json();
      })
      .then((d) => {
        setData(d);
      });
  }, []);

  return (
    <>
      <div className="container hidden h-full flex-col md:flex">
        <div className="flex-1 space-y-4 p-2 pt-6">
          <div className="flex items-center justify-between space-y-2">
            <h2 className="text-3xl font-bold tracking-tight">
              Change Request Approval
            </h2>
            <div className="flex items-center space-x-2">
              <Button
                className="bg-red-500 hover:bg-red-600 transition-all duration-500"
                onClick={() => {
                  const payload = {
                    approval_status: "REJECTED",
                    comment: "comment",
                  };
                  try {
                    const response = fetch(
                      siteConfig.backend +
                        "/change-requests/" +
                        id +
                        "/approve",
                      {
                        method: "POST",
                        headers: {
                          "Content-Type": "application/json",
                        },
                        body: JSON.stringify(payload),
                      }
                    );
                  } catch (error) {
                    console.error("There was an error!", error);
                  }
                }}
              >
                Reject
              </Button>
              <Button
                className="bg-orange-500 hover:bg-orange-700 transition-all duration-500"
                onClick={() => {}}
              >
                Not My Problem
              </Button>
              <Button
                className="bg-green-500 hover:bg-green-600 transition-all duration-500"
                onClick={() => {
                  const payload = {
                    approval_status: "ACCEPTED",
                    comment: "comment",
                  };

                  try {
                    const response = fetch(
                      siteConfig.backend +
                        "/change-requests/" +
                        id +
                        "/approve",
                      {
                        method: "POST",
                        headers: {
                          "Content-Type": "application/json",
                        },
                        body: JSON.stringify(payload),
                      }
                    );
                  } catch (error) {
                    console.error("There was an error!", error);
                  }
                }}
              >
                Accept
              </Button>
            </div>
          </div>
        </div>

        <Card className="mb-6">
          <CardHeader>
            <CardTitle>General Information</CardTitle>
          </CardHeader>
          <CardContent>
            <>
              <Info data={data} />
            </>
          </CardContent>
        </Card>
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Data Change Overview</CardTitle>
            <CardDescription>
              The following list shows all changed properties
            </CardDescription>
          </CardHeader>
          <CardContent>
            <>{data && <Diff data={data} />}</>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Recommendations</CardTitle>
            <CardDescription>
              The following list shows all applied rules and their decisions
            </CardDescription>
          </CardHeader>
          <CardContent>
            <>{data && <Recommendations data={data["recommendations"]} />}</>
          </CardContent>
        </Card>
      </div>
    </>
  );
}

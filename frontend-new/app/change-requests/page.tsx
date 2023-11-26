import {columns} from "./columns";
import {DataTable} from "./data-table";
import {timeSince} from "@/libs/timeSince.js";
import PageNavigation from "./pageNavigation";

import {
    Tabs,
    TabsContent,
    TabsList,
    TabsTrigger,
} from "@/registry/new-york/ui/tabs";
import {siteConfig} from "@/config/site";
import {CalendarDateRangePicker} from "@/app/dashboard/components/date-range-picker";
import {Button} from "@/registry/new-york/ui/button";

// @ts-ignore
export default async function DemoPage({searchParams}) {
    // @ts-ignore
    const getData = async (isPendingOnly) => {
        let wantedStates = [];
        if (isPendingOnly === true) {
            wantedStates.push("PENDING");
        }
        const page = searchParams.page || 1;
        let fetch_params: Record<string, any> = {};
        fetch_params = {
            skip: (page - 1) * 10,
            limit: 10,
        };


        if (Object.keys(wantedStates).length > 0) {
            fetch_params["states"] = wantedStates;
        }
        // console.log("params obj: ", fetch_params);
        console.log(
            "fetch url: ",
            siteConfig.backend +
            "/change-requests?" +
            new URLSearchParams(fetch_params)
        );
        let fetched_data = await fetch(
            siteConfig.backend +
            "/change-requests?" +
            new URLSearchParams(fetch_params),
            {cache: "no-cache"}
        );
        fetched_data = await fetched_data.json();


        const data_short = fetched_data.map((d) => {
            return {
                id: d["_id"],
                LOType: d["originalLogisticsObject"]["@type"].split("#").at(-1),
                approvalStatus: d["approvalStatus"],
                requestedAt:
                    timeSince(d["https://onerecord.iata.org/ns/api#isRequestedAt"]) +
                    " ago"

            };
        });
        console.log(data_short);
        return data_short;
    };

    return (
        <div className="container hidden flex-col md:flex">
            <div className="flex-1 space-y-4 p-2 pt-6">
                <div className="flex items-center justify-between space-y-2">
                    <h2 className="text-3xl font-bold tracking-tight">Change Requests</h2>
                </div>
                <Tabs defaultValue="all" className="">
                    <TabsList>
                        <TabsTrigger value="all">All</TabsTrigger>
                        <TabsTrigger value="pending">Pending</TabsTrigger>
                    </TabsList>
                    <TabsContent value="pending">
                        <>
                            <div className="container mx-auto py-10">
                                <DataTable columns={columns} data={await getData(true)}/>
                            </div>
                            <PageNavigation/>
                        </>
                    </TabsContent>
                    <TabsContent value="all">
                        <>
                            <div className="container mx-auto py-10">
                                <DataTable columns={columns} data={await getData(false)}/>
                            </div>
                            <PageNavigation/>
                        </>
                    </TabsContent>
                </Tabs>
            </div>
        </div>
    );
}

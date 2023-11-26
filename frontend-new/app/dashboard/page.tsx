import {Metadata} from "next"
import {Card, CardContent, CardHeader, CardTitle,} from "@/registry/new-york/ui/card"
import {Tabs, TabsContent, TabsList, TabsTrigger,} from "@/registry/new-york/ui/tabs"
import {Overview} from "@/app/dashboard/components/overview"
import {Overview2} from "@/app/dashboard/components/overview-2"
import {CubeIcon, EnvelopeClosedIcon, GearIcon, LapTimerIcon} from "@radix-ui/react-icons";
import {CalendarDateRangePicker} from "@/app/dashboard/components/date-range-picker";
import {Button} from "@/registry/new-york/ui/button";


export const metadata: Metadata = {
    title: "Dashboard",
    description: "Example dashboard app built using the components.",
}

export default function DashboardPage() {
    return (
        <>
            <div className="container hidden flex-col md:flex">
                <div className="flex-1 space-y-4 p-2 pt-6">
                    <div className="flex items-center justify-between space-y-2">
                        <h2 className="text-3xl font-bold tracking-tight">Dashboard</h2>
                        <div className="flex items-center space-x-2">
                            <CalendarDateRangePicker/>
                            <Button>Apply</Button>
                        </div>
                    </div>
                    <Tabs defaultValue="overview" className="space-y-4">
                        <TabsList>
                            <TabsTrigger value="overview">Overview</TabsTrigger>
                            <TabsTrigger value="analytics" disabled>
                                Analytics
                            </TabsTrigger>
                            <TabsTrigger value="reports" disabled>
                                Reports
                            </TabsTrigger>
                            <TabsTrigger value="notifications" disabled>
                                Notifications
                            </TabsTrigger>
                        </TabsList>
                        <TabsContent value="overview" className="space-y-4">
                            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                                <Card>
                                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                        <CardTitle className="text-sm font-medium">
                                            # Change Requests
                                        </CardTitle>
                                        <CubeIcon className={"h-4 w-4 text-muted-foreground"}/>
                                    </CardHeader>
                                    <CardContent>
                                        <div className="text-2xl font-bold">45,435</div>
                                        <p className="text-xs text-muted-foreground">
                                            +20.1% from last month
                                        </p>
                                    </CardContent>
                                </Card>
                                <Card>
                                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                        <CardTitle className="text-sm font-medium">
                                            Auto / Manual - Ratio
                                        </CardTitle>
                                        <GearIcon className={"h-4 w-4 text-muted-foreground"}/>
                                    </CardHeader>
                                    <CardContent>
                                        <div className="text-2xl font-bold">78% / 22%</div>
                                        <p className="text-xs text-muted-foreground">
                                            +180.1% more auto-processing from last month
                                        </p>
                                    </CardContent>
                                </Card>
                                <Card>
                                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                        <CardTitle className="text-sm font-medium">Avg. Reaction Time</CardTitle>
                                        <LapTimerIcon className={"h-4 w-4 text-muted-foreground"}/>
                                    </CardHeader>
                                    <CardContent>
                                        <div className="text-2xl font-bold">3.2 min</div>
                                        <p className="text-xs text-muted-foreground">
                                            -19% from last month
                                        </p>
                                    </CardContent>
                                </Card>
                                <Card>
                                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                        <CardTitle className="text-sm font-medium">
                                            Pending Now
                                        </CardTitle>
                                        <EnvelopeClosedIcon className={"h-4 w-4 text-muted-foreground"}/>
                                    </CardHeader>
                                    <CardContent>
                                        <div className="text-2xl font-bold">573</div>
                                        <p className="text-xs text-muted-foreground">
                                            +201 since last hour
                                        </p>
                                    </CardContent>
                                </Card>
                            </div>
                            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
                                <Card className="col-span-4">
                                    <CardHeader>
                                        <CardTitle>Overview (Incoming ChangeRequests)</CardTitle>
                                    </CardHeader>
                                    <CardContent className="pl-2">
                                        <Overview/>
                                    </CardContent>
                                </Card>
                                <Card className="col-span-3">
                                    <CardHeader>
                                        <CardTitle>ChangeRequests per Status</CardTitle>
                                    </CardHeader>
                                    <CardContent className="pl-2">
                                        <Overview2/>
                                    </CardContent>
                                </Card>
                                {/*<Card className="col-span-3">*/}
                                {/*    <CardHeader>*/}
                                {/*        <CardTitle>Last accepted ChangeRequests</CardTitle>*/}
                                {/*        <CardDescription>*/}
                                {/*            You accepted 265 change requests today.*/}
                                {/*        </CardDescription>*/}
                                {/*    </CardHeader>*/}
                                {/*    <CardContent>*/}
                                {/*        <RecentSales/>*/}
                                {/*    </CardContent>*/}
                                {/*</Card>*/}
                            </div>
                        </TabsContent>
                    </Tabs>
                </div>
            </div>
        </>
    )
}

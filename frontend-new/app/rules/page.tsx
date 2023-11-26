import {DataTable} from "./data-table";
import {columns} from "./columns";
import {siteConfig} from "@/config/site";
import {CalendarDateRangePicker} from "@/app/dashboard/components/date-range-picker";
import {Button} from "@/registry/new-york/ui/button";

export default async function Rules() {

    // useEffect(() => {
    let fdata = await fetch(siteConfig.backend + "/rules");
    fdata = await fdata.json();

    let table_rules: any[] = [];
    fdata.map((r) => {
        table_rules.push({
            id: r._id,
            name: r.rule_id,
            active: r.active,
            lastUpdated: r.last_updated,
            desc: r.description,
        });
    });
    // console.log("rules2: " + rules2);
    // }, []);
    return (
        <main className="">
            <div className="container hidden flex-col md:flex">
                <div className="flex-1 space-y-4 p-2 pt-6">
                    <div className="flex items-center justify-between space-y-2">
                        <h2 className="text-3xl font-bold tracking-tight">Rules</h2>
                        <div className="flex items-center space-x-2">
                            <Button>Create rule</Button>
                        </div>
                    </div>
                    <DataTable columns={columns} data={table_rules}/>
                </div>
            </div>
        </main>
    );
}

import {siteConfig} from "@/config/site"
import {cn} from "@/lib/utils";

export function SiteFooter() {
    return (
        <footer className={cn("py-6 md:px-8 md:py-2")}>
            <div className="container flex flex-col items-center justify-between gap-4 md:h-8 md:flex-row">
                <p className="text-center text-sm leading-loose text-muted-foreground md:text-left">
                    Built by{" "}
                    <a
                        href={siteConfig.links.twitter}
                        target="_blank"
                        rel="noreferrer"
                        className="font-medium underline underline-offset-4"
                    >
                        Team FRA 2
                    </a>{" "}
                    during the <a href={"https://onerecord-doh.devpost.com/"}
                                  className={"font-medium underline underline-offset-4"} target={"_blank"}>HaQathon
                    2023</a> in DOH.
                    The source code is available on{" "}
                    <a
                        href={siteConfig.links.github}
                        target="_blank"
                        rel="noreferrer"
                        className="font-medium underline underline-offset-4"
                    >
                        GitHub
                    </a>
                    .
                </p>
            </div>
        </footer>
    )
}

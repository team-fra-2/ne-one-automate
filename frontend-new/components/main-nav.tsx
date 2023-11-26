"use client";

import * as React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";

import { siteConfig } from "@/config/site";
import { cn } from "@/lib/utils";
import Image from "next/image";

export function MainNav() {
  const pathname = usePathname();

  return (
    <div className="mr-4 hidden md:flex">
      <Link href="/" className="mr-6 flex items-center space-x-2 ">
        <Image
          className="rounded-md"
          src={"/logo.jpg"}
          alt={"ne-one automate Logo"}
          width={40}
          height={40}
        />
        <span className="hidden font-bold sm:inline-block">
          {siteConfig.name}
        </span>
      </Link>
      <nav className="flex items-center space-x-6 text-sm font-medium">
        <Link
          href="/"
          className={cn(
            "transition-colors hover:text-foreground/80",
            pathname === "/dashboard" ? "text-foreground" : "text-foreground/60"
          )}
        >
          Dashboard
        </Link>
        <Link
          href="/change-requests?page=1"
          className={cn(
            "transition-colors hover:text-foreground/80",
            pathname?.startsWith("/change-requests")
              ? "text-foreground"
              : "text-foreground/60"
          )}
        >
          Change Requests
        </Link>
        <Link
          href="/rules"
          className={cn(
            "transition-colors hover:text-foreground/80",
            pathname?.startsWith("/rules")
              ? "text-foreground"
              : "text-foreground/60"
          )}
        >
          Rules
        </Link>
        {/*<Link*/}
        {/*  href="/examples"*/}
        {/*  className={cn(*/}
        {/*    "transition-colors hover:text-foreground/80",*/}
        {/*    pathname?.startsWith("/examples")*/}
        {/*      ? "text-foreground"*/}
        {/*      : "text-foreground/60"*/}
        {/*  )}*/}
        {/*>*/}
        {/*  Examples*/}
        {/*</Link>*/}
        {/*<Link*/}
        {/*  href={siteConfig.links.github}*/}
        {/*  className={cn(*/}
        {/*    "hidden text-foreground/60 transition-colors hover:text-foreground/80 lg:block"*/}
        {/*  )}*/}
        {/*>*/}
        {/*  GitHub*/}
        {/*</Link>*/}
      </nav>
    </div>
  );
}

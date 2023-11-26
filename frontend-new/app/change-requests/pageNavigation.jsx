"use client"

import { Button } from "@/registry/new-york/ui/button";
import { useSearchParams, useRouter } from "next/navigation";


export default function PageNavigation() {
    const params = useSearchParams()
    const router = useRouter()
    const nextPage = () => {
        // console.log(params.get("page"))
        if (params.get("page") != undefined){
            router.push(`/change-requests?page=${Number(params.get("page"))+1}`)
        } else {
            router.push("/change-requests?page=1")
        }
    }
    const prevPage = () => {
        if (params.get("page") != undefined){
            router.push(`/change-requests?page=${Number(params.get("page"))-1}`)
        } else {
            router.push("/change-requests?page=1")
        }

    }
    return (
      <div className="flex items-center justify-end space-x-2 py-4">
        <Button variant="outline" size="sm" onClick={() => prevPage()} >
          Previous
        </Button>
        <Button variant="outline" size="sm" onClick={() => nextPage()} disabled={false}>
          Next
        </Button>
      </div>
    );
  };
  
"use client";
import {Table, TableBody, TableCell, TableHead, TableHeader, TableRow,} from "@/registry/new-york/ui/table";
import {useEffect, useState} from "react";

const concatNotNullValues = (value) => {
    console.log(value)
    if (typeof value === 'boolean') {
        return value.toString();
    }
    if (value && typeof value === 'string') {

        if (value.startsWith('{')) {
            try {
                const parsed = JSON.parse(value);
                if (parsed) {
                    return Object.values(parsed).filter(value => value !== null).join('');
                }
            } catch (e) {
                // ignore
            }
        }
        return value;
    }
    return value;
};
// @ts-ignore
export default function Diff({data}) {

    const [allProperties, setAllProperties] = useState([]);

    useEffect(() => {
        const combinedKeys = Object.keys({...data['originalLogisticsObject'], ...data['updatedLogisticsObject']}).filter(key => key !== '@id' && key !== '@type');

        //sort alphabetically
        combinedKeys.sort((a, b) => a.localeCompare(b));
        const toArray = combinedKeys.sort((a, b) => a.localeCompare(b));

        // @ts-ignore
        setAllProperties(toArray);

    }, []);
    // console.log("ok");
    // console.log(data);
    return (
        <>
            <Table>
                {/* <TableCaption>A list of your recent invoices.</TableCaption> */}
                <TableHeader>
                    <TableRow>
                        <TableHead className="w-[100px]">Property</TableHead>
                        <TableHead>Old</TableHead>
                        <TableHead>New</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {allProperties.map((k) => {

                        const originalValue = data['originalLogisticsObject'][k];
                        const updatedValue = data['updatedLogisticsObject'][k];

                        if (originalValue === null && updatedValue === null) {
                            return null;
                        }


                        const formatValue = (value) => {
                            if (value && typeof value === 'object') {
                                return value['@id'] ? value['@id'] : JSON.stringify(value);
                            }
                            return value;
                        };

                        const originalFormatted = formatValue(originalValue);
                        const updatedFormatted = formatValue(updatedValue);
                        const isAdded = originalValue === null && updatedValue !== null;
                        const isDeleted = originalValue !== null && updatedValue === null;
                        const isDifferent = !isAdded && !isDeleted && originalFormatted !== updatedFormatted;

                        console.log(originalFormatted);
                        console.log(updatedFormatted);

                        let backgroundColor;
                        if (isAdded) {
                            backgroundColor = '#ccffcc'; // green for added
                        } else if (isDeleted) {
                            backgroundColor = '#ffcccc'; // red for deleted
                        } else if (isDifferent) {
                            backgroundColor = '#ffff99'; // yellow for different
                        }


                        return (
                            <TableRow key={k} style={{backgroundColor: backgroundColor}}>
                                <TableCell>{k.split("#").pop()}</TableCell>
                                <TableCell>{concatNotNullValues(originalFormatted)}</TableCell>
                                <TableCell>{concatNotNullValues(updatedFormatted)}</TableCell>
                            </TableRow>
                        );
                    })}
                </TableBody>
            </Table>
        </>
    );
}

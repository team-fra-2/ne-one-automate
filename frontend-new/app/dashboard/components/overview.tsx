"use client"

import {Bar, BarChart, ResponsiveContainer, XAxis, YAxis} from "recharts"

const data = [
    {
        name: "Mon",
        total: 3200,
    },
    {
        name: "Tue",
        total: 4300,
    },
    {
        name: "Wed",
        total: 5903,
    },
    {
        name: "Thue",
        total: 3230,
    },
    {
        name: "Fri",
        total: 4210,
    },
    {
        name: "Sat",
        total: 1234
    },
    {
        name: "Sun",
        total: 2020,
    },
]

export function Overview() {
    return (
        <ResponsiveContainer width="100%" height={350}>
            <BarChart data={data}>
                <XAxis
                    dataKey="name"
                    stroke="#888888"
                    fontSize={12}
                    tickLine={false}
                    axisLine={false}
                />
                <YAxis
                    stroke="#888888"
                    fontSize={12}
                    tickLine={false}
                    axisLine={false}
                    tickFormatter={(value) => `${value}`}
                />
                <Bar dataKey="total" fill="#5C0632" radius={[4, 4, 0, 0]}/>
            </BarChart>
        </ResponsiveContainer>
    )
}

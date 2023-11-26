"use client";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const data = [
  {
    name: "Accepted",
    AutoAccepted: 6000,
    Accepted: 2400,
  },
  {
    name: "Rejected",
    AutoRejected: 3000,
    Rejected: 1398,
  },
  {
    name: "Pending",
    Pending_without_rule: 200,
    Pending_manual_check_needed: 800,
  },
];

export function Overview2() {
  return (
    <ResponsiveContainer width="100%" height={350}>
      <BarChart data={data} barSize={120}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis
          dataKey="name"
          stroke="#888888"
          fontSize={12}
          tickLine={false}
          axisLine={false}
        />
        <YAxis />
        <Tooltip />
        <Legend />
        {localStorage.theme == "light" && (
          <>
            <Bar dataKey="AutoAccepted" stackId="a" fill="#60a5fa" />
            <Bar dataKey="Accepted" stackId="a" fill="#22c55e" />
            <Bar dataKey="AutoRejected" stackId="a" fill="#9333ea" />
            <Bar dataKey="Rejected" stackId="a" fill="#ef4444" />
            <Bar
              dataKey="Pending_manual_check_needed"
              stackId="a"
              fill="#fbbf24"
            />
            <Bar dataKey="Pending_without_rule" stackId="a" fill="#f97316" />
          </>
        )}

        {localStorage.theme == "dark" && (
          <>
            <Bar dataKey="AutoAccepted" stackId="a" fill="#500724" />
            <Bar dataKey="Accepted" stackId="a" fill="#6b7280" />
            <Bar dataKey="Auto_Rejected" stackId="a" fill="#500724" />
            <Bar dataKey="Rejected" stackId="a" fill="#6b7280" />
            <Bar
              dataKey="Pending_manual_check_needed"
              stackId="a"
              fill="#500724"
            />
            <Bar dataKey="Pending_without_rule" stackId="a" fill="#6b7280" />{" "}
          </>
        )}
      </BarChart>
    </ResponsiveContainer>
  );
}

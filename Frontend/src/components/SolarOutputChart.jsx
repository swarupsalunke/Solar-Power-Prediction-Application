import { useEffect, useState } from "react";
import {
    ResponsiveContainer,
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
} from "recharts";

function formatTime(value) {
    return new Date(value).toLocaleString("en-IN", {
        day: "2-digit",
        month: "short",
        hour: "2-digit",
        minute: "2-digit",
    });
}

function useIsMobile(breakpoint = 560) {
    const [isMobile, setIsMobile] = useState(
        typeof window !== "undefined" && window.innerWidth <= breakpoint
    );

    useEffect(() => {
        const onResize = () => setIsMobile(window.innerWidth <= breakpoint);
        window.addEventListener("resize", onResize);
        return () => window.removeEventListener("resize", onResize);
    }, [breakpoint]);

    return isMobile;
}

function SolarOutputChart({ history, predictions }) {
    const isMobile = useIsMobile();

    const chartData = [
        ...history.map((item) => ({
            timestamp: item.timestamp,
            historicalOutput: Number(item.solar_output),
            predictedOutput: null,
        })),
        ...predictions.map((item) => ({
            timestamp: item.timestamp,
            historicalOutput: null,
            predictedOutput: Number(item.predicted_solar_output),
        })),
    ].sort(
        (a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
    );

    return (
        <section className="panel">
            <div className="section-heading">
                <h2>Historical &amp; Forecast Output</h2>
                <p>Historical dataset and future weather-based predictions</p>
            </div>

            <div className="chart-container">
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart
                        data={chartData}
                        margin={{
                            top: 10,
                            right: isMobile ? 8 : 20,
                            left: isMobile ? -10 : 10,
                            bottom: isMobile ? 60 : 55,
                        }}
                    >
                        <CartesianGrid strokeDasharray="3 3" stroke="#d3e4f0" />

                        <XAxis
                            dataKey="timestamp"
                            tickFormatter={formatTime}
                            angle={-35}
                            textAnchor="end"
                            interval="preserveStartEnd"
                            minTickGap={isMobile ? 40 : 20}
                            tick={{ fontSize: isMobile ? 10 : 11, fill: "#4a6584" }}
                            stroke="#78a4cb"
                        />

                        <YAxis
                            tick={{ fontSize: isMobile ? 10 : 12, fill: "#4a6584" }}
                            stroke="#78a4cb"
                            width={isMobile ? 40 : 60}
                            label={
                                isMobile
                                    ? undefined
                                    : {
                                        value: "Solar Output",
                                        angle: -90,
                                        position: "insideLeft",
                                        fill: "#3674b5",
                                    }
                            }
                        />

                        <Tooltip
                            labelFormatter={formatTime}
                            formatter={(value, name) => [Number(value).toFixed(2), name]}
                            contentStyle={{
                                borderRadius: 12,
                                border: "1px solid #b1e5e6",
                                boxShadow: "0 8px 24px rgba(54,116,181,0.18)",
                            }}
                        />

                        <Legend verticalAlign="top" height={isMobile ? 32 : 36} />

                        <Line
                            type="monotone"
                            dataKey="historicalOutput"
                            name="Historical Output"
                            stroke="#78a4cb"
                            strokeWidth={2}
                            dot={false}
                            connectNulls={false}
                        />

                        <Line
                            type="monotone"
                            dataKey="predictedOutput"
                            name="Predicted Output"
                            stroke="#3674b5"
                            strokeWidth={2.75}
                            dot={false}
                            connectNulls={false}
                        />
                    </LineChart>
                </ResponsiveContainer>
            </div>
        </section>
    );
}

export default SolarOutputChart;
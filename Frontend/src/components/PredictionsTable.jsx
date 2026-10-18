function formatTime(value) {
    return new Date(value).toLocaleString("en-IN", {
        day: "2-digit",
        month: "short",
        hour: "2-digit",
        minute: "2-digit",
    });
}

function PredictionsTable({ predictions }) {
    return (
        <section className="panel">
            <div className="section-heading">
                <h2>Future Predictions</h2>
                <p>Hourly solar output forecast</p>
            </div>

            <div className="table-wrapper">
                <table>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Timestamp</th>
                            <th>Predicted Solar Output</th>
                        </tr>
                    </thead>

                    <tbody>
                        {predictions.map((item, index) => (
                            <tr key={`${item.timestamp}-${index}`}>
                                <td data-label="#">{index + 1}</td>
                                <td data-label="Timestamp">{formatTime(item.timestamp)}</td>
                                <td data-label="Predicted Output" className="output-value">
                                    {Number(item.predicted_solar_output).toFixed(2)}
                                </td>
                            </tr>
                        ))}

                        {predictions.length === 0 && (
                            <tr className="empty-row">
                                <td colSpan="3">
                                    No predictions yet. Search for a location to see the forecast.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </section>
    );
}

export default PredictionsTable;
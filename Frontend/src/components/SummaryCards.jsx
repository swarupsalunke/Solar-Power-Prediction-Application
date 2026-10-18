function SummaryCards({ history, predictions }) {
    const values = predictions.map((item) =>
        Number(item.predicted_solar_output || 0)
    );

    const averageOutput = values.length
        ? values.reduce((sum, v) => sum + v, 0) / values.length
        : 0;

    const peakOutput = values.length ? Math.max(...values) : 0;

    const cards = [
        {
            title: "Historical Records",
            value: history.length,
            description: "Latest 14 days from dataset",
        },
        {
            title: "Forecast Records",
            value: predictions.length,
            description: "Hourly weather-based predictions",
        },
        {
            title: "Peak Predicted Output",
            value: peakOutput.toFixed(2),
            description: `Average output: ${averageOutput.toFixed(2)}`,
        },
    ];

    return (
        <section className="summary-grid" aria-label="Summary">
            {cards.map((card) => (
                <article className="summary-card" key={card.title}>
                    <p>{card.title}</p>
                    <h2>{card.value}</h2>
                    <span>{card.description}</span>
                </article>
            ))}
        </section>
    );
}

export default SummaryCards;
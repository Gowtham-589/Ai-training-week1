"""Generate a standalone SVG bar chart of sample monthly sales."""

from pathlib import Path

SALES = {"January": 120, "February": 185, "March": 150, "April": 220}


def main():
    bars = []
    for index, (month, sales) in enumerate(SALES.items()):
        y = 65 + index * 43
        width = round(sales / max(SALES.values()) * 300)
        bars.extend(
            [
                f'<text x="15" y="{y + 17}">{month}</text>',
                f'<rect x="105" y="{y}" width="{width}" height="24" fill="#2563eb"/>',
                f'<text x="{115 + width}" y="{y + 17}">{sales}</text>',
            ]
        )

    chart = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 255" role="img" aria-labelledby="title">',
        '<title id="title">Sample monthly sales in units</title>',
        '<rect width="480" height="255" fill="white"/>',
        '<g font-family="sans-serif" font-size="15" fill="#172554">',
        '<text x="15" y="33" font-size="23">Sample monthly sales (units)</text>',
        *bars,
        '</g></svg>',
    ]
    Path("monthly-sales.svg").write_text("\n".join(chart) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

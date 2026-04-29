from __future__ import annotations

import textwrap
from pathlib import Path
from typing import Dict, List

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


ACCENT = "#0B6E6E"
DARK = "#1F2937"
LIGHT = "#F8FAFC"
MUTED = "#6B7280"


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def create_insight_card(card: Dict, output_path: Path) -> Path:
    ensure_dir(output_path.parent)
    fig = plt.figure(figsize=(12, 6.75), dpi=160)
    ax = plt.axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    bg = FancyBboxPatch((0.02, 0.03), 0.96, 0.94, boxstyle="round,pad=0.012,rounding_size=0.025", linewidth=0, facecolor=LIGHT)
    stripe = FancyBboxPatch((0.02, 0.03), 0.02, 0.94, boxstyle="round,pad=0.0,rounding_size=0.025", linewidth=0, facecolor=ACCENT)
    right = FancyBboxPatch((0.67, 0.14), 0.27, 0.72, boxstyle="round,pad=0.02,rounding_size=0.03", linewidth=0, facecolor="#E7F3F3")
    ax.add_patch(bg)
    ax.add_patch(stripe)
    ax.add_patch(right)

    title = card.get("title", "Insight")
    subtitle = card.get("subtitle", "")
    bullets: List[str] = card.get("bullets", [])[:4]
    highlight_number = card.get("highlight_number", "3")
    highlight_label = card.get("highlight_label", "关键结论")

    ax.text(0.08, 0.86, title, fontsize=24, fontweight="bold", color=DARK, va="top")
    ax.text(0.08, 0.79, subtitle, fontsize=12, color=MUTED, va="top")

    y = 0.67
    for bullet in bullets:
        wrapped = textwrap.fill(bullet, width=32)
        ax.text(0.09, y, f"• {wrapped}", fontsize=14, color=DARK, va="top", linespacing=1.5)
        y -= 0.14

    ax.text(0.805, 0.60, str(highlight_number), fontsize=46, fontweight="bold", color=ACCENT, ha="center")
    ax.text(0.805, 0.46, highlight_label, fontsize=16, color=DARK, ha="center", wrap=True)
    ax.text(0.805, 0.28, "Consulting-style\ninsight card", fontsize=12, color=MUTED, ha="center")

    plt.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
    return output_path


def create_chart(chart: Dict, output_path: Path) -> Path:
    ensure_dir(output_path.parent)
    chart_type = chart.get("type", "bar")
    title = chart.get("title", "Chart")
    categories = chart.get("categories", [])
    series = chart.get("series", []) or [{"name": "Value", "values": chart.get("values", [])}]

    fig = plt.figure(figsize=(12, 7), dpi=160)
    ax = plt.axes([0.1, 0.16, 0.82, 0.72])

    if chart_type == "line":
        for item in series:
            ax.plot(categories, item.get("values", []), marker="o", linewidth=2.4, label=item.get("name", "Series"))
    elif chart_type == "pie":
        pie_values = series[0].get("values", []) if series else []
        ax.pie(pie_values, labels=categories, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
    else:
        total_series = max(1, len(series))
        x = list(range(len(categories)))
        width = 0.75 / total_series
        offset = -((total_series - 1) * width) / 2
        for idx, item in enumerate(series):
            positions = [i + offset + idx * width for i in x]
            ax.bar(positions, item.get("values", []), width=width, label=item.get("name", "Series"))
        ax.set_xticks(x)
        ax.set_xticklabels(categories, rotation=20, ha="right")

    ax.set_title(title, fontsize=18, fontweight="bold", pad=18)
    if chart.get("x_label"):
        ax.set_xlabel(chart["x_label"])
    if chart.get("y_label"):
        ax.set_ylabel(chart["y_label"])
    if len(series) > 1 and chart_type != "pie":
        ax.legend(frameon=False)
    ax.grid(True, axis="y", linestyle="--", alpha=0.25)
    caption = chart.get("caption") or chart.get("source_note") or ""
    fig.text(0.1, 0.04, caption, fontsize=10, color=MUTED)
    plt.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
    return output_path

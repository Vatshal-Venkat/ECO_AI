# eco_insights_utils.py — Helper functions for Royal Premium Insights Dashboard

import math
import requests
import altair as alt
import pandas as pd
import streamlit.components.v1 as components
from typing import Dict

# API Base (imported by eco_ui)
API_BASE = "http://127.0.0.1:8000"



# ------- THEME COLORS -------
THEME = {
    "bg": "#0a0c12",
    "card_bg": "rgba(255,255,255,0.04)",
    "gold": "#D4AF37",
    "gold_deep": "#b8922c",
    "sapphire": "#1F6FEB",
    "silver": "#8C93A1",
    "muted": "#8C93A1",
    "text": "#EAEAEA"
}


# ------- FETCH IMPACT COUNTS -------
def get_impact_counts_from_api(eco_uid: str = None) -> Dict[str, int]:
    """Fetch counts from API, fallback to sample."""
    sample = {"High": 12, "Medium": 21, "Low": 8}
    if not eco_uid:
        return sample
    try:
        r = requests.get(f"{API_BASE}/tc/eco/{eco_uid}")
        data = r.json()
        items = data.get("impacted_items") or data.get("items") or []
        counts = {"High": 0, "Medium": 0, "Low": 0}
        for it in items:
            if isinstance(it, dict):
                lvl = (it.get("impact") or it.get("risk") or "Low").title()
            else:
                lvl = "Low"
            if "High" in lvl:
                counts["High"] += 1
            elif "Medium" in lvl:
                counts["Medium"] += 1
            else:
                counts["Low"] += 1
        return counts if sum(counts.values()) > 0 else sample
    except:
        return sample


# ------- COMPUTE RISK SCORE -------
def compute_weighted_risk(counts: Dict[str, int], weights=(3, 2, 1)) -> float:
    high, med, low = counts["High"], counts["Medium"], counts["Low"]
    w_high, w_med, w_low = weights
    total_items = max(1, high + med + low)
    score = high * w_high + med * w_med + low * w_low
    max_score = total_items * w_high
    return (score / max_score) * 100


# ------- MULTI-RING SVG GAUGE -------
def render_multi_ring_svg(counts: Dict[str, int], size=360, stroke_widths=(20, 18, 16)):
    high, med, low = counts["High"], counts["Medium"], counts["Low"]
    total = max(1, high + med + low)

    p_high = high / total * 100
    p_med = med / total * 100
    p_low = low / total * 100

    cx = cy = size // 2
    gap = 6
    inner_r = 38
    r_outer = inner_r + (stroke_widths[0] + stroke_widths[1] + stroke_widths[2]) + gap * 2
    r_mid = inner_r + (stroke_widths[1] + stroke_widths[2]) + gap
    r_inner = inner_r + stroke_widths[2]

    def arc_path(r, pct, color, stroke):
        if pct >= 100:
            return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="{stroke}"/>'
        ang = pct / 100 * 360
        sx, sy = cx, cy - r
        ex = cx + r * math.cos(math.radians(-90 + ang))
        ey = cy + r * math.sin(math.radians(-90 + ang))
        large = 1 if ang > 180 else 0
        return f'M {sx} {sy} A {r} {r} 0 {large} 1 {ex} {ey}'

    svg = f"""
    <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">
      <defs>
        <filter id="glow"><feGaussianBlur stdDeviation="6" result="b"/>
          <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
      </defs>

      <circle cx="{cx}" cy="{cy}" r="{r_outer}" fill="none" stroke="rgba(255,255,255,0.04)" stroke-width="{stroke_widths[0]}"/>
      <circle cx="{cx}" cy="{cy}" r="{r_mid}"   fill="none" stroke="rgba(255,255,255,0.03)" stroke-width="{stroke_widths[1]}"/>
      <circle cx="{cx}" cy="{cy}" r="{r_inner}" fill="none" stroke="rgba(255,255,255,0.02)" stroke-width="{stroke_widths[2]}"/>

      <path d="{arc_path(r_outer, p_high, THEME["gold"], stroke_widths[0])}" fill="none" stroke-linecap="round" filter="url(#glow)"/>
      <path d="{arc_path(r_mid, p_med, THEME["gold_deep"], stroke_widths[1])}" fill="none" stroke-linecap="round"/>
      <path d="{arc_path(r_inner, p_low, THEME["muted"], stroke_widths[2])}" fill="none" stroke-linecap="round"/>

      <text x="{cx}" y="{cy}" text-anchor="middle" fill="{THEME["gold"]}"
            font-size="22" font-weight="800">{high + med + low} Items</text>
    </svg>
    """
    return svg


# ------- PROGRESS GAUGE -------
def render_progress_gauge(score, size=220):
    score = max(0, min(100, score))
    cx = cy = size // 2
    r = (size // 2) - 12
    thickness = 18

    start_angle = -225
    sweep = 270 * (score / 100)
    end_angle = start_angle + sweep

    sx = cx + r * math.cos(math.radians(start_angle))
    sy = cy + r * math.sin(math.radians(start_angle))
    ex = cx + r * math.cos(math.radians(end_angle))
    ey = cy + r * math.sin(math.radians(end_angle))
    large = 1 if sweep > 180 else 0

    svg = f"""
    <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">
      <defs>
        <linearGradient id="grad" x1="0" x2="1">
          <stop offset="0%" stop-color="{THEME['sapphire']}"/>
          <stop offset="60%" stop-color="{THEME['gold_deep']}"/>
          <stop offset="100%" stop-color="{THEME['gold']}"/>
        </linearGradient>
      </defs>

      <path d="M {sx} {sy} A {r} {r} 0 1 1 {cx-r} {cy}"
            stroke="rgba(255,255,255,0.05)" stroke-width="{thickness}" fill="none"/>

      <path d="M {sx} {sy} A {r} {r} 0 {large} 1 {ex} {ey}"
            stroke="url(#grad)" stroke-width="{thickness}" fill="none"
            stroke-linecap="round"/>

      <text x="{cx}" y="{cy}" text-anchor="middle" fill="{THEME['gold']}"
            font-size="22" font-weight="800">{score:.0f}%</text>
    </svg>
    """
    return svg


# ------- BAR CHART -------
def bar_chart_counts(df_counts: pd.DataFrame):
    return alt.Chart(df_counts).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6).encode(
        x=alt.X('impact:N', sort=["High", "Medium", "Low"]),
        y=alt.Y('count:Q'),
        color=alt.Color(
            'impact:N',
            scale=alt.Scale(
                domain=["High", "Medium", "Low"],
                range=[THEME["gold"], THEME["gold_deep"], THEME["muted"]]
            )
        ),
        tooltip=['impact', 'count']
    ).properties(width=420, height=260)


# ------- DONUT CHART -------
def donut_chart(df_counts: pd.DataFrame):
    return alt.Chart(df_counts).mark_arc(innerRadius=60).encode(
        theta=alt.Theta("count:Q"),
        color=alt.Color(
            "impact:N",
            scale=alt.Scale(
                domain=["High", "Medium", "Low"],
                range=[THEME["gold"], THEME["gold_deep"], THEME["muted"]]
            )
        ),
        tooltip=["impact", "count"]
    ).properties(width=360, height=360)

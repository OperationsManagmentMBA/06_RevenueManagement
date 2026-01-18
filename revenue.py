import marimo

__generated_with = "0.19.4"
app = marimo.App(
    width="medium",
    app_title="Revenue Management",
    css_file="d3.css",
)


@app.cell(hide_code=True)
def _():
    # Import required libraries
    import marimo as mo
    import altair as alt
    import polars as pl
    import numpy as np
    from scipy import stats
    import warnings

    warnings.filterwarnings("ignore", message=".*narwhals.*is_pandas_dataframe.*")
    return alt, mo, np, pl, stats


@app.cell(hide_code=True)
def _(mo):
    # Slide classes for consistent presentation layout
    from dataclasses import dataclass
    from typing import Optional as _Optional
    import html as _html

    # Slide constants
    SLIDE_WIDTH = 1280
    SLIDE_HEIGHT = 720
    GAP = 24
    PADDING_X = 24
    PADDING_Y = 16
    TITLE_FONT_SIZE = 28
    FOOTER_FONT_SIZE = 12

    @dataclass
    class Slide:
        title: str
        chair: str
        course: str
        presenter: str
        logo_url: _Optional[str]
        page_number: int
        layout_type: str = "side-by-side"
        subtitle: _Optional[str] = None
        content1: _Optional[mo.core.MIME] = None
        content2: _Optional[mo.core.MIME] = None

        def _header(self) -> mo.core.MIME:
            safe_title = _html.escape(self.title)
            return mo.Html(
                f"""
                <div class="slide-header">
                  <div class="slide-title" style="font-size: {TITLE_FONT_SIZE}px; font-weight: 700; line-height: 1.2; margin: 0;">{safe_title}</div>
                  <div class="slide-hr" style="height: 1px; background: #E5E7EB; margin: 8px 0;"></div>
                </div>
                """
            )

        def _footer(self) -> mo.core.MIME:
            safe_page = _html.escape(str(self.page_number))
            safe_chair = _html.escape(self.chair)
            left_html = f"Page {safe_page} &nbsp;&nbsp;|&nbsp;&nbsp; {safe_chair}"
            center_img = (
                f'<img class="slide-logo" src="{_html.escape(self.logo_url)}" alt="logo" style="display: block; max-height: 28px; max-width: 160px; margin: 0 auto; object-fit: contain;">'
                if self.logo_url
                else "&nbsp;"
            )
            return mo.Html(
                f"""
                <div class="slide-footer">
                  <div class="slide-hr" style="height: 1px; background: #E5E7EB; margin: 8px 0;"></div>
                  <div class="slide-footer-row" style="display: grid; grid-template-columns: 1fr auto 1fr; align-items: center;">
                    <div class="slide-footer-left" style="font-size: {FOOTER_FONT_SIZE}px; color: #6B7280; white-space: nowrap;">{left_html}</div>
                    <div class="slide-footer-center">{center_img}</div>
                    <div class="slide-footer-right">&nbsp;</div>
                  </div>
                </div>
                """
            )

        def _title_layout(self) -> mo.core.MIME:
            safe_title = _html.escape(self.title)
            sub = (
                f'<div class="title-slide-sub" style="font-size: 40px; margin: 0 0 16px 0; color: #374151;">{_html.escape(self.subtitle)}</div>'
                if self.subtitle
                else ""
            )
            body = mo.Html(
                f"""
                <div class="slide-body title-center" style="flex: 1 1 auto; min-height: 0; display: flex; align-items: center; justify-content: center; height: 100%;">
                  <div class="title-stack" style="text-align: center;">
                    <div class="title-slide-title" style="font-size: 50px; font-weight: 800; margin: 0 0 8px 0;">{safe_title}</div>
                    {sub}
                    <div class="title-slide-meta" style="font-size: 30px; color: #6B7280;">{_html.escape(self.course)}</div>
                    <div class="title-slide-meta" style="font-size: 22px; color: #6B7280;">{_html.escape(self.presenter)}</div>
                  </div>
                </div>
                """
            )
            return mo.Html(
                f"""
                <div class="slide" style="width: {SLIDE_WIDTH}px; height: {SLIDE_HEIGHT}px; min-width: {SLIDE_WIDTH}px; min-height: {SLIDE_HEIGHT}px; max-width: {SLIDE_WIDTH}px; max-height: {SLIDE_HEIGHT}px; box-sizing: border-box; background: #ffffff; padding: {PADDING_Y}px {PADDING_X}px; display: flex; flex-direction: column; border-radius: 6px; box-shadow: 0 0 0 1px #f3f4f6; overflow: hidden; page-break-after: always; break-after: page;">
                  {self._header()}
                  {body}
                  {self._footer()}
                </div>
                """
            )

        def _one_column_layout(self) -> mo.core.MIME:
            content = (
                mo.md(self.content1)
                if isinstance(self.content1, str)
                else (self.content1 or mo.md(""))
            )
            content_wrapped = mo.vstack([content], gap=0).style(
                {"gap": "0", "margin": "0", "padding": "0"}
            )
            body = mo.Html(
                f"""
                <div class="slide-body" style="flex: 1 1 auto; min-height: 0; display: flex; flex-direction: column;">
                    <div class="slide-col tight-md" style="min-height: 0; overflow: auto; padding-right: 2px;">
                        <style>
                            ul, ol {{ margin-top: -0.2em !important; }}
                            .slide-col.tight-md .paragraph {{ margin-block: 0 !important; margin: 0 0 4px 0 !important; font-size: 19px !important; }}
                            .slide-col.tight-md span.paragraph {{ margin-block: 0 !important; margin: 0 0 4px 0 !important; font-size: 19px !important; }}
                            li {{ font-size: 19px !important; }}
                            li * {{ font-size: 19px !important; }}
                            table {{ font-size: 14px !important; width: auto !important; max-width: 100% !important; }}
                            th, td {{ font-size: 14px !important; padding: 4px 8px !important; }}
                            thead {{ font-size: 14px !important; }}
                            pre {{ font-size: 12px !important; padding: 6px 10px !important; margin: 4px 0 !important; max-width: 100% !important; overflow-x: auto !important; }}
                            code {{ font-size: 12px !important; }}
                            pre code {{ font-size: 12px !important; }}
                        </style>
                        {content_wrapped}
                    </div>
                </div>
                """
            )
            return mo.Html(
                f"""
                <div class="slide" style="width: {SLIDE_WIDTH}px; height: {SLIDE_HEIGHT}px; min-width: {SLIDE_WIDTH}px; min-height: {SLIDE_HEIGHT}px; max-width: {SLIDE_WIDTH}px; max-height: {SLIDE_HEIGHT}px; box-sizing: border-box; background: #ffffff; padding: {PADDING_Y}px {PADDING_X}px; display: flex; flex-direction: column; border-radius: 6px; box-shadow: 0 0 0 1px #f3f4f6; overflow: hidden; page-break-after: always; break-after: page;">
                  {self._header()}
                  {body}
                  {self._footer()}
                </div>
                """
            )

        def _side_by_side_layout(self) -> mo.core.MIME:
            left_content = (
                mo.md(self.content1)
                if isinstance(self.content1, str)
                else (self.content1 or mo.md(""))
            )
            right_content = (
                mo.md(self.content2)
                if isinstance(self.content2, str)
                else (self.content2 or mo.md(""))
            )
            left = mo.vstack([left_content], gap=0).style(
                {"gap": "0", "margin": "0", "padding": "0"}
            )
            right = mo.vstack([right_content], gap=0).style(
                {"gap": "0", "margin": "0", "padding": "0"}
            )
            body = mo.Html(
                f"""
                <div class="slide-body" style="flex: 1 1 auto; min-height: 0; display: flex; flex-direction: column;">
                    <style>
                        ul, ol {{ margin-top: -0.2em !important; }}
                        .slide-col.tight-md .paragraph {{ margin-block: 0 !important; margin: 0 0 4px 0 !important; font-size: 19px !important; }}
                        .slide-col.tight-md span.paragraph {{ margin-block: 0 !important; margin: 0 0 4px 0 !important; font-size: 19px !important; }}
                        li {{ font-size: 19px !important; }}
                        li * {{ font-size: 19px !important; }}
                        table {{ font-size: 14px !important; width: auto !important; max-width: 100% !important; }}
                        th, td {{ font-size: 14px !important; padding: 4px 8px !important; }}
                        thead {{ font-size: 14px !important; }}
                        pre {{ font-size: 12px !important; padding: 6px 10px !important; margin: 4px 0 !important; max-width: 100% !important; overflow-x: auto !important; }}
                        code {{ font-size: 12px !important; }}
                        pre code {{ font-size: 12px !important; }}
                    </style>
                    <div class="slide-cols" style="display: grid; grid-template-columns: 1fr 1fr; gap: {GAP}px; height: 100%; min-height: 0;">
                        <div class="slide-col tight-md" style="min-height: 0; overflow: auto; padding-right: 2px;">
                            {left}
                        </div>
                        <div class="slide-col tight-md" style="min-height: 0; overflow: auto; padding-right: 2px;">
                            {right}
                        </div>
                    </div>
                </div>
                """
            )
            return mo.Html(
                f"""
                <div class="slide" style="width: {SLIDE_WIDTH}px; height: {SLIDE_HEIGHT}px; min-width: {SLIDE_WIDTH}px; min-height: {SLIDE_HEIGHT}px; max-width: {SLIDE_WIDTH}px; max-height: {SLIDE_HEIGHT}px; box-sizing: border-box; background: #ffffff; padding: {PADDING_Y}px {PADDING_X}px; display: flex; flex-direction: column; border-radius: 6px; box-shadow: 0 0 0 1px #f3f4f6; overflow: hidden; page-break-after: always; break-after: page;">
                  {self._header()}
                  {body}
                  {self._footer()}
                </div>
                """
            )

        def _section_layout(self) -> mo.core.MIME:
            safe_title = _html.escape(self.title)
            section_label = (
                f'<div style="font-size: 20px; font-weight: 600; color: #6B7280; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 12px;">{_html.escape(self.subtitle)}</div>'
                if self.subtitle
                else ""
            )
            agenda_content = ""
            if self.content1:
                agenda_html = (
                    mo.md(self.content1)
                    if isinstance(self.content1, str)
                    else self.content1
                )
                agenda_content = f'<div style="margin-top: 32px; font-size: 18px; color: #4B5563; max-width: 600px; text-align: center;">{agenda_html}</div>'

            body = mo.Html(
                f"""
                <div class="slide-body section-center" style="flex: 1 1 auto; min-height: 0; display: flex; align-items: center; justify-content: center; height: 100%;">
                  <div style="text-align: center;">
                    {section_label}
                    <div style="font-size: 42px; font-weight: 700; color: #111827; margin: 0;">{safe_title}</div>
                    {agenda_content}
                  </div>
                </div>
                """
            )
            return mo.Html(
                f"""
                <div class="slide" style="width: {SLIDE_WIDTH}px; height: {SLIDE_HEIGHT}px; min-width: {SLIDE_WIDTH}px; min-height: {SLIDE_HEIGHT}px; max-width: {SLIDE_WIDTH}px; max-height: {SLIDE_HEIGHT}px; box-sizing: border-box; background: #ffffff; padding: {PADDING_Y}px {PADDING_X}px; display: flex; flex-direction: column; border-radius: 6px; box-shadow: 0 0 0 1px #f3f4f6; overflow: hidden; page-break-after: always; break-after: page;">
                  {body}
                  {self._footer()}
                </div>
                """
            )

        def render(self) -> mo.core.MIME:
            if self.layout_type == "title":
                return self._title_layout()
            elif self.layout_type == "section":
                return self._section_layout()
            elif self.layout_type == "1-column":
                return self._one_column_layout()
            return self._side_by_side_layout()

    class SlideCreator:
        def __init__(
            self,
            chair: str,
            course: str,
            presenter: str,
            logo_url: _Optional[str] = None,
        ):
            self.chair = chair
            self.course = course
            self.presenter = presenter
            self.logo_url = logo_url
            self._page_counter = 0

        def styles(self) -> mo.core.MIME:
            return mo.Html(
                f"""
                <style>
                  :root {{
                    --slide-w: {SLIDE_WIDTH}px;
                    --slide-h: {SLIDE_HEIGHT}px;
                    --gap: {GAP}px;
                    --pad-x: {PADDING_X}px;
                    --pad-y: {PADDING_Y}px;
                    --title-size: {TITLE_FONT_SIZE}px;
                    --footer-size: {FOOTER_FONT_SIZE}px;
                    --border-color: #E5E7EB;
                    --text-muted: #6B7280;
                    --bg: #ffffff;
                  }}
                  div.slide, .slide {{
                    width: var(--slide-w) !important;
                    height: var(--slide-h) !important;
                    min-width: var(--slide-w) !important;
                    min-height: var(--slide-h) !important;
                    max-width: var(--slide-w) !important;
                    max-height: var(--slide-h) !important;
                    box-sizing: border-box !important;
                    background: var(--bg) !important;
                    padding: var(--pad-y) var(--pad-x) !important;
                    display: flex !important;
                    flex-direction: column !important;
                    border-radius: 6px;
                    box-shadow: 0 0 0 1px #f3f4f6;
                    overflow: hidden !important;
                  }}
                  div.slide-title, .slide-title {{
                    font-size: var(--title-size) !important;
                    font-weight: 700 !important;
                    line-height: 1.2 !important;
                    margin: 0 !important;
                  }}
                  div.slide-hr, .slide-hr {{
                    height: 1px !important;
                    background: var(--border-color) !important;
                    margin: 8px 0 !important;
                  }}
                  div.slide-body, .slide-body {{
                    flex: 1 1 auto !important;
                    min-height: 0 !important;
                    display: flex !important;
                    flex-direction: column !important;
                  }}
                  div.slide-cols, .slide-cols {{
                    display: grid !important;
                    grid-template-columns: 1fr 1fr !important;
                    gap: var(--gap) !important;
                    height: 100% !important;
                    min-height: 0 !important;
                  }}
                  div.slide-col, .slide-col {{
                    min-height: 0 !important;
                    overflow: auto !important;
                    padding-right: 2px !important;
                  }}
                  div.slide-footer div.slide-footer-row, .slide-footer .slide-footer-row {{
                    display: grid !important;
                    grid-template-columns: 1fr auto 1fr !important;
                    align-items: center !important;
                  }}
                  div.slide-footer-left, .slide-footer-left {{
                    font-size: var(--footer-size) !important;
                    color: var(--text-muted) !important;
                    white-space: nowrap !important;
                  }}
                  img.slide-logo, .slide-logo {{
                    display: block !important;
                    max-height: 28px !important;
                    max-width: 160px !important;
                    margin: 0 auto !important;
                    object-fit: contain !important;
                  }}
                  div.title-center, .title-center {{
                    display: flex !important;
                    align-items: center !important;
                    justify-content: center !important;
                    height: 100% !important;
                  }}
                  div.title-stack, .title-stack {{
                    text-align: center !important;
                  }}
                  div.title-slide-title, .title-slide-title {{
                    font-size: 40px !important;
                    font-weight: 800 !important;
                    margin: 0 0 8px 0 !important;
                  }}
                  div.title-slide-sub, .title-slide-sub {{
                    font-size: 20px !important;
                    margin: 0 0 16px 0 !important;
                    color: #374151 !important;
                  }}
                  div.title-slide-meta, .title-slide-meta {{
                    font-size: 16px !important;
                    color: var(--text-muted) !important;
                  }}
                  .tight-md p {{ margin: 0 0 4px 0 !important; }}
                  .tight-md .paragraph {{ margin-block: 0 !important; margin: 0 0 4px 0 !important; display: block !important; font-size: 19px !important; }}
                  .tight-md span.paragraph {{ margin-block: 0 !important; margin: 0 0 4px 0 !important; display: block !important; font-size: 19px !important; }}
                  ul, ol {{ margin-top: -0.2em !important; margin-bottom: 6px !important; margin-left: 1.25em !important; margin-right: 0 !important; }}
                  .tight-md li {{ margin: 2px 0 !important; font-size: 19px !important; }}
                  li {{ font-size: 19px !important; }}
                  li * {{ font-size: 19px !important; }}
                  .tight-md h1, .tight-md h2, .tight-md h3, .tight-md h4 {{ margin: 0 0 6px 0 !important; }}
                  .slide table, .slide-col table {{
                    font-size: 14px !important;
                    width: auto !important;
                    max-width: 100% !important;
                    border-collapse: collapse !important;
                  }}
                  .slide th, .slide td, .slide-col th, .slide-col td {{
                    font-size: 14px !important;
                    padding: 4px 8px !important;
                    white-space: nowrap !important;
                  }}
                  .slide thead, .slide-col thead {{
                    font-size: 14px !important;
                  }}
                  .slide pre, .slide-col pre {{
                    font-size: 13px !important;
                    padding: 8px 12px !important;
                    margin: 4px 0 !important;
                    max-width: 100% !important;
                    overflow-x: auto !important;
                    white-space: pre !important;
                    box-sizing: border-box !important;
                  }}
                  .slide code, .slide-col code {{
                    font-size: 13px !important;
                  }}
                  .slide pre code, .slide-col pre code {{
                    font-size: 13px !important;
                    white-space: pre !important;
                  }}
                  .katex-display, .katex {{
                    font-size: 22px !important;
                  }}
                  .katex-display {{
                    margin: 0.5em 0 !important;
                  }}
                </style>
                """
            )

        def create_slide(
            self,
            title: str,
            layout_type: str = "side-by-side",
            page_number: _Optional[int] = None,
        ) -> Slide:
            if page_number is None:
                self._page_counter += 1
                page_number = self._page_counter
            return Slide(
                title=title,
                chair=self.chair,
                course=self.course,
                presenter=self.presenter,
                logo_url=self.logo_url,
                page_number=page_number,
                layout_type=layout_type,
            )

        def create_title_slide(
            self,
            title: str,
            subtitle: _Optional[str] = None,
            page_number: _Optional[int] = None,
        ) -> Slide:
            slide = self.create_slide(title, layout_type="title", page_number=page_number)
            slide.subtitle = subtitle
            return slide
    return (SlideCreator,)


@app.cell(hide_code=True)
def _():
    # Course metadata
    lehrstuhl = "Chair of Logistics and Quantitative Methods"
    vorlesung = "Operations Management"
    presenter = "Nikolai Stein"
    return lehrstuhl, presenter, vorlesung


@app.cell(hide_code=True)
def _(SlideCreator, lehrstuhl, presenter, vorlesung):
    # Initialize slide creator
    sc = SlideCreator(lehrstuhl, vorlesung, presenter)
    return (sc,)


@app.cell(hide_code=True)
def _(sc):
    # Title slide
    title_slide = sc.create_title_slide(
        "Revenue Management",
        subtitle="Capacity Control",
        page_number=1,
    )
    sc.styles()
    title_slide.render()
    return


@app.cell(hide_code=True)
def _(sc):
    # Section 1 separator
    section_1 = sc.create_slide(
        "Booking Limits & Protection Levels",
        layout_type="section",
        page_number=2,
    )
    section_1.subtitle = "Section 1"
    section_1.content1 = "How many seats should we protect for late-arriving, high-fare customers?"
    section_1.render()
    return


@app.cell(hide_code=True)
def _(mo, sc):
    # Slide 1.1 — The Setting (neutral introduction)
    slide_1_1 = sc.create_slide(
        "The Setting: A Hotel Revenue Manager's View",
        layout_type="side-by-side",
        page_number=3,
    )

    slide_1_1.content1 = mo.md(
        """
    **Your hotel**

    - **100 rooms** available for a specific night
    - Two distinct customer segments:

    | Segment | Typical Rate | Booking Window | Demand |
    |---------|-------------|----------------|--------|
    | Leisure | €80/night | 2-4 weeks early | ~120/day (σ ≈ 15) |
    | Business | €200/night | 1-3 days before | ~50/day (σ ≈ 25) |

    Both demand levels are uncertain, but business demand has higher variability.
    """
    )

    slide_1_1.content2 = mo.vstack(
        [
            mo.md("**When each segment typically books**"),
            mo.image("public/images/booking_behavior.png"),
            mo.md(
                """
    *Leisure travelers lock in vacation plans early.*

    *Business travelers book once meetings are confirmed.*
    """
            ),
        ],
        gap=1,
    )

    slide_1_1.render()
    return


@app.cell(hide_code=True)
def _(alt, mo, np, pl, sc):
    # Slide 1.2 — FCFS Simulation (Interactive discovery)

    def simulate_fcfs(n_simulations=1000, seed=1):
        """Simulate FCFS policy outcomes."""
        np.random.seed(seed)
        C = 100  # capacity
        r_L, r_H = 80, 200

        results = []
        for _ in range(n_simulations):
            # Leisure demand (books first), typically exceeds capacity
            leisure_demand = max(0, int(np.random.normal(120, 15)))
            leisure_booked = min(leisure_demand, C)

            # Business arrives late, higher uncertainty
            business_demand = max(0, int(np.random.normal(50, 25)))
            rooms_left = C - leisure_booked
            business_booked = min(business_demand, rooms_left)
            business_rejected = business_demand - business_booked

            revenue = leisure_booked * r_L + business_booked * r_H
            results.append(
                {
                    "Revenue": revenue,
                    "Leisure Booked": leisure_booked,
                    "Business Booked": business_booked,
                    "Business Rejected": business_rejected,
                    "Rooms Used": leisure_booked + business_booked,
                }
            )
        return pl.DataFrame(results)

    # Run simulation
    _fcfs_results = simulate_fcfs(n_simulations=1000)

    # Compute summary stats
    _mean_rev = _fcfs_results["Revenue"].mean()
    _mean_leisure = _fcfs_results["Leisure Booked"].mean()
    _mean_business = _fcfs_results["Business Booked"].mean()
    _mean_rejected = _fcfs_results["Business Rejected"].mean()

    # Create histogram
    _hist = (
        alt.Chart(_fcfs_results.to_pandas())
        .mark_bar(color="#2563eb", opacity=0.7)
        .encode(
            x=alt.X("Revenue:Q", bin=alt.Bin(maxbins=30), title="Daily Revenue (€)"),
            y=alt.Y("count()", title="Frequency"),
        )
        .properties(width=480, height=280)
    )

    # Add mean line
    _mean_rule = (
        alt.Chart(pl.DataFrame({"x": [_mean_rev]}).to_pandas())
        .mark_rule(strokeDash=[5, 5], color="#dc2626", strokeWidth=2)
        .encode(x="x:Q")
    )

    _chart = _hist + _mean_rule

    slide_1_2_fcfs = sc.create_slide(
        "FCFS: The Natural Policy",
        layout_type="side-by-side",
        page_number=4,
    )

    slide_1_2_fcfs.content1 = mo.md(
        f"""
    **First-Come-First-Served (FCFS)**

    Accept bookings in order of arrival until sold out.

    ---

    **Simulation: 1000 days of FCFS**

    | Metric | Average |
    |--------|---------|
    | Revenue (avg.) | **€{_mean_rev:,.2f}** |
    | Leisure rooms sold (avg.) | {_mean_leisure:.2f} |
    | Business rooms sold (avg.) | {_mean_business:.2f} |
    | **Business travelers turned away (avg.)** | **{_mean_rejected:.2f}** |
    """
    )

    slide_1_2_fcfs.content2 = mo.vstack(
        [
            mo.md("**Revenue distribution under FCFS**"),
            _chart,
            mo.md(f"Mean revenue: €{_mean_rev:,.0f} (red dashed line)"),
        ]
    )

    slide_1_2_fcfs.render()
    return


@app.cell(hide_code=True)
def _(mo, sc):
    # Slide 1.3 — Transition: Is FCFS Optimal?
    slide_1_3_transition = sc.create_slide(
        "Is FCFS the Best We Can Do?",
        layout_type="side-by-side",
        page_number=5,
    )

    slide_1_3_transition.content1 = mo.md(
        """
    **What we observed under FCFS:**

    - Revenue averages around **€8,000** per night
    - We consistently serve ~100 leisure travelers at €80
    - We turn away ~50 business travelers who would pay €200

    **The math:**

    - Those 50 rejected business travelers: 50 × €200 = **€10,000**
    - We served 50 leisure travelers instead: 50 × €80 = **€4,000**
    - **Lost opportunity: €6,000 per night**
    """
    )

    slide_1_3_transition.content2 = mo.md(
        """
    **A thought experiment:**

    What if we reserved some rooms for late-booking business travelers?

    - Reject some early leisure bookings
    - Hold capacity for high-paying customers

    **The trade-off:**

    - If business shows up → we earn more
    - If business doesn't show up → rooms go empty

    *How many rooms should we protect?*
    """
    )

    slide_1_3_transition.render()
    return


@app.cell(hide_code=True)
def _(mo, sc):
    # Slide 1.4 — Key definitions (was 1.3)
    slide_1_4 = sc.create_slide(
        "Key definitions",
        layout_type="1-column",
        page_number=6,
    )

    slide_1_4.content1 = mo.md(
        """
    | Symbol | Definition | Our Hotel Example |
    |--------|-----------|-------------------|
    | $C$ | Total capacity | 100 rooms |
    | $r_L$ | Low fare (leisure) | €80 |
    | $r_H$ | High fare (business) | €200 |
    | $D_H$ | High-fare demand | Random variable |
    | $Q$ | **Protection level** | Rooms reserved for high-fare |
    | $B$ | **Booking limit** for low-fare | $B = C - Q$ |

    **Protection level** $Q$ = number of rooms we *protect* (reserve) for high-fare customers

    **Booking limit** $B$ = maximum rooms we sell to low-fare customers
    """
    )

    slide_1_4.render()
    return


@app.cell(hide_code=True)
def _(mo, np):
    # UI inputs for the booking limit interactive
    capacity_slider = mo.ui.slider(
        start=50, stop=200, step=10, value=100, label="Capacity (C)"
    )
    low_fare_slider = mo.ui.slider(
        start=50, stop=150, step=10, value=80, label="Low fare ($)"
    )
    high_fare_slider = mo.ui.slider(
        start=100, stop=400, step=25, value=200, label="High fare ($)"
    )
    demand_mean_slider = mo.ui.slider(
        start=20, stop=100, step=5, value=50, label="Expected high-fare demand"
    )
    demand_std_slider = mo.ui.slider(
        start=5, stop=40, step=5, value=15, label="Demand std. dev."
    )
    protection_slider = mo.ui.slider(
        start=0, stop=100, step=1, value=40, label="Protection level (Q)"
    )

    # Assume unlimited leisure demand for simplicity
    LEISURE_DEMAND = 200

    def compute_metrics(C, r_L, r_H, mean_H, std_H, Q):
        """Compute expected revenue and metrics for given protection level."""
        # Booking limit
        B = C - Q

        # Generate demand distribution for high-fare (truncated at 0)
        demands = np.arange(0, int(mean_H + 4 * std_H) + 1)
        probs = np.exp(-0.5 * ((demands - mean_H) / std_H) ** 2)
        probs = probs / probs.sum()

        # Low-fare rooms sold (limited by booking limit B)
        low_fare_sold = min(LEISURE_DEMAND, B)

        # Expected high-fare sold and empty rooms
        high_fare_sold_expected = 0
        empty_expected = 0
        for d, p in zip(demands, probs):
            # High-fare demand can fill at most Q rooms (protected capacity)
            high_sold = min(d, Q)
            high_fare_sold_expected += p * high_sold
            # Empty rooms = Q - min(D_H, Q) = max(0, Q - D_H)
            empty_expected += p * max(0, Q - d)

        # Expected revenue
        revenue_expected = low_fare_sold * r_L + high_fare_sold_expected * r_H

        # Rejected high-fare demand
        rejected_expected = 0
        for d, p in zip(demands, probs):
            rejected_expected += p * max(0, d - Q)

        return {
            "booking_limit": B,
            "low_fare_sold": low_fare_sold,
            "high_fare_sold": high_fare_sold_expected,
            "empty_rooms": empty_expected,
            "rejected_high": rejected_expected,
            "revenue": revenue_expected,
        }
    return


@app.cell(hide_code=True)
def _(mo):
    # State to track explored Q values for slide 1.5
    get_explored_q, set_explored_q = mo.state({})  # dict: Q -> mean_revenue
    explore_q_slider = mo.ui.slider(start=0, stop=100, step=1, value=0, label="Protection level (Q)")
    run_exploration_btn = mo.ui.run_button(label="Test this Q")
    reset_exploration_btn = mo.ui.run_button(label="Reset")
    return (
        explore_q_slider,
        get_explored_q,
        reset_exploration_btn,
        run_exploration_btn,
        set_explored_q,
    )


@app.cell(hide_code=True)
def _(
    alt,
    explore_q_slider,
    get_explored_q,
    mo,
    np,
    pl,
    reset_exploration_btn,
    run_exploration_btn,
    sc,
    set_explored_q,
):
    # Slide 1.5 — Explore protection levels interactively
    slide_1_5 = sc.create_slide(
        "Explore: How does Q affect revenue?",
        layout_type="side-by-side",
        page_number=7,
    )

    # Simulation parameters (fixed for exploration)
    _C = 100
    _r_L, _r_H = 80, 200
    _mean_L, _std_L = 120, 15
    _mean_H, _std_H = 50, 25

    def _simulate_with_protection(Q, n_simulations=1000):
        """Simulate revenue with a given protection level."""
        np.random.seed(1)  # Reproducible per Q
        B = _C - Q  # Booking limit for low-fare
        revenues = []
        for _ in range(n_simulations):
            # Leisure demand (books first, limited by B)
            leisure_demand = max(0, int(np.random.normal(_mean_L, _std_L)))
            leisure_booked = min(leisure_demand, B)

            # Business demand (gets protected rooms + any leftover)
            business_demand = max(0, int(np.random.normal(_mean_H, _std_H)))
            rooms_for_business = _C - leisure_booked
            business_booked = min(business_demand, rooms_for_business)

            revenue = leisure_booked * _r_L + business_booked * _r_H
            revenues.append(revenue)
        return np.mean(revenues)

    # Handle reset button
    _explored = get_explored_q()
    if reset_exploration_btn.value:
        set_explored_q({})
        _explored = {}

    # Run simulation when button is clicked
    if run_exploration_btn.value:
        _Q = explore_q_slider.value
        _rev = _simulate_with_protection(_Q)
        if _Q not in _explored:
            set_explored_q({**_explored, _Q: _rev})
            _explored = {**_explored, _Q: _rev}

    # Build chart from explored data
    if _explored:
        _df = pl.DataFrame([
            {"Q": q, "Revenue": rev} for q, rev in sorted(_explored.items())
        ])
        _points = (
            alt.Chart(_df.to_pandas())
            .mark_circle(size=120, color="#2563eb")
            .encode(
                x=alt.X("Q:Q", title="Protection Level (Q)", scale=alt.Scale(domain=[0, 100])),
                y=alt.Y("Revenue:Q", title="Expected Revenue (€)", scale=alt.Scale(domain=[8000, 14000])),
                tooltip=["Q:Q", "Revenue:Q"],
            )
        )
        _line = (
            alt.Chart(_df.to_pandas())
            .mark_line(color="#2563eb", strokeWidth=2, opacity=0.5)
            .encode(x="Q:Q", y="Revenue:Q")
        )
        _chart = (_line + _points).properties(width=480, height=300)

        # Find best explored Q so far
        _best_q = max(_explored, key=_explored.get)
        _best_rev = _explored[_best_q]
        _status = mo.md(f"**Best so far:** Q = {_best_q} → €{_best_rev:,.0f}")
    else:
        _chart = mo.md("*Move the slider and click 'Test this Q' to explore*")
        _status = mo.md("*No data yet*")

    slide_1_5.content1 = mo.vstack(
        [
            mo.md("""
    **Try different protection levels**

    How many rooms should we reserve for business travelers?

    - Q = 0: No protection (FCFS)
    - Q = 100: Protect everything (no leisure)
    """),
            explore_q_slider,
            mo.hstack([run_exploration_btn, reset_exploration_btn, mo.md(f"Points explored: {len(_explored)}")]),
            _status,
        ],
        gap=0.5,
    )

    slide_1_5.content2 = _chart

    slide_1_5.render()
    return


@app.cell(hide_code=True)
def _(mo, sc):
    # Slide 1.6 — The critical fractile formula
    slide_1_6 = sc.create_slide(
        "Finding the optimal protection level",
        layout_type="side-by-side",
        page_number=8,
    )

    slide_1_6.content1 = mo.md(
        r"""
    **This is a newsvendor problem!**

    **Underage cost** $C_u$: Protect too few rooms
    - We sell a room at $r_L$ instead of $r_H$
    - $C_u = r_H - r_L$

    **Overage cost** $C_o$: Protect too many rooms
    - A protected room stays empty
    - $C_o = r_L$ (forgone low-fare revenue)

    **Critical fractile:**

    $$\frac{C_u}{C_u + C_o} = \frac{r_H - r_L}{r_H}$$
    """
    )

    slide_1_6.content2 = mo.md(
        r"""
    **Optimal protection level** $Q^*$:

    $$P(D_H \leq Q^*) = \frac{r_H - r_L}{r_H}$$

    **Interpretation:**

    Protect rooms until the probability of high-fare demand exceeding $Q^*$ equals the critical ratio.

    **Our hotel example:**

    $$\frac{200 - 80}{200} = 0.60$$

    Find $Q^*$ where $P(D_H \leq Q^*) = 0.60$
    """
    )

    slide_1_6.render()
    return


@app.cell(hide_code=True)
def _(mo):
    # UI elements for slide 1.7 - exploring what drives Q*
    explore_low_fare = mo.ui.slider(start=50, stop=150, step=10, value=80, label="Low fare (€)")
    explore_high_fare = mo.ui.slider(start=100, stop=400, step=25, value=200, label="High fare (€)")
    explore_demand_mean = mo.ui.slider(start=20, stop=80, step=5, value=50, label="High-fare demand mean")
    explore_demand_std = mo.ui.slider(start=5, stop=40, step=5, value=25, label="High-fare demand std")
    return (
        explore_demand_mean,
        explore_demand_std,
        explore_high_fare,
        explore_low_fare,
    )


@app.cell(hide_code=True)
def _(
    alt,
    explore_demand_mean,
    explore_demand_std,
    explore_high_fare,
    explore_low_fare,
    mo,
    np,
    pl,
    sc,
    stats,
):
    # Slide 1.7 — Explore what drives Q*
    slide_1_7 = sc.create_slide(
        "Explore: What drives the optimal Q*?",
        layout_type="side-by-side",
        page_number=9,
    )

    _C = 100  # Fixed capacity
    _r_L = explore_low_fare.value
    _r_H = explore_high_fare.value
    _mean_H = explore_demand_mean.value
    _std_H = explore_demand_std.value

    # Compute critical fractile
    _crit_frac = (_r_H - _r_L) / _r_H

    # Compute optimal Q using inverse CDF
    _Q_star = int(np.ceil(stats.norm.ppf(_crit_frac, _mean_H, _std_H)))
    _Q_star = max(0, min(_Q_star, _C))
    _B_star = _C - _Q_star

    # Create demand distribution visualization
    _x = np.linspace(max(0, _mean_H - 4 * _std_H), _mean_H + 4 * _std_H, 200)
    _y = stats.norm.pdf(_x, _mean_H, _std_H)
    _dist_df = pl.DataFrame({"x": _x, "density": _y})

    # Distribution curve
    _dist_curve = (
        alt.Chart(_dist_df.to_pandas())
        .mark_area(opacity=0.3, color="#2563eb")
        .encode(x=alt.X("x:Q", title="High-fare demand"), y=alt.Y("density:Q", title="Probability density"))
    )

    # Shaded area up to Q*
    _shaded_df = pl.DataFrame({
        "x": [xi for xi in _x if xi <= _Q_star],
        "density": [yi for xi, yi in zip(_x, _y) if xi <= _Q_star],
    })
    _shaded_area = (
        alt.Chart(_shaded_df.to_pandas())
        .mark_area(opacity=0.5, color="#2563eb")
        .encode(x="x:Q", y="density:Q")
    )

    # Vertical line at Q*
    _q_line = (
        alt.Chart(pl.DataFrame({"Q": [_Q_star]}).to_pandas())
        .mark_rule(strokeDash=[5, 5], color="#dc2626", strokeWidth=2)
        .encode(x="Q:Q")
    )

    # Q* label
    _q_label = (
        alt.Chart(pl.DataFrame({"Q": [_Q_star], "y": [max(_y) * 0.8], "text": [f"Q* = {_Q_star}"]}).to_pandas())
        .mark_text(align="left", dx=5, fontSize=14, color="#dc2626")
        .encode(x="Q:Q", y="y:Q", text="text:N")
    )

    _chart = (_dist_curve + _shaded_area + _q_line + _q_label).properties(width=450, height=280)

    slide_1_7.content1 = mo.vstack(
        [
            mo.md("**Adjust parameters and observe how Q* changes:**"),
            mo.hstack([explore_low_fare, explore_high_fare]),
            mo.hstack([explore_demand_mean, explore_demand_std]),
            mo.md("---"),
            mo.md(f"""
    **Results:**

    | Parameter | Value |
    |-----------|-------|
    | Critical ratio | **{_crit_frac:.1%}** |
    | Optimal Q* | **{_Q_star}** rooms protected |
    | Booking limit B* | **{_B_star}** rooms for low-fare |
    """),
            mo.md("""
    **Try these experiments:**
    - Change high fare → What happens to Q*?
    - Change low fare → What happens to Q*?
    - Change demand variance → What happens to Q*?
    """),
        ],
        gap=0.3,
    )

    slide_1_7.content2 = mo.vstack([
        mo.md("**High-fare demand distribution with Q* marked**"),
        _chart,
        mo.md(f"Shaded area = P(D_H ≤ Q*) = {_crit_frac:.1%}"),
    ])

    slide_1_7.render()
    return


@app.cell(hide_code=True)
def _(mo, sc):
    # Slide 1.8 — Managerial takeaway
    slide_1_8 = sc.create_slide(
        "Booking limits: Key insight",
        layout_type="1-column",
        page_number=10,
    )

    slide_1_8.content1 = mo.md(
        r"""
    **The goal is to protect upside, not punish low-fare customers**

    **What we learned:**

    1. **FCFS is naive** — it ignores customer value and timing
    2. **Protection levels balance two risks:**
       - Selling too cheap (rejecting high-fare demand)
       - Protecting too much (empty capacity)
    3. **The optimal $Q^*$ depends on:**
       - The **critical ratio** $(r_H - r_L) / r_H$
       - The **demand distribution** for high-fare segment

    **Managerial insight:**

    When fares differ significantly and high-fare demand is uncertain,
    even imperfect protection levels substantially outperform FCFS.
    """
    )

    slide_1_8.render()
    return


@app.cell(hide_code=True)
def _(sc):
    # Section 2 separator
    section_2 = sc.create_slide(
        "Overbooking",
        layout_type="section",
        page_number=11,
    )
    section_2.subtitle = "Section 2"
    section_2.content1 = "Should we sell more than we have?"
    section_2.render()
    return


@app.cell(hide_code=True)
def _(mo, sc):
    # Slide 2.1 — The Setting (neutral introduction)
    slide_2_1 = sc.create_slide(
        "The Setting: A Hotel's Reservation System",
        layout_type="side-by-side",
        page_number=12,
    )

    slide_2_1.content1 = mo.md(
        """
    **Your hotel:**

    - **100 rooms** available each night
    - Guests make reservations in advance
    - Each reservation is confirmed

    **A simple observation:**

    Not all confirmed guests actually show up.

    - Plans change
    - Flexible cancellation policies
    - Last-minute changes
    - "Just in case" bookings
    """
    )

    slide_2_1.content2 = mo.md(
        """
    **Historical data shows:**

    | Metric | Value |
    |--------|-------|
    | Average no-show rate | ~10% |
    | Variability | Some nights 5%, others 15% |
    | Room rate | €150/night |

    *This is a common pattern across hotels, airlines, restaurants...*

    **Question:** What happens when we accept exactly 100 reservations?
    """
    )

    slide_2_1.render()
    return


@app.cell(hide_code=True)
def _(alt, mo, np, pl, sc):
    # Slide 2.2 — No-show simulation (Discovery)
    slide_2_2_sim = sc.create_slide(
        "What Happens When We Book 100 Rooms?",
        layout_type="side-by-side",
        page_number=13,
    )

    def _simulate_exact_booking(n_simulations=1000, seed=2):
        """Simulate outcomes when booking exactly 100 rooms."""
        np.random.seed(seed)
        C = 100  # capacity
        noshow_rate = 0.10
        r = 150  # room rate

        results = []
        for _ in range(n_simulations):
            # Each guest has 10% chance of not showing
            noshows = np.random.binomial(C, noshow_rate)
            arrivals = C - noshows
            empty_rooms = noshows
            lost_revenue = empty_rooms * r
            actual_revenue = arrivals * r
            results.append({
                "Arrivals": arrivals,
                "Empty Rooms": empty_rooms,
                "Lost Revenue": lost_revenue,
                "Actual Revenue": actual_revenue,
            })
        return pl.DataFrame(results)

    # Run simulation
    _sim_results = _simulate_exact_booking(n_simulations=10000)

    # Compute summary stats
    _mean_arrivals = _sim_results["Arrivals"].mean()
    _mean_empty = _sim_results["Empty Rooms"].mean()
    _mean_lost = _sim_results["Lost Revenue"].mean()
    _mean_revenue = _sim_results["Actual Revenue"].mean()

    # Create histogram of revenue (use bin step=150 to align with discrete values)
    _hist = (
        alt.Chart(_sim_results.to_pandas())
        .mark_bar(color="#2563eb", opacity=0.7)
        .encode(
            x=alt.X("Actual Revenue:Q", bin=alt.Bin(step=150), title="Daily Revenue (€)"),
            y=alt.Y("count()", title="Frequency (out of 1000 nights)"),
        )
        .properties(width=500, height=280)
    )

    # Add mean line
    _mean_rule = (
        alt.Chart(pl.DataFrame({"x": [_mean_revenue]}).to_pandas())
        .mark_rule(strokeDash=[5, 5], color="#dc2626", strokeWidth=2)
        .encode(x="x:Q")
    )

    _chart = _hist + _mean_rule

    slide_2_2_sim.content1 = mo.md(
        f"""
    **Simulation: 1000 nights with 100 bookings**

    Each night:
    - Accept exactly 100 reservations
    - Each guest has ~10% chance of no-show
    - Room rate: €150

    **Results:**

    | Metric | Average |
    |--------|---------|
    | Guests who arrive (avg.) | **{_mean_arrivals:.2f}** |
    | Empty rooms (avg.) | **{_mean_empty:.2f}** |
    | Lost revenue (avg.) | **€{_mean_lost:,.2f}** |
    | Actual revenue (avg.) | **€{_mean_revenue:,.2f}** |
    """
    )

    slide_2_2_sim.content2 = mo.vstack([
        mo.md("**Daily revenue distribution**"),
        _chart,
        mo.md(f"*Mean revenue: €{_mean_revenue:,.2f}*"),
    ])

    slide_2_2_sim.render()
    return


@app.cell(hide_code=True)
def _(mo, sc):
    # Slide 2.3 — Transition: Can we do better?
    slide_2_3_transition = sc.create_slide(
        "Can We Do Better?",
        layout_type="side-by-side",
        page_number=14,
    )

    slide_2_3_transition.content1 = mo.md(
        """
    **What we just discovered:**

    - Booking exactly 100 rooms leaves **~10 rooms empty** on average
    - That's **€1,500 in lost revenue** per night
    - Over a year: ~€550,000 wasted capacity

    **The pattern is predictable:**

    We *know* about 10% won't show up.
    Yet we accept exactly 100 reservations.

    *We're planning for a world where everyone shows up—
    but that almost never happens.*
    """
    )

    slide_2_3_transition.content2 = mo.md(
        """
    **A thought experiment:**

    What if we sold **110 reservations** for 100 rooms?

    - Expected arrivals: 110 × 0.90 = **99** ✓
    - We'd fill almost all rooms

    **But wait...**

    What if more than 100 show up?

    - We'd have to **turn away** confirmed guests
    - Compensation, rebooking, angry customers...

    *Is the risk worth it? How much should we overbook?*
    """
    )

    slide_2_3_transition.render()
    return


@app.cell(hide_code=True)
def _(mo, sc):
    # Slide 2.4 — Key definitions (moved from old 2.2)
    slide_2_4 = sc.create_slide(
        "Overbooking: Key definitions",
        layout_type="1-column",
        page_number=15,
    )

    slide_2_4.content1 = mo.md(
        """
    | Symbol | Definition | Example |
    |--------|-----------|---------|
    | $C$ | Physical capacity | 100 rooms |
    | $X$ | Number of no-shows | Random variable |
    | $Y$ | **Overbooking level** | Extra bookings beyond $C$ |
    | $C + Y$ | Total reservations accepted | $C$ + $Y$ |
    | $r$ | Revenue per customer | €150 |
    | $c_b$ | **Bumping cost** | Cost of denying a customer with reservation |
    """
    )

    slide_2_4.render()
    return


@app.cell(hide_code=True)
def _(mo, np):
    # UI inputs for overbooking interactive
    ob_capacity_slider = mo.ui.slider(
        start=50, stop=200, step=10, value=100, label="Capacity (C)"
    )
    ob_revenue_slider = mo.ui.slider(
        start=50, stop=300, step=25, value=150, label="Revenue per room ($)"
    )
    ob_bump_cost_slider = mo.ui.slider(
        start=100, stop=800, step=50, value=400, label="Bumping cost ($)"
    )
    ob_noshow_rate_slider = mo.ui.slider(
        start=0.02, stop=0.25, step=0.01, value=0.10, label="No-show rate"
    )
    ob_level_slider = mo.ui.slider(
        start=0, stop=30, step=1, value=10, label="Overbooking level (Y)"
    )

    def compute_overbooking_metrics(C, r, c_bump, noshow_rate, Y):
        """Compute expected revenue and metrics for given overbooking level."""
        # Total reservations
        total_reservations = C + Y

        # No-shows follow binomial distribution
        # Expected no-shows = total_reservations * noshow_rate
        # Use normal approximation for simplicity
        mean_noshows = total_reservations * noshow_rate
        std_noshows = np.sqrt(total_reservations * noshow_rate * (1 - noshow_rate))

        # Expected arrivals
        expected_arrivals = total_reservations - mean_noshows

        # Expected bumped customers = max(0, arrivals - C)
        # This requires integration over the distribution
        arrivals_range = np.arange(0, total_reservations + 1)
        # Probability of each arrival count (binomial, approximate with normal)
        probs = np.exp(-0.5 * ((arrivals_range - expected_arrivals) / max(std_noshows, 1)) ** 2)
        probs = probs / probs.sum()

        expected_bumped = 0
        expected_empty = 0
        prob_bumping = 0

        for arrivals, p in zip(arrivals_range, probs):
            if arrivals > C:
                expected_bumped += p * (arrivals - C)
                prob_bumping += p
            else:
                expected_empty += p * (C - arrivals)

        # Expected revenue
        expected_occupied = min(expected_arrivals, C)
        expected_revenue = expected_arrivals * r - expected_bumped * c_bump
        # More accurate: revenue from occupied rooms minus bump costs
        expected_net_revenue = 0
        for arrivals, p in zip(arrivals_range, probs):
            occupied = min(arrivals, C)
            bumped = max(0, arrivals - C)
            expected_net_revenue += p * (occupied * r - bumped * c_bump)

        return {
            "total_reservations": total_reservations,
            "expected_arrivals": expected_arrivals,
            "expected_occupied": expected_occupied,
            "expected_empty": expected_empty,
            "expected_bumped": expected_bumped,
            "prob_bumping": prob_bumping,
            "expected_net_revenue": expected_net_revenue,
        }
    return


@app.cell(hide_code=True)
def _(mo):
    # State to track explored Y values for slide 2.5
    get_explored_y, set_explored_y = mo.state({})  # dict: Y -> net_revenue
    explore_y_slider = mo.ui.slider(start=0, stop=30, step=1, value=0, label="Overbooking level (Y)")
    run_y_exploration_btn = mo.ui.run_button(label="Test this Y")
    reset_y_exploration_btn = mo.ui.run_button(label="Reset")
    return (
        explore_y_slider,
        get_explored_y,
        reset_y_exploration_btn,
        run_y_exploration_btn,
        set_explored_y,
    )


@app.cell(hide_code=True)
def _(
    alt,
    explore_y_slider,
    get_explored_y,
    mo,
    np,
    pl,
    reset_y_exploration_btn,
    run_y_exploration_btn,
    sc,
    set_explored_y,
):
    # Slide 2.5 — Explore overbooking levels interactively
    slide_2_5_explore = sc.create_slide(
        "Explore: How does Y affect revenue?",
        layout_type="side-by-side",
        page_number=16,
    )

    # Fixed parameters for exploration
    _C = 100
    _r = 150
    _c_bump = 400
    _noshow = 0.10

    def _simulate_overbooking(Y, n_simulations=1000):
        """Simulate net revenue for a given overbooking level."""
        np.random.seed(1234)  # Reproducible
        total_reservations = _C + Y
        revenues = []
        for _ in range(n_simulations):
            # No-shows follow binomial
            noshows = np.random.binomial(total_reservations, _noshow)
            arrivals = total_reservations - noshows
            occupied = min(arrivals, _C)
            bumped = max(0, arrivals - _C)
            revenue = occupied * _r - bumped * _c_bump
            revenues.append(revenue)
        return np.mean(revenues)

    # Handle reset button
    _explored = get_explored_y()
    if reset_y_exploration_btn.value:
        set_explored_y({})
        _explored = {}

    # Run simulation when button is clicked
    if run_y_exploration_btn.value:
        _Y = explore_y_slider.value
        _rev = _simulate_overbooking(_Y)
        if _Y not in _explored:
            set_explored_y({**_explored, _Y: _rev})
            _explored = {**_explored, _Y: _rev}

    # Build chart from explored data
    if _explored:
        _df = pl.DataFrame([
            {"Y": y, "Revenue": rev} for y, rev in sorted(_explored.items())
        ])
        _points = (
            alt.Chart(_df.to_pandas())
            .mark_circle(size=120, color="#2563eb")
            .encode(
                x=alt.X("Y:Q", title="Overbooking Level (Y)", scale=alt.Scale(domain=[0, 30])),
                y=alt.Y("Revenue:Q", title="Expected Net Revenue (€)", scale=alt.Scale(domain=[13000, 15500])),
                tooltip=["Y:Q", "Revenue:Q"],
            )
        )
        _line = (
            alt.Chart(_df.to_pandas())
            .mark_line(color="#2563eb", strokeWidth=2, opacity=0.5)
            .encode(x="Y:Q", y="Revenue:Q")
        )
        _chart = (_line + _points).properties(width=480, height=300)

        # Find best explored Y so far
        _best_y = max(_explored, key=_explored.get)
        _best_rev = _explored[_best_y]
        _status = mo.md(f"**Best so far:** Y = {_best_y} → €{_best_rev:,.0f}")
    else:
        _chart = mo.md("*Move the slider and click 'Test this Y' to explore*")
        _status = mo.md("*No data yet*")

    slide_2_5_explore.content1 = mo.vstack(
        [
            mo.md("""
    **Try different overbooking levels**

    How many extra reservations should we accept beyond capacity?

    - Y = 0: No overbooking (accept exactly 100)
    - Y = 10: Accept 110 reservations
    - Y = 20: Accept 120 reservations

    **Fixed parameters:**
    C = 100, r = €150, c_b = €400, no-show = 10%
    """),
            explore_y_slider,
            mo.hstack([run_y_exploration_btn, reset_y_exploration_btn, mo.md(f"Points explored: {len(_explored)}")]),
            _status,
        ],
        gap=0.5,
    )

    slide_2_5_explore.content2 = _chart

    slide_2_5_explore.render()
    return


@app.cell(hide_code=True)
def _(mo, sc):
    # Slide 2.6 — The critical fractile for overbooking
    slide_2_6_crit = sc.create_slide(
        "Finding the optimal overbooking level",
        layout_type="side-by-side",
        page_number=17,
    )

    slide_2_6_crit.content1 = mo.md(
        r"""
    **Again, a newsvendor problem!**

    **Underage cost** $C_u$: Overbook too little
    - An empty room
    - $C_u = r$ (lost revenue)

    **Overage cost** $C_o$: Overbook too much
    - A customer is bumped
    - $C_o = c_b$ (bumping cost)

    **Critical fractile:**

    $$\frac{C_u}{C_u + C_o} = \frac{r}{r + c_b}$$
    """
    )

    slide_2_6_crit.content2 = mo.md(
        r"""
    **Optimal overbooking level** $Y^*$:

    $$P(X \leq Y^*) = \frac{r}{r + c_b}$$

    **Interpretation:**

    Overbook until the probability of no-shows being at most $Y^*$ equals the critical ratio.

    Since bumping is expensive ($c_b > r$), we are conservative.

    **Our hotel:** $r = 150$, $c_b = 400$

    $$\frac{150}{150 + 400} \approx 0.27$$
    """
    )

    slide_2_6_crit.render()
    return


@app.cell(hide_code=True)
def _(mo):
    # UI elements for slide 2.7 - exploring what drives Y*
    explore_ob_revenue = mo.ui.slider(start=50, stop=300, step=25, value=150, label="Room revenue (€)")
    explore_ob_bump_cost = mo.ui.slider(start=100, stop=800, step=50, value=400, label="Bumping cost (€)")
    explore_ob_noshow = mo.ui.slider(start=0.05, stop=0.20, step=0.01, value=0.10, label="No-show rate")
    return explore_ob_bump_cost, explore_ob_noshow, explore_ob_revenue


@app.cell(hide_code=True)
def _(
    alt,
    explore_ob_bump_cost,
    explore_ob_noshow,
    explore_ob_revenue,
    mo,
    np,
    pl,
    sc,
    stats,
):
    # Slide 2.7 — Explore what drives Y*
    slide_2_7_sensitivity = sc.create_slide(
        "Explore: What drives the optimal Y*?",
        layout_type="side-by-side",
        page_number=18,
    )

    _C = 100  # Fixed capacity
    _r = explore_ob_revenue.value
    _c_bump = explore_ob_bump_cost.value
    _noshow = explore_ob_noshow.value

    # Compute critical fractile: r / (r + c_b)
    _crit_frac = _r / (_r + _c_bump)

    # Simpler textbook approach (Cachon & Terwiesch style):
    # No-shows from base capacity ~ Binomial(C, noshow_rate) ≈ Normal
    _ns_mean = _C * _noshow
    _ns_std = max(np.sqrt(_C * _noshow * (1 - _noshow)), 1)
    _Y_star = max(0, int(np.floor(stats.norm.ppf(_crit_frac, _ns_mean, _ns_std))))

    # Expected bumped customers at Y*
    # When no-shows < Y*, we bump (Y* - no-shows) customers
    # E[bumped] = E[max(0, Y* - no-shows)] using truncated normal formula
    _z = (_Y_star - _ns_mean) / _ns_std
    _expected_bumped = (_Y_star - _ns_mean) * stats.norm.cdf(_z) + _ns_std * stats.norm.pdf(_z)
    _actual_prob = stats.norm.cdf(_Y_star, _ns_mean, max(_ns_std, 1))
    _x = np.linspace(max(0, _ns_mean - 4 * _ns_std), _ns_mean + 4 * _ns_std, 200)
    _y = stats.norm.pdf(_x, _ns_mean, max(_ns_std, 1))
    _dist_df = pl.DataFrame({"x": _x, "density": _y})

    # Distribution curve
    _dist_curve = (
        alt.Chart(_dist_df.to_pandas())
        .mark_area(opacity=0.3, color="#2563eb")
        .encode(x=alt.X("x:Q", title="Number of no-shows"), y=alt.Y("density:Q", title="Probability density"))
    )

    # Shaded area up to Y*
    _shaded_df = pl.DataFrame({
        "x": [xi for xi in _x if xi <= _Y_star],
        "density": [yi for xi, yi in zip(_x, _y) if xi <= _Y_star],
    })
    _shaded_area = (
        alt.Chart(_shaded_df.to_pandas())
        .mark_area(opacity=0.5, color="#2563eb")
        .encode(x="x:Q", y="density:Q")
    )

    # Vertical line at Y*
    _y_line = (
        alt.Chart(pl.DataFrame({"Y": [_Y_star]}).to_pandas())
        .mark_rule(strokeDash=[5, 5], color="#dc2626", strokeWidth=2)
        .encode(x="Y:Q")
    )

    # Y* label
    _y_label = (
        alt.Chart(pl.DataFrame({"Y": [_Y_star], "y": [max(_y) * 0.8], "text": [f"Y* = {_Y_star}"]}).to_pandas())
        .mark_text(align="left", dx=5, fontSize=14, color="#dc2626")
        .encode(x="Y:Q", y="y:Q", text="text:N")
    )

    _chart = (_dist_curve + _shaded_area + _y_line + _y_label).properties(width=450, height=280)

    slide_2_7_sensitivity.content1 = mo.vstack(
        [
            mo.md("**Adjust parameters and observe how Y* changes:**"),
            explore_ob_revenue,
            explore_ob_bump_cost,
            explore_ob_noshow,
            mo.md("---"),
            mo.md(f"""
    **Results:**

    | Parameter | Value |
    |-----------|-------|
    | Critical ratio | $c_b / (r + c_b)$ = **{_crit_frac:.1%}** |
    | Optimal Y* | **{_Y_star}** extra reservations |
    | Total accepted | **{_C + _Y_star}** reservations |
    | Expected bumped | **{_expected_bumped:.2f}** customers |
    """),
            mo.md("""
    **Try these experiments:**
    - Change bump cost → What happens to Y*?
    - Change no-show rate → What happens to Y*?
    - Change Revenue → What happens to Y*?
    """),
        ],
        gap=0.3,
    )

    slide_2_7_sensitivity.content2 = mo.vstack([
        mo.md("**No-show distribution with Y* marked**"),
        _chart,
        mo.md(f"Shaded area = P(no-shows ≤ Y*) = {_actual_prob:.1%}"),
    ])

    slide_2_7_sensitivity.render()
    return


@app.cell(hide_code=True)
def _(mo, sc):
    # Slide 2.8 — Managerial takeaway
    slide_2_8_insight = sc.create_slide(
        "Overbooking: Key insight",
        layout_type="1-column",
        page_number=19,
    )

    slide_2_8_insight.content1 = mo.md(
        r"""
    **Overbooking is insurance against no-shows**

    **What we learned:**

    1. **No-shows waste capacity** — accepting exactly $C$ reservations leaves rooms empty
    2. **Overbooking balances two risks:**
       - Empty capacity (underbooking)
       - Bumping customers (overbooking too much)
    3. **The optimal $Y^*$ depends on:**
       - The **revenue-to-bump-cost ratio** $r / (r + c_b)$
       - The **no-show rate** distribution

    **Managerial insight:**

    Airlines, hotels, and restaurants all overbook — the question isn't *whether* to overbook,
    but *how much*. The answer depends on your bumping cost, which includes reputation effects.
    """
    )

    slide_2_8_insight.render()
    return


@app.cell(hide_code=True)
def _(sc):
    # Section 3 separator
    section_3 = sc.create_slide(
        "Combining the Levers",
        layout_type="section",
        page_number=20,
    )
    section_3.subtitle = "Section 3"
    section_3.content1 = "Using booking limits and overbooking together"
    section_3.render()
    return


@app.cell(hide_code=True)
def _(mo, sc):
    # Slide 3.1 — The Story So Far (recap)
    slide_3_1 = sc.create_slide(
        "The story so far",
        layout_type="side-by-side",
        page_number=21,
    )

    slide_3_1.content1 = mo.md(
        """
    **We now have two levers for revenue management**

    **Lever 1: Booking Limits** (Section 1)
    - Problem: Low-fare guests fill capacity before high-fare arrive
    - Solution: Protect Q* rooms for high-fare customers
    - Reduces waste from "selling too cheap"

    **Lever 2: Overbooking** (Section 2)
    - Problem: No-shows leave rooms empty
    - Solution: Accept Y* extra reservations
    - Reduces waste from "empty rooms"
    """
    )

    slide_3_1.content2 = mo.md(
        r"""
    **Each lever solves ONE problem**

    | Lever | Waste Addressed | Key Trade-off |
    |-------|-----------------|---------------|
    | Booking limits | Low revenue per room | Risk of empty rooms |
    | Overbooking | Empty rooms from no-shows | Risk of bumping |

    **But what if we face BOTH problems?**

    - No-shows leave rooms empty → need overbooking
    - Mixed fare classes → need booking limits
    - Most hotels and airlines face BOTH simultaneously
    """
    )

    slide_3_1.render()
    return


@app.cell(hide_code=True)
def _(np, pl, stats):
    # Combined simulation function
    def simulate_combined_policy(
        C, r_L, r_H, c_bump, Q, Y, mean_H, std_H, noshow_rate, n_simulations=5000
    ):
        """Simulate revenue outcomes under combined policy."""
        np.random.seed(1)

        B = (C + Y) - Q  # Booking limit for low-fare
        total_capacity = C + Y

        revenues = []
        bumped_list = []
        empty_list = []
        high_rejected_list = []

        for _ in range(n_simulations):
            # Low-fare demand (assume always exceeds booking limit)
            low_fare_booked = B

            # High-fare demand realization
            high_demand = max(0, int(np.random.normal(mean_H, std_H)))
            high_fare_booked = min(high_demand, Q)
            high_rejected = max(0, high_demand - Q)

            total_booked = low_fare_booked + high_fare_booked

            # No-shows
            noshows = np.random.binomial(total_booked, noshow_rate)
            arrivals = total_booked - noshows

            # Outcomes
            occupied = min(arrivals, C)
            bumped = max(0, arrivals - C)
            empty = max(0, C - arrivals)

            # Approximate revenue attribution
            # Assume high-fare customers arrive proportionally
            high_arrivals = int(high_fare_booked * (1 - noshow_rate))
            low_arrivals = arrivals - high_arrivals

            revenue = min(low_arrivals, C) * r_L
            if low_arrivals < C:
                revenue += min(high_arrivals, C - low_arrivals) * r_H
            revenue -= bumped * c_bump

            revenues.append(revenue)
            bumped_list.append(bumped)
            empty_list.append(empty)
            high_rejected_list.append(high_rejected)

        return {
            "mean_revenue": np.mean(revenues),
            "std_revenue": np.std(revenues),
            "mean_bumped": np.mean(bumped_list),
            "mean_empty": np.mean(empty_list),
            "mean_rejected_high": np.mean(high_rejected_list),
            "revenues": revenues,
        }

    def run_policy_comparison(C, r_L, r_H, c_bump, mean_H, std_H, noshow_rate):
        """Compare four policies."""
        # 1. FCFS only (Q=0, Y=0)
        fcfs = simulate_combined_policy(
            C, r_L, r_H, c_bump, Q=0, Y=0, mean_H=mean_H, std_H=std_H, noshow_rate=noshow_rate
        )

        # 2. Booking limits only (optimal Q, Y=0)
        crit_frac_bl = (r_H - r_L) / r_H
        Q_star = int(np.ceil(stats.norm.ppf(crit_frac_bl, mean_H, std_H)))
        Q_star = max(0, min(Q_star, C))
        bl_only = simulate_combined_policy(
            C, r_L, r_H, c_bump, Q=Q_star, Y=0, mean_H=mean_H, std_H=std_H, noshow_rate=noshow_rate
        )

        # 3. Overbooking only (Q=0, optimal Y)
        # No-shows ~ Binomial(C, noshow_rate) ≈ Normal(C·p, √(C·p·(1-p)))
        # Y* = floor(ppf(critical_ratio)) - accept while F(Y) ≤ critical_ratio
        crit_frac_ob = r_L / (r_L + c_bump)
        ns_mean = C * noshow_rate
        ns_std = max(np.sqrt(C * noshow_rate * (1 - noshow_rate)), 1)
        Y_star = max(0, int(np.floor(stats.norm.ppf(crit_frac_ob, ns_mean, ns_std))))
        ob_only = simulate_combined_policy(
            C, r_L, r_H, c_bump, Q=0, Y=Y_star, mean_H=mean_H, std_H=std_H, noshow_rate=noshow_rate
        )

        # 4. Combined (optimal Q on effective capacity, optimal Y)
        C_eff = C + Y_star
        Q_combined = int(np.ceil(stats.norm.ppf(crit_frac_bl, mean_H, std_H)))
        Q_combined = max(0, min(Q_combined, C_eff))
        combined = simulate_combined_policy(
            C,
            r_L,
            r_H,
            c_bump,
            Q=Q_combined,
            Y=Y_star,
            mean_H=mean_H,
            std_H=std_H,
            noshow_rate=noshow_rate,
        )

        return pl.DataFrame(
            {
                "Policy": ["FCFS", "Booking Limits", "Overbooking", "Combined"],
                "Q": [0, Q_star, 0, Q_combined],
                "Y": [0, 0, Y_star, Y_star],
                "Revenue": [
                    fcfs["mean_revenue"],
                    bl_only["mean_revenue"],
                    ob_only["mean_revenue"],
                    combined["mean_revenue"],
                ],
                "Empty": [
                    fcfs["mean_empty"],
                    bl_only["mean_empty"],
                    ob_only["mean_empty"],
                    combined["mean_empty"],
                ],
                "Bumped": [
                    fcfs["mean_bumped"],
                    bl_only["mean_bumped"],
                    ob_only["mean_bumped"],
                    combined["mean_bumped"],
                ],
                "Rejected High": [
                    fcfs["mean_rejected_high"],
                    bl_only["mean_rejected_high"],
                    ob_only["mean_rejected_high"],
                    combined["mean_rejected_high"],
                ],
            }
        )
    return run_policy_comparison, simulate_combined_policy


@app.cell(hide_code=True)
def _(alt, mo, pl, run_policy_comparison, sc):
    # Slide 3.2 — What's Missing? (simulation with bar chart)
    slide_3_2 = sc.create_slide(
        "What's missing?",
        layout_type="side-by-side",
        page_number=22,
    )

    # Get comparison data
    _comparison_df = run_policy_comparison(
        C=100, r_L=80, r_H=200, c_bump=400, mean_H=50, std_H=15, noshow_rate=0.10
    )

    # Filter to only 3 policies for discovery - Combined is revealed in Slide 3.4
    _df_three = _comparison_df.filter(pl.col("Policy") != "Combined")

    # Create bar chart for revenue comparison
    _revenue_chart = (
        alt.Chart(_df_three.to_pandas())
        .mark_bar()
        .encode(
            x=alt.X("Policy:N", sort=["FCFS", "Booking Limits", "Overbooking"], title=None),
            y=alt.Y("Revenue:Q", title="Average Revenue (€)"),
            color=alt.Color(
                "Policy:N",
                scale=alt.Scale(
                    domain=["FCFS", "Booking Limits", "Overbooking"],
                    range=["#94a3b8", "#3b82f6", "#f59e0b"],
                ),
                legend=None,
            ),
        )
        .properties(width=280, height=200, title="Revenue by Policy")
    )

    # Create stacked bar for waste sources (only 3 policies)
    _waste_data = pl.DataFrame(
        {
            "Policy": ["FCFS", "FCFS", "Booking Limits", "Booking Limits", "Overbooking", "Overbooking"],
            "Waste Type": ["Empty Rooms", "Rejected High-Fare", "Empty Rooms", "Rejected High-Fare", "Empty Rooms", "Rejected High-Fare"],
            "Count": [
                _df_three["Empty"][0], _df_three["Rejected High"][0],
                _df_three["Empty"][1], _df_three["Rejected High"][1],
                _df_three["Empty"][2], _df_three["Rejected High"][2],
            ],
        }
    )

    _waste_chart = (
        alt.Chart(_waste_data.to_pandas())
        .mark_bar()
        .encode(
            x=alt.X("Policy:N", sort=["FCFS", "Booking Limits", "Overbooking"], title=None),
            y=alt.Y("Count:Q", title="Average Count"),
            color=alt.Color(
                "Waste Type:N",
                scale=alt.Scale(domain=["Empty Rooms", "Rejected High-Fare"], range=["#ef4444", "#f97316"]),
            ),
            xOffset="Waste Type:N",
        )
        .properties(width=280, height=200, title="Sources of Waste")
    )

    slide_3_2.content1 = mo.vstack(
        [
            mo.md(
                """
    **Simulating a hotel with BOTH problems**

    **Scenario:** 100 rooms, €80/€200 fares, 10% no-shows

    Let's test each lever in isolation:
    - **FCFS**: No protection, no overbooking
    - **Booking limits only**: Protect for high-fare, but no overbooking
    - **Overbooking only**: Overbook, but no fare protection
    """
            ),
            mo.ui.altair_chart(_revenue_chart),
        ]
    )

    slide_3_2.content2 = mo.vstack(
        [
            mo.ui.altair_chart(_waste_chart),
            mo.md(
                """
    **What each lever misses:**

    | Policy | Empty Rooms | High-Fare Rejected |
    |--------|-------------|-------------------|
    | Booking limits only | ✓ Still has empties (no-shows) | Low |
    | Overbooking only | Low | ✓ Misses high-fare protection |

    *Each lever alone leaves value on the table!*
    """
            ),
        ]
    )

    slide_3_2.render()
    return


@app.cell(hide_code=True)
def _(mo, run_policy_comparison, sc):
    # Slide 3.3 — Can We Use Both? (transition)
    slide_3_3 = sc.create_slide(
        "Can we use both?",
        layout_type="side-by-side",
        page_number=23,
    )

    # Get comparison data to show specific numbers
    _comp_df = run_policy_comparison(
        C=100, r_L=80, r_H=200, c_bump=400, mean_H=50, std_H=15, noshow_rate=0.10
    )

    _bl_rev = _comp_df["Revenue"][1]
    _bl_empty = _comp_df["Empty"][1]
    _ob_rev = _comp_df["Revenue"][2]
    _ob_rejected = _comp_df["Rejected High"][2]

    slide_3_3.content1 = mo.md(
        f"""
    **The gap in each approach**

    **Booking limits alone:**
    - Revenue: €{_bl_rev:,.0f}
    - But: {_bl_empty:.1f} empty rooms (from no-shows)
    - *Good at fare protection, bad at filling rooms*

    **Overbooking alone:**
    - Revenue: €{_ob_rev:,.0f}
    - But: {_ob_rejected:.1f} high-fare customers rejected
    - *Good at filling rooms, bad at fare protection*
    """
    )

    slide_3_3.content2 = mo.md(
        """
    **The opportunity**

    What if we combined both levers?

    - Use **overbooking** to fill no-show gaps
    - Use **booking limits** to protect high-fare seats

    **The challenge:** How do they interact?
    - If we overbook, we have more total capacity...
    - But we still need to protect for high-fare...
    - Does one lever affect the other?

    *Let's develop a systematic approach!*
    """
    )

    slide_3_3.render()
    return


@app.cell(hide_code=True)
def _(mo, sc):
    # Slide 3.4 — The Sequential Heuristic
    slide_3_4 = sc.create_slide(
        "The sequential heuristic",
        layout_type="side-by-side",
        page_number=24,
    )

    slide_3_4.content1 = mo.md(
        """
    **A simple sequential approach**

    We can combine both levers using a **two-step heuristic**:

    **The Sequential Heuristic:**

    1. **First**, compute optimal overbooking Y*
       - Based on no-show rate and bump cost
       - Same formula as Section 2

    2. **Then**, define **virtual capacity**
       - $C' = C + Y^*$
       - We're "creating" extra sellable capacity

    3. **Finally**, compute protection level Q*
       - Apply booking limit logic on C'
       - Same formula as Section 1

    *This is known as the **virtual capacity method**.*
    """
    )

    slide_3_4.content2 = mo.md(
        r"""
    **The combined policy**

    **Booking limit for low-fare:**

    $$B^* = C' - Q^* = (C + Y^*) - Q^*$$

    **Example:**
    - Capacity $C = 100$
    - Optimal overbooking $Y^* = 8$
    - Effective capacity $C' = 108$
    - Protection level $Q^* = 54$
    - **Booking limit** $B^* = 108 - 54 = 54$

    **Interpretation:**
    - Accept up to 54 low-fare bookings
    - Accept up to 108 total bookings
    - Protect 54 seats for high-fare
    """
    )

    slide_3_4.render()
    return


@app.cell(hide_code=True)
def _(mo):
    # State for Slide 3.5 — Sensitivity analysis sliders
    sensitivity_noshow = mo.ui.slider(
        start=0.02, stop=0.25, step=0.02, value=0.10, label="No-show rate", show_value=True
    )
    sensitivity_fare_ratio = mo.ui.slider(
        start=1.5, stop=5.0, step=0.5, value=2.5, label="Fare ratio (r_H/r_L)", show_value=True
    )
    sensitivity_bump_ratio = mo.ui.slider(
        start=0.5, stop=8.0, step=0.5, value=5.0, label="Bump cost ratio (c_bump/r_L)", show_value=True
    )
    return sensitivity_bump_ratio, sensitivity_fare_ratio, sensitivity_noshow


@app.cell(hide_code=True)
def _(
    alt,
    mo,
    np,
    pl,
    sc,
    sensitivity_bump_ratio,
    sensitivity_fare_ratio,
    sensitivity_noshow,
    simulate_combined_policy,
    stats,
):
    # Slide 3.5 — How Much Does Combining Help?
    slide_3_5 = sc.create_slide(
        "How much does combining help?",
        layout_type="side-by-side",
        page_number=25,
    )

    # Fixed base parameters
    _C = 100
    _r_L = 80
    _mean_H = 50
    _std_H = 15

    # Variable parameters from sliders
    _noshow_rate = sensitivity_noshow.value
    _fare_ratio = sensitivity_fare_ratio.value
    _bump_ratio = sensitivity_bump_ratio.value
    _r_H = _r_L * _fare_ratio
    _c_bump = _r_L * _bump_ratio

    # Calculate optimal Y (simpler textbook approach)
    # No-shows from base capacity ~ Binomial(C, noshow_rate) ≈ Normal
    _crit_frac_ob = _r_L / (_r_L + _c_bump)
    _ns_mean = _C * _noshow_rate
    _ns_std = max(np.sqrt(_C * _noshow_rate * (1 - _noshow_rate)), 1)
    _Y_star = max(0, int(np.floor(stats.norm.ppf(_crit_frac_ob, _ns_mean, _ns_std))))

    # Calculate optimal Q
    _crit_frac_bl = (_r_H - _r_L) / _r_H
    _Q_star = int(np.ceil(stats.norm.ppf(_crit_frac_bl, _mean_H, _std_H)))
    _Q_star = max(0, min(_Q_star, _C + _Y_star))

    # Simulate four policies
    _fcfs = simulate_combined_policy(
        _C, _r_L, _r_H, _c_bump, Q=0, Y=0,
        mean_H=_mean_H, std_H=_std_H, noshow_rate=_noshow_rate
    )
    _bl_only = simulate_combined_policy(
        _C, _r_L, _r_H, _c_bump, Q=_Q_star, Y=0,
        mean_H=_mean_H, std_H=_std_H, noshow_rate=_noshow_rate
    )
    _ob_only = simulate_combined_policy(
        _C, _r_L, _r_H, _c_bump, Q=0, Y=_Y_star,
        mean_H=_mean_H, std_H=_std_H, noshow_rate=_noshow_rate
    )
    _combined = simulate_combined_policy(
        _C, _r_L, _r_H, _c_bump, Q=_Q_star, Y=_Y_star,
        mean_H=_mean_H, std_H=_std_H, noshow_rate=_noshow_rate
    )

    # Calculate gains
    _best_single = max(_bl_only["mean_revenue"], _ob_only["mean_revenue"])
    _gain_vs_single = _combined["mean_revenue"] - _best_single
    _gain_pct = (_gain_vs_single / _best_single) * 100 if _best_single > 0 else 0

    # Create comparison bar chart
    _compare_df = pl.DataFrame({
        "Policy": ["FCFS (No RM)", "Booking Limits Only", "Overbooking Only", "Combined"],
        "Revenue": [_fcfs["mean_revenue"], _bl_only["mean_revenue"], _ob_only["mean_revenue"], _combined["mean_revenue"]],
    })

    _bar_chart = (
        alt.Chart(_compare_df.to_pandas())
        .mark_bar()
        .encode(
            x=alt.X("Policy:N", sort=["FCFS (No RM)", "Booking Limits Only", "Overbooking Only", "Combined"], title=None),
            y=alt.Y("Revenue:Q", title="Average Revenue (€)"),
            color=alt.Color(
                "Policy:N",
                scale=alt.Scale(
                    domain=["FCFS (No RM)", "Booking Limits Only", "Overbooking Only", "Combined"],
                    range=["#9ca3af", "#3b82f6", "#f59e0b", "#22c55e"],
                ),
                legend=None,
            ),
        )
        .properties(width=320, height=200)
    )

    slide_3_5.content1 = mo.vstack(
        [
            mo.md(
                """
    **Experiment: When does combining help most?**

    Adjust the parameters and observe how the **gain from combining** changes.
    """
            ),
            sensitivity_noshow,
            sensitivity_fare_ratio,
            sensitivity_bump_ratio,
            mo.md(
                f"""
    **Current parameters:**
    - No-show rate: {_noshow_rate:.0%}
    - Fares: €{_r_L:.0f} / €{_r_H:.0f}
    - Bump cost: €{_c_bump:.0f}
    - Optimal: Q* = {_Q_star}, Y* = {_Y_star}
    """
            ),
        ]
    )

    slide_3_5.content2 = mo.vstack(
        [
            mo.ui.altair_chart(_bar_chart),
            mo.md(
                f"""
    **Gain from combining:**
    - Best single lever: €{_best_single:,.0f}
    - Combined: €{_combined['mean_revenue']:,.0f}
    - **Additional gain: €{_gain_vs_single:,.0f} ({_gain_pct:.1f}%)**
    """
            ),
        ]
    )

    slide_3_5.render()
    return


@app.cell(hide_code=True)
def _(mo, sc):
    # Slide 3.6 — Key Insight (synthesis)
    slide_3_6 = sc.create_slide(
        "Key insight: Both levers work together",
        layout_type="2-column",
        page_number=26,
    )

    slide_3_6.content1 = mo.md(
        """
    **What we discovered:**

    1. **Each lever alone is incomplete**
       - Booking limits miss the no-show opportunity
       - Overbooking misses the fare mix opportunity

    2. **Combining is better than either alone**
       - Address BOTH sources of waste simultaneously
       - The gain depends on the severity of each problem

    **The sequential heuristic:**
    3. **Simple and effective approach**
       - Compute Y* first (overbooking)
       - Then compute Q* on effective capacity
       - Order matters: overbooking expands the "pie"
    """
    )

    slide_3_6.content2 = mo.md(
        """
    **In practice:**
    - Airlines/hotels use these principles with many fare classes
    - Modern RM systems automate the optimization
    - The core trade-offs we explored remain the same
    """
    )

    slide_3_6.render()
    return


@app.cell(hide_code=True)
def _(sc):
    # Section 4 separator
    section_4 = sc.create_slide(
        "Summary & Key Takeaways",
        layout_type="section",
        page_number=27,
    )
    section_4.subtitle = "Section 4"
    section_4.render()
    return


@app.cell(hide_code=True)
def _(mo, sc):
    # Slide 4.1 — Summary
    slide_4_1 = sc.create_slide(
        "Capacity control: The big picture",
        layout_type="1-column",
        page_number=28,
    )

    slide_4_1.content1 = mo.md(
        r"""
    **Allocate scarce, perishable capacity under uncertainty**

    | Lever | Problem Addressed | Key Trade-off |
    |-------|------------------|---------------|
    | **Booking limits** | High-value demand arrives late | Spoiled capacity vs. rejected high-fare |
    | **Overbooking** | No-shows waste capacity | Empty rooms vs. bumped customers |
    | **Combining both** | Both problems occur simultaneously | Sequential heuristic balances both |

    **The common thread:** Both are **newsvendor problems**

    **When is capacity control appropriate?**
    - Perishable capacity (can't store)
    - Fixed short-term capacity
    - Segmentable customers
    - Demand uncertainty
    """
    )

    slide_4_1.render()
    return


if __name__ == "__main__":
    app.run()

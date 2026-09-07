"""ResumeIQ PDF report generation.

This module formats analysis results already produced by ResumeIQ into a
professional PDF. It intentionally contains no resume/ATS/AI analysis logic.
"""

from io import BytesIO
import re
from datetime import datetime
from typing import Any, Dict, Iterable

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)


def _safe(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "Yes" if value else "No"
    return str(value).strip()


def _items(value: Any) -> list:
    return value if isinstance(value, list) else []


def _obj(value: Any) -> dict:
    return value if isinstance(value, dict) else {}


def _clean_filename(name: str) -> str:
    name = re.sub(r"[^A-Za-z0-9._-]+", "_", name or "")
    return name.strip("._-") or "Candidate"


def get_report_filename(report_data: Dict[str, Any]) -> str:
    candidate = _obj(_obj(report_data.get("resumeAnalysis")).get("candidate"))
    name = _safe(candidate.get("name"))
    if name and name.lower() not in {"not detected", "unknown"}:
        return f"ResumeIQ_{_clean_filename(name)}_Report.pdf"
    return "ResumeIQ_Report.pdf"


class NumberedCanvasMixin:
    """Adds page numbers without requiring a custom canvas implementation."""


def _footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#6B7280"))
    canvas.drawString(18 * mm, 10 * mm, "ResumeIQ — AI Resume Intelligence Report")
    canvas.drawRightString(192 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


def _bullet_list(items: Iterable[Any], styles: dict, empty_text: str = "Not available") -> list:
    values = [_safe(item) for item in items if _safe(item)]
    if not values:
        return [Paragraph(empty_text, styles["Muted"])]
    return [Paragraph(f"• {_escape(v)}", styles["BodySmall"]) for v in values]


def _escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def _paragraph(value: Any, style) -> Paragraph:
    text = _safe(value)
    return Paragraph(_escape(text).replace("\n", "<br/>") if text else "Not available", style)


def _section_title(title: str, styles: dict):
    return [Spacer(1, 5 * mm), Paragraph(_escape(title), styles["Section"]), Spacer(1, 2 * mm)]


def _table(rows, styles, widths=None):
    converted = []
    for row in rows:
        converted.append([
            Paragraph(_escape(_safe(cell)), styles["TableCell"]) if not hasattr(cell, "wrap") else cell
            for cell in row
        ])
    table = Table(converted, colWidths=widths, repeatRows=1 if len(converted) > 1 else 0, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EEF2FF")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#3730A3")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#D1D5DB")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return table


def generate_report_pdf(report_data: Dict[str, Any]) -> bytes:
    """Generate a PDF using only the supplied, already-computed ResumeIQ data."""

    resume = _obj(report_data.get("resumeAnalysis"))
    candidate = _obj(resume.get("candidate"))
    score = _obj(resume.get("score"))
    breakdown = _obj(score.get("breakdown"))
    ats = _obj(report_data.get("atsAnalysis"))
    skill_gap = _obj(report_data.get("skillGapAnalysis"))
    career = _obj(report_data.get("careerAnalysis"))
    ai = _obj(career.get("ai_analysis"))
    engine = _obj(career.get("career_engine"))
    assistant_messages = _items(report_data.get("assistantMessages"))
    filename = _safe(report_data.get("resumeFilename")) or _safe(_obj(report_data.get("file")).get("filename"))
    page_count = resume.get("page_count") or _obj(report_data.get("file")).get("pages") or ""
    generation_date = datetime.now().strftime("%d %B %Y")

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="TitleIQ", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=24, leading=29, textColor=colors.HexColor("#111827"), alignment=TA_CENTER, spaceAfter=3 * mm))
    styles.add(ParagraphStyle(name="SubtitleIQ", parent=styles["Normal"], fontName="Helvetica", fontSize=12, leading=16, textColor=colors.HexColor("#4F46E5"), alignment=TA_CENTER, spaceAfter=8 * mm))
    styles.add(ParagraphStyle(name="Section", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=colors.HexColor("#3730A3"), spaceBefore=4 * mm, spaceAfter=2 * mm))
    styles.add(ParagraphStyle(name="BodySmall", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.5, leading=14, textColor=colors.HexColor("#1F2937"), spaceAfter=1.5 * mm))
    styles.add(ParagraphStyle(name="Muted", parent=styles["BodyText"], fontName="Helvetica-Oblique", fontSize=9.5, leading=14, textColor=colors.HexColor("#6B7280")))
    styles.add(ParagraphStyle(name="TableCell", parent=styles["BodyText"], fontName="Helvetica", fontSize=8.5, leading=12, textColor=colors.HexColor("#1F2937")))
    styles.add(ParagraphStyle(name="Metric", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=18, leading=21, textColor=colors.HexColor("#111827"), alignment=TA_CENTER))
    styles.add(ParagraphStyle(name="MetricLabel", parent=styles["BodyText"], fontName="Helvetica", fontSize=8, leading=10, textColor=colors.HexColor("#6B7280"), alignment=TA_CENTER))

    buffer = BytesIO()
    doc = BaseDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=17 * mm,
        bottomMargin=16 * mm,
        title="ResumeIQ AI Resume Intelligence Report",
        author="ResumeIQ",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
    doc.addPageTemplates([PageTemplate(id="ResumeIQ", frames=frame, onPage=_footer)])

    story = []

    # 1. Header
    story.append(Spacer(1, 12 * mm))
    story.append(Paragraph("ResumeIQ", styles["TitleIQ"]))
    story.append(Paragraph("AI Resume Intelligence Report", styles["SubtitleIQ"]))
    header_rows = [["Candidate", _safe(candidate.get("name")) or "Not detected"],
                   ["Email", _safe(candidate.get("email")) or "Not detected"],
                   ["Phone", _safe(candidate.get("phone")) or "Not detected"],
                   ["Resume", filename or "Not available"],
                   ["Generated", generation_date]]
    story.append(_table([["Field", "Value"]] + header_rows, styles, [45 * mm, 125 * mm]))

    # 2. Resume overview
    story.extend(_section_title("1. Resume Overview", styles))
    metrics = [
        [_safe(score.get("total")) or "0", "Overall Score"],
        [str(len(_items(resume.get("skills")))), "Skills Found"],
        [_safe(resume.get("word_count")) or "0", "Word Count"],
        [str(len(_items(resume.get("sections")))), "Sections"],
        [_safe(page_count) or "Not available", "Page Count"],
    ]
    metric_table = Table([[Paragraph(_escape(v), styles["Metric"]), Paragraph(_escape(label), styles["MetricLabel"])] for v, label in metrics], colWidths=[28 * mm, 32 * mm] * 0 + [34 * mm, 34 * mm, 34 * mm, 34 * mm, 34 * mm], hAlign="LEFT")
    # Five compact metric cells in one row.
    metric_table = Table([[Paragraph(_escape(v), styles["Metric"]) for v, _ in metrics], [Paragraph(_escape(label), styles["MetricLabel"]) for _, label in metrics]], colWidths=[34 * mm] * 5)
    metric_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ("BOX", (0, 0), (-1, -1), 0.4, colors.HexColor("#D1D5DB")),
        ("INNERGRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#E5E7EB")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    story.append(metric_table)

    # 3. Score breakdown
    story.extend(_section_title("2. Resume Score Breakdown", styles))
    rows = [["Component", "Score"]]
    labels = {
        "contact_information": "Contact Information",
        "sections": "Sections",
        "skills": "Skills",
        "projects_or_experience": "Projects / Experience",
        "certifications_or_achievements": "Certifications / Achievements",
    }
    for key, label in labels.items():
        if key in breakdown and breakdown.get(key) not in (None, ""):
            rows.append([label, _safe(breakdown.get(key))])
    if len(rows) == 1:
        rows.append(["Breakdown", "Not available"])
    rows.append(["Overall Score", _safe(score.get("total")) or "Not available"])
    story.append(_table(rows, styles, [115 * mm, 55 * mm]))

    # 4. Skills
    story.extend(_section_title("3. Detected Skills", styles))
    story.extend(_bullet_list(resume.get("skills"), styles, "No skills detected."))

    # 5. ATS
    story.extend(_section_title("4. ATS Analysis", styles))
    if ats:
        ats_score = ats.get("score")
        if ats_score not in (None, ""):
            story.append(Paragraph(f"<b>ATS Match Score:</b> {_escape(_safe(ats_score))}/100", styles["BodySmall"]))
        recommendations = _items(ats.get("recommendations"))
        if recommendations:
            story.append(Paragraph("<b>Recommendations</b>", styles["BodySmall"]))
            story.extend(_bullet_list(recommendations, styles))
        skills = _obj(ats.get("skills"))
        keywords = _obj(ats.get("keywords"))
        ats_rows = [["Category", "Values"]]
        for label, values in [
            ("Matching Skills", skills.get("matched")),
            ("Missing Skills", skills.get("missing")),
            ("Resume-only Skills", skills.get("resume_only")),
            ("Matched Keywords", keywords.get("matched")),
            ("Missing Keywords", keywords.get("missing")),
        ]:
            vals = ", ".join(_safe(v) for v in _items(values) if _safe(v))
            if vals:
                ats_rows.append([label, vals])
        breakdown_ats = _obj(ats.get("breakdown"))
        for key, value in breakdown_ats.items():
            if isinstance(value, dict):
                raw = value.get("raw_score")
                weighted = value.get("weighted_score")
                val = f"Raw: {_safe(raw)}; Weighted: {_safe(weighted)}"
            else:
                val = _safe(value)
            if val:
                ats_rows.append([f"Score Breakdown — {key}", val])
        if len(ats_rows) > 1:
            story.append(_table(ats_rows, styles, [55 * mm, 115 * mm]))
        else:
            story.append(Paragraph("ATS analysis was performed, but no additional result details were returned.", styles["Muted"]))
    else:
        story.append(Paragraph("ATS analysis was not performed.", styles["Muted"]))

    # 6. Skill gap
    story.extend(_section_title("5. Skill Gap Analysis", styles))
    if skill_gap:
        if skill_gap.get("coverage") not in (None, ""):
            story.append(Paragraph(f"<b>Skill Coverage:</b> {_escape(_safe(skill_gap.get('coverage')))}%", styles["BodySmall"]))
        summary = _obj(skill_gap.get("summary"))
        for key, label in [("required_skills", "Required Skills"), ("matched_skills", "Matched Skills"), ("missing_skills", "Missing Skills")]:
            if key in summary:
                story.append(Paragraph(f"<b>{label}:</b> {_escape(_safe(summary.get(key)))}", styles["BodySmall"]))
        for label, key in [("Required Skills", "required_skills"), ("Matched Skills", "matched_skills"), ("Missing Skills", "missing_skills")]:
            vals = _items(skill_gap.get(key))
            if vals:
                story.append(Paragraph(f"<b>{label}</b>", styles["BodySmall"]))
                story.extend(_bullet_list(vals, styles))
        gaps = _items(skill_gap.get("gaps"))
        if gaps:
            gap_rows = [["Skill", "Priority", "Reason", "Learning Focus"]]
            for gap in gaps:
                g = _obj(gap)
                gap_rows.append([_safe(g.get("skill")) or "Not available", _safe(g.get("priority")) or "Not available", _safe(g.get("reason")) or "Not available", _safe(g.get("learning_focus")) or "Not available"])
            story.append(_table(gap_rows, styles, [34 * mm, 23 * mm, 57 * mm, 56 * mm]))
    else:
        story.append(Paragraph("Skill gap analysis was not performed.", styles["Muted"]))

    # 7. Career recommendation
    story.extend(_section_title("6. Career Recommendation", styles))
    if career:
        rec = _obj(ai.get("recommended_career"))
        if rec:
            story.append(Paragraph(f"<b>Best Career Match:</b> {_escape(_safe(rec.get('title')) or 'Not available')}", styles["BodySmall"]))
            if rec.get("fit_score") not in (None, ""):
                story.append(Paragraph(f"<b>Match Percentage:</b> {_escape(_safe(rec.get('fit_score')))}%", styles["BodySmall"]))
            if rec.get("reason"):
                story.append(Paragraph(f"<b>Reason:</b> {_escape(_safe(rec.get('reason')))}", styles["BodySmall"]))
        recommendations = _items(engine.get("recommendations"))
        if recommendations:
            rows = [["Career", "Score"]] + [[_safe(r.get("career")), _safe(r.get("score"))] for r in recommendations if isinstance(r, dict)]
            if len(rows) > 1:
                story.append(_table(rows, styles, [125 * mm, 45 * mm]))
    else:
        story.append(Paragraph("Career recommendation analysis was not performed.", styles["Muted"]))

    # 8. Gemini Career Intelligence
    story.extend(_section_title("7. Gemini Career Intelligence", styles))
    if ai:
        for key, label in [("career_summary", "Career Summary"), ("final_advice", "Final Advice")]:
            if ai.get(key):
                story.append(Paragraph(f"<b>{label}</b>", styles["BodySmall"]))
                story.append(_paragraph(ai.get(key), styles["BodySmall"]))
        for key, label in [("current_strengths", "Current Strengths"), ("missing_skills", "Missing Skills")]:
            values = _items(ai.get(key))
            if values:
                story.append(Paragraph(f"<b>{label}</b>", styles["BodySmall"]))
                story.extend(_bullet_list(values, styles))
        recommended_skills = _items(ai.get("recommended_skills"))
        if recommended_skills:
            rows = [["Skill", "Priority", "Reason"]]
            for item in recommended_skills:
                x = _obj(item)
                rows.append([_safe(x.get("skill")), _safe(x.get("priority")), _safe(x.get("reason"))])
            story.append(_table(rows, styles, [45 * mm, 25 * mm, 100 * mm]))
        projects = _items(ai.get("recommended_projects"))
        if projects:
            story.append(Paragraph("<b>Recommended Projects</b>", styles["BodySmall"]))
            for project in projects:
                p = _obj(project)
                title = _safe(p.get("title")) or "Project"
                story.append(Paragraph(f"<b>{_escape(title)}</b>", styles["BodySmall"]))
                if p.get("description"):
                    story.append(_paragraph(p.get("description"), styles["BodySmall"]))
                skills = _items(p.get("skills"))
                if skills:
                    story.append(Paragraph(f"Skills: {_escape(', '.join(_safe(s) for s in skills))}", styles["BodySmall"]))
        roadmap = _obj(ai.get("roadmap"))
        roadmap_rows = [["Period", "Roadmap"]]
        for key, label in [("days_30", "30 Days"), ("days_60", "60 Days"), ("days_90", "90 Days")]:
            values = _items(roadmap.get(key))
            if values:
                roadmap_rows.append([label, "\n".join(f"• {_safe(v)}" for v in values)])
        if len(roadmap_rows) > 1:
            story.append(_table(roadmap_rows, styles, [30 * mm, 140 * mm]))
    else:
        story.append(Paragraph("Gemini career intelligence was not performed.", styles["Muted"]))

    # 9. Assistant summary — only if actual interactions exist.
    if assistant_messages:
        story.extend(_section_title("8. AI Assistant Summary", styles))
        for message in assistant_messages[-6:]:
            msg = _obj(message)
            role = _safe(msg.get("role")) or "Assistant"
            text = _safe(msg.get("message"))
            if text:
                story.append(Paragraph(f"<b>{_escape(role)}</b>", styles["BodySmall"]))
                story.append(_paragraph(text, styles["BodySmall"]))

    # 10. Final summary derived only from returned modules.
    story.extend(_section_title("9. Final Summary", styles))
    strengths = []
    if score.get("total") not in (None, ""):
        strengths.append(f"Overall resume score: {_safe(score.get('total'))}/100.")
    if _items(resume.get("skills")):
        strengths.append(f"Detected {_safe(len(_items(resume.get('skills'))))} skills.")
    if _items(resume.get("sections")):
        strengths.append(f"Detected {_safe(len(_items(resume.get('sections'))))} resume sections.")
    ai_strengths = _items(ai.get("current_strengths"))
    if ai_strengths:
        strengths.extend(_safe(v) for v in ai_strengths[:4] if _safe(v))
    if strengths:
        story.append(Paragraph("<b>Resume strengths</b>", styles["BodySmall"]))
        story.extend(_bullet_list(strengths, styles))

    gaps = []
    gaps.extend(_items(skill_gap.get("missing_skills")))
    gaps.extend(_items(_obj(ats.get("skills")).get("missing")))
    gaps.extend(_items(ai.get("missing_skills")))
    # Preserve order while removing duplicates.
    unique_gaps = []
    seen = set()
    for gap in gaps:
        g = _safe(gap)
        if g and g.lower() not in seen:
            seen.add(g.lower())
            unique_gaps.append(g)
    if unique_gaps:
        story.append(Paragraph("<b>Important skill gaps</b>", styles["BodySmall"]))
        story.extend(_bullet_list(unique_gaps[:10], styles))

    if rec_title := _safe(_obj(ai.get("recommended_career")).get("title")):
        story.append(Paragraph(f"<b>Recommended career direction:</b> {_escape(rec_title)}", styles["BodySmall"]))
    elif recommendations := _items(engine.get("recommendations")):
        top = _obj(recommendations[0])
        if top.get("career"):
            story.append(Paragraph(f"<b>Recommended career direction:</b> {_escape(_safe(top.get('career')))}", styles["BodySmall"]))

    next_steps = []
    roadmap = _obj(ai.get("roadmap"))
    next_steps.extend(_items(roadmap.get("days_30")))
    next_steps.extend([
        _safe(_obj(g).get("learning_focus"))
        for g in _items(skill_gap.get("gaps"))
        if _safe(_obj(g).get("learning_focus"))
    ])
    if next_steps:
        story.append(Paragraph("<b>Most important next steps</b>", styles["BodySmall"]))
        story.extend(_bullet_list(next_steps[:8], styles))

    doc.build(story)
    return buffer.getvalue()


def report_filename(report_data: Dict[str, Any]) -> str:
    resume = _obj(report_data.get("resumeAnalysis"))
    candidate = _obj(resume.get("candidate"))
    name = _safe(candidate.get("name"))
    if name:
        safe_name = re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("._-")
        if safe_name:
            return f"ResumeIQ_{safe_name}_Report.pdf"
    return "ResumeIQ_Report.pdf"

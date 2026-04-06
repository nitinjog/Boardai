"""
PDF generation for CBSE mock test papers and evaluation reports.
Uses reportlab for professional formatting.
"""
import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from app.config import settings

logger = logging.getLogger(__name__)

# Color palette
DARK_BLUE = colors.HexColor("#1e3a5f")
ACCENT_BLUE = colors.HexColor("#2563eb")
LIGHT_BLUE = colors.HexColor("#eff6ff")
DARK_GRAY = colors.HexColor("#374151")
MEDIUM_GRAY = colors.HexColor("#6b7280")
LIGHT_GRAY = colors.HexColor("#f3f4f6")
SUCCESS_GREEN = colors.HexColor("#059669")
WARNING_AMBER = colors.HexColor("#d97706")
ERROR_RED = colors.HexColor("#dc2626")


def _make_styles():
    base = getSampleStyleSheet()
    styles = {}

    styles["school_name"] = ParagraphStyle(
        "school_name",
        fontName="Helvetica-Bold",
        fontSize=16,
        textColor=DARK_BLUE,
        alignment=TA_CENTER,
        spaceAfter=2,
    )
    styles["exam_title"] = ParagraphStyle(
        "exam_title",
        fontName="Helvetica-Bold",
        fontSize=13,
        textColor=DARK_BLUE,
        alignment=TA_CENTER,
        spaceAfter=4,
    )
    styles["info_label"] = ParagraphStyle(
        "info_label",
        fontName="Helvetica-Bold",
        fontSize=10,
        textColor=DARK_GRAY,
    )
    styles["info_value"] = ParagraphStyle(
        "info_value",
        fontName="Helvetica",
        fontSize=10,
        textColor=DARK_GRAY,
    )
    styles["section_header"] = ParagraphStyle(
        "section_header",
        fontName="Helvetica-Bold",
        fontSize=11,
        textColor=colors.white,
        backColor=DARK_BLUE,
        spaceBefore=12,
        spaceAfter=6,
        leftIndent=6,
        rightIndent=6,
        borderPad=4,
    )
    styles["question_text"] = ParagraphStyle(
        "question_text",
        fontName="Helvetica",
        fontSize=10,
        textColor=DARK_GRAY,
        leading=14,
        spaceAfter=4,
    )
    styles["option_text"] = ParagraphStyle(
        "option_text",
        fontName="Helvetica",
        fontSize=10,
        textColor=DARK_GRAY,
        leftIndent=20,
        leading=13,
    )
    styles["marks_badge"] = ParagraphStyle(
        "marks_badge",
        fontName="Helvetica-Bold",
        fontSize=9,
        textColor=ACCENT_BLUE,
        alignment=TA_RIGHT,
    )
    styles["instruction"] = ParagraphStyle(
        "instruction",
        fontName="Helvetica",
        fontSize=9,
        textColor=MEDIUM_GRAY,
        leading=13,
    )
    styles["report_title"] = ParagraphStyle(
        "report_title",
        fontName="Helvetica-Bold",
        fontSize=18,
        textColor=DARK_BLUE,
        alignment=TA_CENTER,
        spaceAfter=6,
    )
    styles["score_big"] = ParagraphStyle(
        "score_big",
        fontName="Helvetica-Bold",
        fontSize=32,
        textColor=SUCCESS_GREEN,
        alignment=TA_CENTER,
    )
    styles["body"] = ParagraphStyle(
        "body",
        fontName="Helvetica",
        fontSize=10,
        textColor=DARK_GRAY,
        leading=14,
    )
    return styles


def generate_question_paper(
    test_session_data: Dict,
    student_name: str,
    output_filename: str,
) -> str:
    """
    Generate a CBSE-style question paper PDF.
    Returns the file path.
    """
    os.makedirs(settings.PDF_OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(settings.PDF_OUTPUT_DIR, output_filename)
    styles = _make_styles()

    doc = SimpleDocTemplate(
        filepath,
        pagesize=A4,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
    )

    story = []

    # ── Header ────────────────────────────────────────────────────────────────
    story.append(Paragraph("BoardAI – CBSE Mock Test Platform", styles["school_name"]))
    story.append(Paragraph(
        f"Class {test_session_data['class_level']} – {test_session_data['subject']} Mock Examination",
        styles["exam_title"],
    ))
    story.append(HRFlowable(width="100%", thickness=2, color=DARK_BLUE, spaceAfter=6))

    # Info table
    info_data = [
        [
            Paragraph("<b>Student:</b>", styles["info_label"]),
            Paragraph(student_name, styles["info_value"]),
            Paragraph("<b>Date:</b>", styles["info_label"]),
            Paragraph(datetime.now().strftime("%d %B %Y"), styles["info_value"]),
        ],
        [
            Paragraph("<b>Maximum Marks:</b>", styles["info_label"]),
            Paragraph(str(test_session_data["total_marks"]), styles["info_value"]),
            Paragraph("<b>Time Allowed:</b>", styles["info_label"]),
            Paragraph(f"{test_session_data['duration_minutes']} Minutes", styles["info_value"]),
        ],
    ]
    info_table = Table(info_data, colWidths=[3.5 * cm, 6 * cm, 3.5 * cm, 4 * cm])
    info_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BLUE),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.lightblue),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 10))

    # General instructions
    story.append(Paragraph("<b>General Instructions:</b>", styles["info_label"]))
    instructions = [
        "1. This question paper contains multiple sections. Read each section carefully before answering.",
        "2. All questions are compulsory unless stated otherwise.",
        "3. Write your answers neatly in the space provided below each question.",
        "4. For MCQs, write only the letter (A/B/C/D) of the correct option.",
        "5. Marks are indicated against each question.",
    ]
    for instr in instructions:
        story.append(Paragraph(instr, styles["instruction"]))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1, color=MEDIUM_GRAY, spaceAfter=8))

    # ── Sections ──────────────────────────────────────────────────────────────
    sections = test_session_data.get("sections", [])
    q_number = 1

    for section in sections:
        story.append(Paragraph(
            f"  {section['name']}  –  {section['description']}  ({section['total_marks']} Marks)",
            styles["section_header"],
        ))
        story.append(Spacer(1, 4))

        for q in section["questions"]:
            # Question header row
            q_header = Table(
                [[
                    Paragraph(f"Q{q_number}. {q['question']}", styles["question_text"]),
                    Paragraph(f"[{q['marks']} Mark{'s' if q['marks'] > 1 else ''}]", styles["marks_badge"]),
                ]],
                colWidths=[13.5 * cm, 3 * cm],
            )
            q_header.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (0, 0), 0),
            ]))
            story.append(q_header)

            # Options for MCQ
            if q.get("options"):
                for opt in q["options"]:
                    story.append(Paragraph(f"({opt['label']}) {opt['text']}", styles["option_text"]))

            # Answer space for non-MCQ
            else:
                lines = max(2, q["marks"] * 2)
                for _ in range(lines):
                    story.append(Paragraph("_" * 90, styles["option_text"]))

            story.append(Spacer(1, 8))
            q_number += 1

    doc.build(story)
    logger.info(f"Question paper PDF generated: {filepath}")
    return filepath


def generate_report_pdf(
    report_data: Dict,
    student_name: str,
    subject: str,
    output_filename: str,
) -> str:
    """
    Generate an evaluation report PDF with scores and feedback.
    Returns the file path.
    """
    os.makedirs(settings.PDF_OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(settings.PDF_OUTPUT_DIR, output_filename)
    styles = _make_styles()

    doc = SimpleDocTemplate(
        filepath,
        pagesize=A4,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
    )
    story = []

    # Header
    story.append(Paragraph("BoardAI – Performance Report", styles["report_title"]))
    story.append(Paragraph(f"{student_name} | Class – {subject}", styles["exam_title"]))
    story.append(HRFlowable(width="100%", thickness=2, color=DARK_BLUE, spaceAfter=10))

    # Score summary
    pct = report_data.get("percentage", 0)
    score_color = SUCCESS_GREEN if pct >= 75 else (WARNING_AMBER if pct >= 45 else ERROR_RED)
    styles["score_dynamic"] = ParagraphStyle(
        "score_dynamic", fontName="Helvetica-Bold", fontSize=36,
        textColor=score_color, alignment=TA_CENTER,
    )
    story.append(Paragraph(
        f"{report_data.get('total_score', 0)}/{report_data.get('max_score', 0)}",
        styles["score_dynamic"],
    ))
    story.append(Paragraph(
        f"Grade: {report_data.get('grade', 'N/A')}  |  {pct:.1f}%",
        styles["exam_title"],
    ))
    story.append(Spacer(1, 12))

    # Topic scores table
    topic_scores = report_data.get("topic_scores", [])
    if topic_scores:
        story.append(Paragraph("  Topic-wise Performance", styles["section_header"]))
        story.append(Spacer(1, 4))
        table_data = [["Topic", "Score", "Max", "Percentage", "Status"]]
        for ts in topic_scores:
            pct_t = ts.get("percentage", 0)
            status = "Good" if pct_t >= 70 else ("Average" if pct_t >= 40 else "Needs Work")
            table_data.append([
                ts.get("topic", ""),
                str(ts.get("score", 0)),
                str(ts.get("max_score", 0)),
                f"{pct_t:.1f}%",
                status,
            ])
        t = Table(table_data, colWidths=[6 * cm, 2 * cm, 2 * cm, 3 * cm, 3.5 * cm])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), DARK_BLUE),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ("ALIGN", (1, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        story.append(t)
        story.append(Spacer(1, 10))

    # Strengths & Weaknesses
    strengths = report_data.get("strengths", [])
    weaknesses = report_data.get("weaknesses", [])
    if strengths or weaknesses:
        story.append(Paragraph("  Strengths & Areas for Improvement", styles["section_header"]))
        story.append(Spacer(1, 6))
        sw_data = [
            [Paragraph("<b>Strengths</b>", styles["info_label"]),
             Paragraph("<b>Areas for Improvement</b>", styles["info_label"])],
        ]
        max_len = max(len(strengths), len(weaknesses))
        for i in range(max_len):
            s = Paragraph(f"✓ {strengths[i]}", styles["body"]) if i < len(strengths) else Paragraph("", styles["body"])
            w = Paragraph(f"✗ {weaknesses[i]}", styles["body"]) if i < len(weaknesses) else Paragraph("", styles["body"])
            sw_data.append([s, w])
        sw_table = Table(sw_data, colWidths=[8.25 * cm, 8.25 * cm])
        sw_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#d1fae5")),
            ("BACKGROUND", (1, 0), (1, 0), colors.HexColor("#fee2e2")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(sw_table)
        story.append(Spacer(1, 10))

    # Recommendations
    recommendations = report_data.get("recommendations", [])
    if recommendations:
        story.append(Paragraph("  Personalized Recommendations", styles["section_header"]))
        story.append(Spacer(1, 6))
        for i, rec in enumerate(recommendations, 1):
            story.append(Paragraph(f"{i}. {rec}", styles["body"]))
        story.append(Spacer(1, 8))

    # Footer
    story.append(HRFlowable(width="100%", thickness=1, color=MEDIUM_GRAY))
    story.append(Paragraph(
        f"Generated by BoardAI on {datetime.now().strftime('%d %B %Y at %I:%M %p')}",
        styles["instruction"],
    ))

    doc.build(story)
    logger.info(f"Report PDF generated: {filepath}")
    return filepath

"""
Google Gemini integration using the new google-genai SDK.
Model: gemini-2.5-flash
"""
import json
import re
import logging
from typing import Any, Dict, List, Optional

from google import genai

from app.config import settings

logger = logging.getLogger(__name__)

MODEL = "gemini-2.5-flash"


def _client() -> genai.Client:
    return genai.Client(api_key=settings.GEMINI_API_KEY)


def _call(prompt: str) -> str:
    """Make a single-turn text generation call."""
    client = _client()
    response = client.models.generate_content(model=MODEL, contents=prompt)
    return response.text


def _call_vision(prompt: str, image_bytes: bytes, mime_type: str) -> str:
    """Make a vision call with an image."""
    from google.genai import types
    client = _client()
    response = client.models.generate_content(
        model=MODEL,
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
            prompt,
        ],
    )
    return response.text


def _extract_json(text: str) -> Any:
    """Extract JSON from response, stripping markdown code fences."""
    text = text.strip()
    match = re.search(r"```(?:json)?\s*([\s\S]+?)\s*```", text)
    if match:
        text = match.group(1)
    return json.loads(text)


# ── Public API ────────────────────────────────────────────────────────────────

def generate_mock_test(
    class_level: int,
    subject: str,
    weak_topics: List[str],
    strong_topics: List[str],
    total_marks: int,
    rag_context: str,
    paper_structure: Dict,
) -> Dict:
    weak_str = ", ".join(weak_topics) if weak_topics else "None identified"
    strong_str = ", ".join(strong_topics) if strong_topics else "None identified"

    sections_spec = "\n".join(
        f"- {name}: {spec['count']} {spec['type'].replace('_', ' ')} questions "
        f"x {spec['marks_each']} marks each ({spec['description']})"
        for name, spec in paper_structure.items()
    )

    prompt = f"""You are an expert CBSE Class {class_level} {subject} paper setter with 20+ years experience.

Generate a complete mock test paper:

STUDENT PROFILE:
- Weak topics (focus more here): {weak_str}
- Strong topics: {strong_str}

PAPER STRUCTURE ({total_marks} marks total):
{sections_spec}

RELEVANT CBSE CONTENT:
{rag_context if rag_context else f"Use standard CBSE syllabus for Class {class_level}"}

RULES:
1. Follow CBSE 2024-25 exam pattern strictly
2. Difficulty mix: 30% easy, 50% moderate, 20% hard
3. All questions from NCERT Class {class_level} syllabus
4. MCQ options: exactly 4 choices labelled A, B, C, D
5. Provide expected/model answer for every question
6. Every question must have topic and chapter fields
7. Question IDs must be unique strings like q1, q2, q3 ...

Return ONLY valid JSON (no extra text):
{{
  "sections": [
    {{
      "name": "Section A",
      "description": "Multiple Choice Questions",
      "total_marks": 20,
      "questions": [
        {{
          "id": "q1",
          "type": "mcq",
          "question": "Question text?",
          "marks": 1,
          "topic": "Topic name",
          "chapter": "Chapter name",
          "difficulty": "easy",
          "options": [
            {{"label": "A", "text": "Option A"}},
            {{"label": "B", "text": "Option B"}},
            {{"label": "C", "text": "Option C"}},
            {{"label": "D", "text": "Option D"}}
          ],
          "expected_answer": "A",
          "hint": "Brief hint"
        }}
      ]
    }},
    {{
      "name": "Section B",
      "description": "Short Answer Questions",
      "total_marks": 18,
      "questions": [
        {{
          "id": "q21",
          "type": "short_answer",
          "question": "Question text?",
          "marks": 3,
          "topic": "Topic name",
          "chapter": "Chapter name",
          "difficulty": "medium",
          "options": null,
          "expected_answer": "Model answer with key points",
          "hint": "Brief hint"
        }}
      ]
    }}
  ]
}}

Generate all {total_marks} marks worth of questions now:"""

    text = _call(prompt)
    return _extract_json(text)


def analyze_diagnostic_responses(
    class_level: int,
    subject: str,
    responses: Dict[str, Any],
    all_topics: List[str],
) -> Dict:
    prompt = f"""You are a CBSE education expert analysing a student's self-assessment for Class {class_level} {subject}.

Student responses (question_id -> answer):
{json.dumps(responses, indent=2)}

Available topics: {all_topics}

Return ONLY valid JSON:
{{
  "weak_topics": ["topics where student scored 1-2 or low confidence"],
  "strong_topics": ["topics where student scored 4-5"],
  "confidence_score": 3.2,
  "analysis_summary": "2-3 sentence summary"
}}

Rules:
- conf_* questions are rated 1-5
- topic_strength questions are rated 1-5
- past_marks: "Below 33%"=1, "33-50%"=2, "51-60%"=3, "61-75%"=4, "76-90%"=5, "Above 90%"=6
- Only include topics from the provided list
- confidence_score is the overall average (1.0-5.0)"""

    text = _call(prompt)
    return _extract_json(text)


def evaluate_answers(
    class_level: int,
    subject: str,
    questions_with_answers: List[Dict],
) -> Dict:
    qa_text = json.dumps(questions_with_answers, indent=2)

    prompt = f"""You are a strict but fair CBSE examiner evaluating Class {class_level} {subject} answers.

Questions, model answers, and student answers:
{qa_text}

RULES:
1. MCQs: full marks if correct, 0 if wrong (no partial)
2. Short/long answers: award partial marks for partially correct answers
3. Error types: "correct", "conceptual", "calculation", "incomplete", "wrong"
4. Give specific 1-2 sentence feedback per question

Return ONLY valid JSON:
{{
  "question_evaluations": [
    {{
      "question_id": "q1",
      "marks_awarded": 1.0,
      "max_marks": 1,
      "student_answer": "the student answer",
      "feedback": "Specific feedback",
      "error_type": "correct"
    }}
  ],
  "total_score": 45.5,
  "max_score": 80,
  "percentage": 56.9,
  "topic_analysis": {{
    "topic_name": {{"score": 8, "max": 10, "percentage": 80.0}}
  }},
  "strengths": ["3-5 strength statements"],
  "weaknesses": ["3-5 weakness statements"],
  "overall_feedback": "2-3 sentence overall assessment"
}}"""

    text = _call(prompt)
    return _extract_json(text)


def generate_improvement_plan(
    class_level: int,
    subject: str,
    weak_topics: List[str],
    evaluation_data: Dict,
    diagnostic_data: Optional[Dict] = None,
) -> Dict:
    prompt = f"""You are a CBSE expert counsellor creating a personalised improvement plan.

Student: Class {class_level} {subject}
Weak topics: {weak_topics}
Score: {evaluation_data.get('total_score', 0)}/{evaluation_data.get('max_score', 80)} ({evaluation_data.get('percentage', 0):.1f}%)
Weaknesses: {evaluation_data.get('weaknesses', [])}

Return ONLY valid JSON:
{{
  "study_schedule": {{
    "week_1": {{
      "focus": "Topic to focus",
      "daily_hours": 2,
      "activities": ["Activity 1", "Activity 2"],
      "resources": ["NCERT Chapter X"]
    }},
    "week_2": {{"focus": "...", "daily_hours": 2, "activities": [], "resources": []}},
    "week_3": {{"focus": "...", "daily_hours": 2, "activities": [], "resources": []}},
    "week_4": {{"focus": "...", "daily_hours": 2, "activities": [], "resources": []}}
  }},
  "priority_topics": [
    {{
      "topic": "Topic name",
      "priority": "high",
      "suggested_hours": 8,
      "ncert_chapters": ["Chapter name"],
      "key_concepts": ["Concept 1", "Concept 2"]
    }}
  ],
  "practice_recommendations": ["Recommendation 1", "Recommendation 2"],
  "expected_improvement": "Expected outcome statement"
}}"""

    text = _call(prompt)
    return _extract_json(text)


def extract_text_from_image(image_bytes: bytes, mime_type: str = "image/jpeg") -> str:
    prompt = """Extract all text from this scanned answer sheet.
Organise by question number where visible.
Preserve mathematical expressions as best as possible.
Format: Q1: [answer text]  Q2: [answer text]  etc.
Return only the extracted text."""

    return _call_vision(prompt, image_bytes, mime_type)

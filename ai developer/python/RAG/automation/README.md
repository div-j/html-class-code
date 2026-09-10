# Automation Workflow Report: StudyPulse AI Study Plan Generator

## 1. Workflow Design
`New Google Sheets Row (Trigger)` ──> `HTTP Webhook Request (Action)` ──> `POST /study-plan (AI Processing)` ──> `Send Email / Update Sheet (Delivery Result)`

---

## 2. Field Mapping & Payload Schema

### Input Trigger Fields (Google Sheets)
* `student_email`: Email address of the student/teacher.
* `topic`: Topic or subject title.
* `lesson_note`: Raw text notes or syllabus outline.
* `difficulty`: Selected difficulty level (`easy`, `medium`, `hard`).

### JSON Request Payload sent to `POST /study-plan`
```json
{
  "student_email": "student@example.com",
  "topic": "Photosynthesis and Plant Cellular Respiration",
  "lesson_note": "Plants transform light energy into chemical energy using chlorophyll in chloroplasts...",
  "difficulty": "medium"
}
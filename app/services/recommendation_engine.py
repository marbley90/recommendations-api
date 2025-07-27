from app.models.schemas import PatientData

def generate_recommendation(data: PatientData) -> str:
    if data.age > 65 and data.has_chronic_pain:
        return "Physical Therapy"
    if data.bmi > 30:
        return "Weight Management Program"
    if data.had_recent_surgery:
        return "Post-Op Rehabilitation Plan"
    return "General Wellness Check"

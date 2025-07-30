from app.models.schemas import PatientData
from app.services.recommendation_engine import generate_recommendation

def test_physical_therapy():
    data = PatientData(age=70, has_chronic_pain=True, bmi=25, had_recent_surgery=False)
    assert generate_recommendation(data) == "Physical Therapy"

def test_weight_management():
    data = PatientData(age=40, has_chronic_pain=False, bmi=32, had_recent_surgery=False)
    assert generate_recommendation(data) == "Weight Management Program"

def test_post_op_rehab():
    data = PatientData(age=50, has_chronic_pain=False, bmi=25, had_recent_surgery=True)
    assert generate_recommendation(data) == "Post-Op Rehabilitation Plan"

def test_general_wellness():
    data = PatientData(age=30, has_chronic_pain=False, bmi=23, had_recent_surgery=False)
    assert generate_recommendation(data) == "General Wellness Check"

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import json
import re
from mangum import Mangum  # Vercel-compatible handler

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# ----- Predefined functions -----
def get_ticket_status(ticket_id: int):
    return {"ticket_id": ticket_id}

def schedule_meeting(date: str, time: str, meeting_room: str):
    return {"date": date, "time": time, "meeting_room": meeting_room}

def get_expense_balance(employee_id: int):
    return {"employee_id": employee_id}

def calculate_performance_bonus(employee_id: int, current_year: int):
    return {"employee_id": employee_id, "current_year": current_year}

def report_office_issue(issue_code: int, department: str):
    return {"issue_code": issue_code, "department": department}

# ----- Endpoint -----
@app.get("/execute")
def execute(q: str = Query(...)):
    q_lower = q.lower()
    
    if "status of ticket" in q_lower:
        ticket_id = int(re.search(r"ticket (\d+)", q_lower).group(1))
        return {"name": "get_ticket_status", "arguments": json.dumps({"ticket_id": ticket_id})}
    
    elif "schedule a meeting" in q_lower:
        date = re.search(r"on (\d{4}-\d{2}-\d{2})", q_lower).group(1)
        time = re.search(r"at (\d{2}:\d{2})", q_lower).group(1)
        room = re.search(r"in (.+?)\.", q).group(1)
        return {"name": "schedule_meeting", "arguments": json.dumps({"date": date, "time": time, "meeting_room": room})}
    
    elif "expense balance" in q_lower:
        employee_id = int(re.search(r"employee (\d+)", q_lower).group(1))
        return {"name": "get_expense_balance", "arguments": json.dumps({"employee_id": employee_id})}
    
    elif "performance bonus" in q_lower:
        employee_id = int(re.search(r"employee (\d+)", q_lower).group(1))
        year = int(re.search(r"for (\d{4})", q_lower).group(1))
        return {"name": "calculate_performance_bonus", "arguments": json.dumps({"employee_id": employee_id, "current_year": year})}
    
    elif "report office issue" in q_lower:
        issue_code = int(re.search(r"issue (\d+)", q_lower).group(1))
        department = re.search(r"for the (.+?) department", q).group(1)
        return {"name": "report_office_issue", "arguments": json.dumps({"issue_code": issue_code, "department": department})}
    
    else:
        return {"error": "Query not recognized"}

# ----- Vercel handler -----
handler = Mangum(app)

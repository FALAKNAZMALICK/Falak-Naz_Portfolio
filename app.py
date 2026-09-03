import os
import json
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, send_from_directory
import urllib.request
import urllib.error

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent

PORTFOLIO = {
    "name": "Falak Naz",
    "headline":  " Data Scientist/Machine Learning Engineering Intern · Computer Science Undergraduate",
    "roles": ["Data Scientist", "Data Analyst", "Machine Learning Engineer", "AI / ML Enthusiast"],
    "location": "Karachi, Pakistan",
    "email": "itsfalaknaz@gmail.com",
    "phone": "+92-310-2909433",
    "github": "https://github.com/FALAKNAZMALICK",
    "linkedin": "https://www.linkedin.com/in/falaknaz-/",
    "leetcode": "https://leetcode.com/u/Falak_Naz/",
    "resume_file": "resume/Falak_Naz_Resume.pdf",
    "photo_file": "images/profile.jpg",
    "summary": (
        "Machine Learning Engineering Intern and Computer Science undergraduate at NED University of Engineering "
        "and Technology Specialization in data science, focused on ML, AI, and Data Science. I enjoy turning datasets into useful insights, "
        "visualizations, models, and practical AI products."
    ),
    "stats": [
        {"value": "15+", "label": "Projects"},
        {"value": "4", "label": "Internships & Simulations"},
        {"value": "20+", "label": "Certifications"},
    ],
    "skills": {
        "Data Science": ["Python", "Pandas", "NumPy", "Statistics", "EDA", "Data Analysis", "Data Visualization", "SQL", "Tableau", "Excel"],
        "ML & AI": ["Machine Learning", "Model Training", "Predictive Analytics", "Feature Engineering", "Google Gemini API", "AI Applications"],
        "CS/Programming": ["C", "C++", "Java", "JavaScript", "Next.js", "React", "Tailwind CSS", "Git/GitHub", "DBMS", "OOP"],
    },
    "experience": [
        {"role":"ML Engineering Intern", "org":"FlyRank (AI Internship Program)", "period":"June 2026 – Present", "points":["Applying Python and machine learning fundamentals to organic-growth and content/SEO tooling."]},
        {"role":"Data Science & Analytics Intern", "org":"DevelopersHub Corporation", "period":"April 2026 – June 2026", "points":["Used Python and statistical data analysis on real-world datasets to uncover trends and translate findings into business-facing recommendations.", "Performed model training and data visualization as part of the analytics workflow."]},
        {"role":"Data Analytics Job Simulation", "org":"Deloitte Australia (via Forage)", "period":"April 2026", "points":["Worked with structured datasets in a forensic-technology and data-analysis simulation.", "Built a Tableau dashboard and used Excel to classify data and support conclusions."]},
        {"role":"Software Engineering Virtual Experience", "org":"Electronic Arts (via Forage)", "period":"March 2026", "points":["Proposed a feature for EA Sports College Football and prepared the feature proposal.", "Designed a class diagram, implemented a C++ header, patched a bug, and improved a data structure."]},
    ],
    "projects": [
        {"name":"Auralis AI", "role":"AI Learning Workspace · Personal project", "period":"July 2026", "description":"A working AI-powered learning platform with AI chat, Study Mesh, student profiles, dashboard, leaderboard, and responsive UI.", "tags":["Next.js","React","Tailwind","Clerk","Gemini API"], "link":"https://github.com/FALAKNAZMALICK/Auralis-AI"},
        {"name":"Emergency Resource Management System", "role":"Team lead · Academic project", "period":"May 2026", "description":"SQL-based system for tracking critical supplies and coordinating personnel during disaster-response scenarios, with schema design and real-time queries.", "tags":["SQL","DBMS","Schema Design"], "link":"https://github.com/FALAKNAZMALICK/EMERGENCY-RESOURCE-MANAGEMENT-SYSTEM----DBMS_PROJECT"},
        {"name":"Math Clash", "role":"Team lead · Academic project", "period":"November 2025", "description":"Competitive math game applying data structures and algorithms, with authentication, scoring, progress tracking, and leaderboard features.", "tags":["C++","DSA","Authentication"], "link":"https://github.com/FALAKNAZMALICK/MATH-CLASH-game"},
        {"name":"Health Recommendation System", "role":"Co-lead · Academic project", "period":"May 2025", "description":"Modular C++ OOP system for personalized diet and exercise recommendations, with authentication, input validation, and a recommendation engine.", "tags":["C++","OOP","System Design"], "link":"https://github.com/FALAKNAZMALICK/Project-HEALTH-RECOMMENDATIION-SYSTEM"},
    ],
    "education":[
        {"degree":"Bachelor of Computer Science & Information Technology", "school":"NED University of Engineering and Technology, Karachi", "period":"Aug 2024 – Aug 2028"},
        {"degree":"Intermediate", "school":"Saint Lawrence Government Girls Degree College, Karachi", "period":"Mar 2021 – Jun 2023"},
    ],
    "certifications":["Python for Data Science — IBM SkillsBuild","Structured Query Language — Coursera","Artificial Intelligence Course — AI Institute of Pakistan","Intro to Programming — Kaggle","Google AI — Coursera","Web Developer — BanoQabil",".....","explore more on my linkdin"],
    "leadership":[{"role":"Graphic Designer & Marketing Lead", "org":"NSA Society, NED University", "period":"2024 – 2026", "points":["Designed visuals and promotional material, led marketing and social-media promotions, supervised 3 volunteers, and prepared semester-wise performance reports."]}],
    "awards":["Jauhar merit-based academic scholarship — NED University of Engineering and Technology (2024–2026)","Merit-based Laptop Award — Prime Minister's Youth Laptop Scheme (2024–2026)"],
    "languages":["English", "Urdu"]
}

SYSTEM_PROMPT = """You are the official portfolio assistant for Falak Naz. Answer visitors who ask about Falak's background, skills, experience, education, projects, certifications, leadership, awards, or contact details. Use ONLY the portfolio facts provided below. Never invent employers, metrics, technologies, achievements, dates, responsibilities, or links. If something is not in the profile, say that it is not listed and suggest asking about a listed area. Keep answers concise, polished, friendly, and suitable for a recruiter or professional visitor. Speak in the user's language when obvious.\n\nPROFILE:\n""" + json.dumps(PORTFOLIO, ensure_ascii=False)

@app.route("/")
def home():
    return render_template("index.html", data=PORTFOLIO)

@app.route("/api/gemini", methods=["POST"])
def gemini():
    key = os.getenv("GEMINI_API_KEY", "").strip()
    payload = request.get_json(silent=True) or {}
    message = str(payload.get("message", "")).strip()
    
    if not message:
        return jsonify({"ok": False, "reply": "Ask me anything about Falak's skills, projects, experience, education, or background."}), 400
    if not key:
        return jsonify({"ok": False, "reply": "The Gemini assistant is configured in the portfolio, but GEMINI_API_KEY has not been added to the server environment yet."}), 503

    model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
    body = json.dumps({
        "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "contents": [{"role": "user", "parts": [{"text": message}]}],
        "generationConfig": {"temperature": 0.25, "maxOutputTokens": 450}
    }).encode("utf-8")
    
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            result = json.loads(response.read().decode("utf-8"))
        parts = result.get("candidates", [{}])[0].get("content", {}).get("parts", [])
        reply = "".join(p.get("text", "") for p in parts).strip()
        if not reply:
            raise ValueError("Empty Gemini response")
        return jsonify({"ok": True, "reply": reply})
    except urllib.error.HTTPError as exc:
        return jsonify({"ok": False, "reply": f"Gemini is temporarily unavailable. Please check the server API configuration. ({exc.code})"}), 502
    except Exception:
        return jsonify({"ok": False, "reply": "Gemini could not respond right now. Please try again in a moment."}), 502

@app.route('/resume/<path:filename>')
def resume(filename):
    return send_from_directory(BASE_DIR / 'static' / 'resume', filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
# Falak Naz — Dark AI Portfolio

A custom, responsive Flask portfolio with a black/graphite visual system, centered profile portrait, project/experience sections, and a Gemini-powered portfolio chatbot.

## What's included
- Premium black dark theme with lime accent
- Smaller centered profile portrait using `static/images/profile.jpg`
- Clear spacing and divider lines between every major section
- Data Science / Data Analytics / ML focused content based on the supplied résumé
- Résumé download at `/resume/Falak_Naz_Resume.pdf`
- Gemini chatbot: visitors can ask about Falak's experience, projects, skills, education, certifications, etc.
- Responsive mobile navigation and scroll-reveal animation
- Render/Gunicorn-ready deployment files

## Run locally

```bash
python -m venv venv
# Windows
venv\\Scripts\\activate
# macOS/Linux
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`.

## Enable Gemini

Create a Gemini API key and set it only on the server:

```bash
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.5-flash
```

For Render, add these as Environment Variables. **Do not put the API key in HTML or JavaScript.** The Flask `/api/gemini` route keeps the secret server-side and sends only the visitor's question to Gemini together with the portfolio facts.

If the key is missing, the chatbot displays a clear configuration message instead of exposing or inventing credentials.

## Deployment

Build command:

```bash
pip install -r requirements.txt
```

Start command:

```bash
gunicorn app:app
```

## Personalization

Portfolio content is kept in `app.py` inside `PORTFOLIO`. Replace the profile photo with another `static/images/profile.jpg` if desired, and replace the résumé at `static/resume/Falak_Naz_Resume.pdf` when you have a newer version.
# FALAK-NAZ_PORTFOLIO

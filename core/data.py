"""Site content and fallback GitHub contribution data."""

CONTRIBUTION_TOTAL = 1248

# Fallback pattern used only when live GitHub data cannot be fetched.
DESKTOP_CONTRIBUTION_GRID = [
    [0, 3, 2, 1, 1, 0, 3],
    [0, 0, 3, 2, 1, 1, 0],
    [1, 0, 0, 3, 2, 1, 1],
    [2, 1, 0, 0, 3, 2, 1],
    [2, 2, 1, 0, 0, 3, 2],
    [2, 2, 1, 0, 0, 3, 2],
    [3, 2, 2, 1, 0, 0, 3],
    [0, 3, 2, 2, 1, 0, 0],
    [1, 0, 3, 2, 2, 1, 0],
    [1, 1, 0, 3, 2, 2, 1],
    [1, 1, 0, 3, 2, 2, 1],
    [2, 1, 1, 0, 3, 2, 2],
    [3, 2, 1, 1, 0, 3, 2],
    [0, 3, 2, 1, 1, 0, 3],
    [0, 0, 3, 2, 1, 1, 0],
    [1, 0, 0, 3, 2, 1, 1],
    [2, 1, 0, 0, 3, 2, 1],
    [2, 2, 1, 0, 0, 3, 2],
    [3, 2, 2, 1, 0, 0, 3],
    [3, 2, 2, 1, 0, 0, 3],
    [3, 2, 2, 1, 0, 0, 3],
    [0, 3, 2, 2, 1, 0, 0],
    [1, 0, 3, 2, 2, 1, 0],
    [1, 1, 0, 3, 2, 2, 1],
    [2, 1, 1, 0, 3, 2, 2],
    [2, 1, 1, 0, 3, 2, 2],
    [3, 2, 1, 1, 0, 3, 2],
    [0, 3, 2, 1, 1, 0, 3],
    [0, 0, 3, 2, 1, 1, 0],
    [1, 0, 0, 3, 2, 1, 1],
    [2, 1, 0, 0, 3, 2, 1],
    [2, 2, 1, 0, 0, 3, 2],
    [2, 2, 1, 0, 0, 3, 2],
    [3, 2, 2, 1, 0, 0, 3],
    [0, 3, 2, 2, 1, 0, 0],
    [1, 0, 3, 2, 2, 1, 0],
    [1, 1, 0, 3, 2, 2, 1],
    [1, 1, 0, 3, 2, 2, 1],
    [2, 1, 1, 0, 3, 2, 2],
    [3, 2, 1, 1, 0, 3, 2],
    [0, 3, 2, 1, 1, 0, 3],
    [0, 0, 3, 2, 1, 1, 0],
    [1, 0, 0, 3, 2, 1, 1],
    [2, 1, 0, 0, 3, 2, 1],
    [2, 2, 1, 0, 0, 3, 2],
    [2, 2, 1, 0, 0, 3, 2],
    [3, 2, 2, 1, 0, 0, 3],
    [0, 3, 2, 2, 1, 0, 0],
    [1, 0, 3, 2, 2, 1, 0],
    [1, 1, 0, 3, 2, 2, 1],
    [2, 1, 1, 0, 3, 2, 2],
    [3, 2, 1, 1, 0, 3, 2],
]

MOBILE_CONTRIBUTION_GRID = DESKTOP_CONTRIBUTION_GRID[:26]

EXPERIENCE = [
    {
        "period": "Oct 2024 — Present",
        "period_mobile": "Present · Movylab SAS",
        "title": "Software Engineer",
        "company": "Movylab SAS",
        "description": (
            "Django platform for medical rehabilitation appointments and computerized "
            "gait analysis, with Google Calendar integration and Docker deployment."
        ),
        "description_mobile": "Django rehab platform · gait analysis · Docker",
        "tags": ["Django", "PostgreSQL", "Docker"],
        "mobile_visible": True,
    },
    {
        "period": "Feb 2022 — Jul 2024",
        "period_mobile": "2022–2024 · IDEMIA",
        "title": "Junior Software Engineer",
        "company": "IDEMIA",
        "description": (
            "Backend maintenance for Chile’s national identity management system: "
            "PL/SQL automation over 10M+ records, gender-X document support, and "
            "citizen email dispatch."
        ),
        "description_mobile": "Chile national identity systems · PL/SQL · Spring",
        "tags": ["Java", "Spring", "PL/SQL"],
        "mobile_visible": True,
    },
    {
        "period": "Aug 2023 — Dec 2023",
        "period_mobile": "2023 · Aprendizaje Profundo",
        "title": "Front-end Developer",
        "company": "Aprendizaje Profundo",
        "description": (
            "Angular platform for Colombia’s National Registry to report election-related "
            "issues, scaled for 500+ concurrent transactions."
        ),
        "description_mobile": "Angular election-reporting platform",
        "tags": ["Angular"],
        "mobile_visible": True,
    },
    {
        "period": "Jul 2021 — Feb 2022",
        "period_mobile": "2021–2022 · IDEMIA",
        "title": "Software Engineering Intern",
        "company": "IDEMIA",
        "description": (
            "Tuned facial recognition parameters for Colombia’s national registry using "
            "ICAO portrait-quality libraries in Spring Boot."
        ),
        "description_mobile": "Facial recognition · Spring Boot · ICAO",
        "tags": ["Spring Boot", "Computer Vision"],
        "mobile_visible": False,
    },
]

STUDIES = [
    {
        "period": "Present",
        "period_mobile": "Present · Politecnico di Torino",
        "title": "Politecnico di Torino — MSc Computer Engineering",
        "title_mobile": "MSc Computer Engineering",
        "description": (
            "Automation and Cyber-physical Systems. Research focus on brain–computer "
            "interfaces for rehabilitation."
        ),
        "tags": ["COLFUTURO Scholarship"],
        "tags_mobile": ["COLFUTURO"],
        "mobile_visible": True,
    },
    {
        "period": "2024",
        "period_mobile": "2024 · World Campus Japan",
        "title": "World Campus Japan · Global Education Program",
        "title_mobile": "Global Education Program",
        "description": (
            "Cross-cultural leadership and immersive community collaboration in Japan."
        ),
        "tags": [],
        "tags_mobile": [],
        "mobile_visible": False,
    },
    {
        "period": "2023",
        "period_mobile": "2023 · Universidad Nacional",
        "title": "Universidad Nacional de Colombia — Data Science Diploma",
        "title_mobile": "Data Science Diploma",
        "description": (
            "Machine learning, big data, and predictive analytics coursework."
        ),
        "tags": [],
        "tags_mobile": [],
        "mobile_visible": False,
    },
    {
        "period": "2018–2023",
        "period_mobile": "2018–2023 · Universidad Central",
        "title": "Universidad Central — Systems Engineering",
        "title_mobile": "Systems Engineering",
        "description": (
            "Graduated with Meritorious Mention. Thesis on information security in J24."
        ),
        "tags": ["Meritorious Mention"],
        "tags_mobile": ["Meritorious Mention"],
        "mobile_visible": True,
    },
    {
        "period": "Leadership",
        "period_mobile": "Leadership · PoliTOrbital",
        "title": "PoliTOrbital · SKTracks-Capture",
        "title_mobile": "SKTracks-Capture medical aspects",
        "description": (
            "Medical aspects member supporting computer-vision rehab capture for SKTracks."
        ),
        "tags": ["Recognition"],
        "tags_mobile": [],
        "mobile_visible": True,
    },
]

NORT = {
    "title": "NORT",
    "description": (
        "Non-invasive neural decoding for rehabilitation — EEG software backbone and a "
        "temple/behind-ear wearable prototype."
    ),
    "description_mobile": "Non-invasive neural decoding for rehabilitation.",
    "tags": ["BCI", "EEG + sEMG", "Wearable"],
    "url": "#nort",
}

CONTACT = {
    "email": "esteban.cubi1@gmail.com",
    "github": "https://github.com/JuanPuyo1",
    "github_label": "github.com/JuanPuyo1",
    "linkedin": "https://linkedin.com/in/juanpuyo",
    "linkedin_label": "linkedin.com/in/juanpuyo",
}

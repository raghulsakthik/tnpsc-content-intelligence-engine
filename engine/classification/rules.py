"""Conservative keyword rules used by the Phase 6 baseline classifier.

Rules are intentionally explicit. They are a deterministic baseline, not an
LLM or semantic classifier. New aliases should be reviewed and tested before
being added.
"""

SUBJECT_RULES: dict[str, tuple[str, ...]] = {
    "general-studies": (
        "general studies", "பொது அறிவு", "general science", "science",
        "geography", "history", "polity", "economy", "environment",
        "இந்திய அரசியல்", "இந்திய பொருளாதாரம்", "புவியியல்", "வரலாறு",
    ),
    "aptitude-mental-ability": (
        "aptitude", "mental ability", "reasoning", "quantitative aptitude",
        "அளவியல்", "மனத்திறன்", "கணித", "reasoning ability",
    ),
    "general-tamil": ("general tamil", "பொது தமிழ்", "தமிழ் இலக்கணம்", "tamil grammar"),
    "general-english": ("general english", "பொது ஆங்கிலம்", "english grammar"),
    "thirukkural": ("thirukkural", "thirukural", "திருக்குறள்", "kural"),
    "current-affairs": (
        "current affairs", "daily current affairs", "current events",
        "நடப்பு நிகழ்வுகள்", "நடப்பு நிகழ்ச்சிகள்", "today's current affairs",
    ),
}

UNIT_RULES: dict[str, tuple[str, ...]] = {
    "science": ("general science", "science", "அறிவியல்", "physics", "chemistry", "biology", "botany", "zoology"),
    "geography": ("geography", "புவியியல்", "physical geography", "indian geography"),
    "history-culture": ("history and culture", "history & culture", "வரலாறும் பண்பாடும்", "ancient india", "medieval india"),
    "indian-national-movement": ("national movement", "freedom movement", "indian national movement", "தேசிய இயக்கம்"),
    "indian-polity": ("indian polity", "constitution", "அரசியலமைப்பு", "இந்திய அரசியல்"),
    "indian-economy": ("indian economy", "economy", "பொருளாதாரம்"),
    "tn-development-administration": ("development administration", "tamil nadu development", "தமிழ்நாடு வளர்ச்சி நிர்வாகம்"),
    "tn-history-culture-heritage": ("tamil nadu history", "tn history", "heritage", "தமிழ்நாடு வரலாறு", "தமிழர் பண்பாடு"),
    "science-technology": ("science and technology", "science & technology", "அறிவியல் மற்றும் தொழில்நுட்பம்", "technology"),
    "socio-economic-issues": ("socio economic", "socio-economic", "social issues", "சமூக பொருளாதார"),
    "environment": ("environment", "ecology", "சுற்றுச்சூழல்", "biodiversity"),
}

PYQ_RULES = (
    "previous year question", "previous years questions", "previous year questions",
    "pyq", "pyqs", "past question paper", "question paper", "question papers",
    "முந்தைய ஆண்டு வினாத்தாள்", "முந்தைய ஆண்டு கேள்விகள்", "வினாத்தாள்",
)

MOCK_RULES = (
    "mock test", "grand mock", "practice test", "model test", "online test",
    "free mock", "மாதிரி தேர்வு", "பயிற்சி தேர்வு", "மாதிரி வினாத்தாள்",
)

CURRENT_AFFAIRS_RULES = (
    "current affairs", "current events", "daily current affairs", "today's news",
    "monthly current affairs", "நடப்பு நிகழ்வுகள்", "நடப்பு நிகழ்ச்சிகள்",
)

GOVERNMENT_RULES = (
    "government of tamil nadu", "govt. of tamil nadu", "government of tamilnadu",
    "tamil nadu government", "tn government", "official government", "government portal",
    "தமிழ்நாடு அரசு", "தமிழக அரசு", "அரசு வெளியீடு", "அரசு இணையதளம்",
)

LANGUAGE_RULES: dict[str, tuple[str, ...]] = {
    "ta": ("தமிழ்", "தமிழ்நாடு", "திருக்குறள்", "பொது தமிழ்", "அரசியலமைப்பு"),
    "en": ("the", "and", "general", "tnpsc", "government"),
}

"""YouTube metadata file (TYTUŁ / OPIS / TAGI) in the format upload_youtube.py parses."""

from odczyt.episode import Episode

TITLE_SUFFIX = " | Deep Dive"
TITLE_MAX = 100
SUGGEST_URL = "https://github.com/Automaat/youtube-whitepapers/issues"
MIN_CHAPTER_SECONDS = 10


def clock(seconds: float) -> str:
    total = int(seconds)
    h, rest = divmod(total, 3600)
    m, s = divmod(rest, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def chapter_marks(timeline: dict) -> list[tuple[float, str]]:
    """YouTube chapters: 0:00 intro, then each chapter's first scene, ≥10 s apart."""
    titles = {c["id"]: c["title"] for c in timeline["chapters"]}
    marks: list[tuple[float, str]] = [(0.0, "Wstęp")]
    seen: set[str] = set()
    for scene in timeline["scenes"]:
        chapter = scene.get("chapter")
        if chapter is None or chapter in seen:
            continue
        seen.add(chapter)
        if scene["start"] - marks[-1][0] >= MIN_CHAPTER_SECONDS:
            marks.append((scene["start"], titles[chapter]))
    return marks


def format_metadata(ep: Episode, data: dict, timeline: dict) -> str:
    """Render the metadata text file from the LLM's structured output and the timeline."""
    title = data["title"].strip()
    if not title.endswith(TITLE_SUFFIX):
        title += TITLE_SUFFIX
    if len(title) > TITLE_MAX:
        raise ValueError(f"Title longer than {TITLE_MAX} characters: {title}")
    tags = " ".join("#" + t.lstrip("#").replace(" ", "") for t in data["tags"])
    lines = [
        "TYTUŁ:",
        title,
        "",
        "OPIS:",
        data["intro"].strip(),
        "",
        "W tym odcinku omawiamy:",
        *[f"• {t}" for t in data["topics"]],
        "",
        "Rozdziały:",
        *[f"{clock(t)} {name}" for t, name in chapter_marks(timeline)],
        "",
        f"📄 Oryginalny artykuł: {ep.config['paper_url']}",
        "",
        f"Autorzy: {ep.config['authors']}",
        f"Publikacja: {data['publication'].strip()}",
        "",
        f"💡 Masz propozycję artykułu? Zgłoś: {SUGGEST_URL}",
        "",
        "TAGI:",
        tags,
    ]
    return "\n".join(lines) + "\n"

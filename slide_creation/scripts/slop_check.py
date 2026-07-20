import argparse
import re
import sys
from collections import defaultdict

try:
    from markitdown import MarkItDown
except ImportError:
    print("ERROR: markitdown not installed.", file=sys.stderr)
    sys.exit(2)

#configs
BANNED_PHRASES = [
    r"fast[\s-]?paced world",
    r"unlock the power",
    r"seamless(ly)?",
    r"robust solution",
    r"cutting[\s-]?edge",
    r"in today'?s",
    r"let'?s dive in",
    r"dive into",
    r"game[\s-]?changer",
    r"at the end of the day",
    r"synerg(y|ies|istic)",
    r"\bleverage\b",        
    r"paradigm shift",
    r"take .* to the next level",
    r"holistic approach",
    r"best[\s-]?in[\s-]?class",
    r"world[\s-]?class",
    r"empower(ing|ed|s)?",
    r"revolutioniz(e|ing|ed)",
    r"transformative",
    r"innovative solutions?",
]

ABSTRACT_BUZZWORDS = {
    "strategy", "growth", "value", "innovation", "excellence", "solutions",
    "synergy", "efficiency", "optimization", "transformation", "impact",
    "engagement", "alignment", "vision", "mission", "empowerment",
}

CONTENT_FREE_TITLES = {
    "thank you", "thanks", "questions", "questions?", "q&a", "the end",
}

NUMBER_PATTERN = re.compile(
    r"(\$[\d,]+(\.\d+)?[kmb]?\b|\b\d{1,3}(,\d{3})*(\.\d+)?%?\b)", re.IGNORECASE
)



#slide extraction
def extract_slides(pptx_path):
    md = MarkItDown()
    result = md.convert(pptx_path)
    text = result.text_content

    parts = re.split(r"<!--\s*Slide number:\s*(\d+)\s*-->", text)
    slides = {}
    for i in range(1, len(parts), 2):
        num = int(parts[i])
        content = parts[i + 1].strip() if i + 1 < len(parts) else ""
        slides[num] = content
    return dict(sorted(slides.items()))


# banned phrases checking
def check_banned_phrases(slides):
    findings = []
    pattern = re.compile("|".join(BANNED_PHRASES), re.IGNORECASE)
    for num, text in slides.items():
        for m in pattern.finditer(text):
            findings.append({
                "slide": num,
                "check": "banned_phrase",
                "detail": f"found phrase matching /{m.group(0)}/",
                "severity": "high",
            })
    return findings


NOISE_LINES = {"### notes:", "notes:"}

def _real_lines(text):
    raw = [l.strip() for l in text.splitlines() if l.strip()]
    return [l for l in raw if l.lower() not in NOISE_LINES]


def check_content_free_slides(slides):
    findings = []
    for num, text in slides.items():
        lines = _real_lines(text)
        if not lines:
            findings.append({
                "slide": num, "check": "empty_slide",
                "detail": "slide has no extractable text at all",
                "severity": "high",
            })
            continue
        title = lines[0].lower().strip("*#: ")
        body_lines = lines[1:]
        if title in CONTENT_FREE_TITLES and not body_lines:
            findings.append({
                "slide": num, "check": "content_free_slide",
                "detail": f"title-only slide ('{lines[0]}') with no next step or content",
                "severity": "medium",
            })
    return findings


def check_numeric_claims(slides):
    findings = []
    for num, text in slides.items():
        for m in NUMBER_PATTERN.finditer(text):
            token = m.group(0)
            if len(token) <= 1:
                continue
            findings.append({
                "slide": num, "check": "numeric_claim_needs_source_check",
                "detail": f"contains '{token}' — confirm this traces to user's source material",
                "severity": "info",
            })
    return findings


def check_specificity_ratio(slides):
    findings = []
    for num, text in slides.items():
        lines = _real_lines(text)
        if not lines:
            continue
        body = "\n".join(lines[1:])
        words = re.findall(r"[a-zA-Z]+", body.lower())
        if not words:
            continue
        buzz_count = sum(1 for w in words if w in ABSTRACT_BUZZWORDS)
        has_number = bool(NUMBER_PATTERN.search(body))
        has_proper_noun = bool(re.search(r"(?<!^)(?<![.!?]\s)\b[A-Z][a-z]{2,}\b", body))
        if buzz_count >= 2 and not has_number and not has_proper_noun:
            findings.append({
                "slide": num, "check": "low_specificity",
                "detail": f"{buzz_count} abstract buzzwords, no number or named entity anchoring the claim",
                "severity": "medium",
            })
    return findings


def check_repeated_openings(slides):
    findings = []
    openings = defaultdict(list)
    for num, text in slides.items():
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        if not lines:
            continue
        title_words = re.findall(r"[a-zA-Z]+", lines[0].lower())[:3]
        if len(title_words) < 2:
            continue
        key = " ".join(title_words)
        openings[key].append(num)
    for key, nums in openings.items():
        if len(nums) > 1:
            findings.append({
                "slide": ",".join(map(str, nums)), "check": "repeated_title_structure",
                "detail": f"slides {nums} all open titles with '{key}...' — vary structure",
                "severity": "low",
            })
    return findings



# reporing 
SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2, "info": 3}

def run(pptx_path, strict=False):
    slides = extract_slides(pptx_path)
    if not slides:
        print("Could not extract any slides — check the file path/format.", file=sys.stderr)
        return 2

    all_findings = []
    all_findings += check_banned_phrases(slides)
    all_findings += check_content_free_slides(slides)
    all_findings += check_numeric_claims(slides)
    all_findings += check_specificity_ratio(slides)
    all_findings += check_repeated_openings(slides)

    all_findings.sort(key=lambda f: (SEVERITY_ORDER.get(f["severity"], 9), str(f["slide"])))

    if not all_findings:
        print(f"no slop findings across {len(slides)} slides.")
        return 0

    print(f"{pptx_path}: {len(all_findings)} findings across {len(slides)} slides\n")
    for f in all_findings:
        print(f"  [{f['severity'].upper():6}] slide {f['slide']:>3}  {f['check']:30} {f['detail']}")

    high_or_med = [f for f in all_findings if f["severity"] in ("high", "medium")]
    print()
    if high_or_med:
        print(f"→ {len(high_or_med)} high/medium findings must be fixed before delivery.")
    else:
        print("→ Only low/info findings — review at your discretion.")

    if strict:
        return 1 if all_findings else 0
    return 1 if high_or_med else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Slop detection for a powerpoint presentation")
    parser.add_argument("pptx", help="Path to powerpoint file")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on ANY finding, including low/info")
    args = parser.parse_args()
    sys.exit(run(args.pptx, strict=args.strict))
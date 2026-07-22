"""
Each test loads one fixture from tests/fixtures/ built to trip exactly one
check in scripts/slop_check.py, and asserts that check fires. clean.pptx is
the shared negative case: it should never trip any of the checks below.

Run: pytest tests/
Regenerate fixtures: python tests/fixtures/generate_fixtures.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import pytest
import slop_check as sc

FIXTURES = Path(__file__).resolve().parent / "fixtures"

BRAND = {
    "type_scale": {"min_title": 24, "min_body": 14},
    "slide_caps": {"default": 10, "internal_update": 6, "client_proposal": 12},
    "footer": {"client_facing_text": "Your Company — Confidential"},
    "logo": {"width_in": 1.4, "min_width_in": 0.9},
}


def load(name):
    return sc.extract(FIXTURES / name)[0]


def checks_for(slides, deck_type="default", client_facing=False, brand=BRAND):
    out = []
    out += sc.check_banned_phrases(slides)
    out += sc.check_content_free_slides(slides)
    out += sc.check_specificity(slides)
    out += sc.check_repeated_openings(slides)
    out += sc.check_voice_rules(slides)
    out += sc.check_slide_cap(slides, brand, deck_type)
    out += sc.check_font_sizes(slides, brand)
    out += sc.check_footer(slides, brand, client_facing)
    out += sc.check_logo(slides, brand)
    return out


def has(findings, check_name):
    return any(f["check"] == check_name for f in findings)


@pytest.fixture(scope="module")
def clean_findings():
    return checks_for(load("clean.pptx"), client_facing=True)


def test_clean_deck_has_no_blocking_findings(clean_findings):
    blocking = [f for f in clean_findings if f["severity"] in sc.BLOCKING]
    assert blocking == [], blocking


@pytest.mark.parametrize("fixture,check_name", [
    ("banned_phrase.pptx", "banned_phrase"),
    ("content_free_slide.pptx", "content_free_slide"),
    ("title_only_slide.pptx", "title_only_slide"),
    ("low_specificity.pptx", "low_specificity"),
    ("repeated_openings.pptx", "repeated_title_structure"),
    ("exclamation_mark.pptx", "exclamation_mark"),
    ("rhetorical_question.pptx", "rhetorical_question_title"),
    ("font_below_minimum.pptx", "font_below_minimum"),
    ("logo_missing.pptx", "logo_missing"),
    ("logo_format.pptx", "logo_format"),
    ("logo_stretched.pptx", "logo_stretched"),
    ("logo_too_small.pptx", "logo_too_small"),
    ("logo_size_off_spec.pptx", "logo_size_off_spec"),
])
def test_fixture_trips_its_check(fixture, check_name, clean_findings):
    findings = checks_for(load(fixture))
    assert has(findings, check_name), f"{fixture} did not trip {check_name}: {findings}"
    assert not has(clean_findings, check_name)


def test_empty_slide():
    findings = checks_for(load("empty_slide.pptx"))
    assert has(findings, "empty_slide")


def test_banned_phrase_in_notes_is_low_severity_not_high():
    findings = checks_for(load("banned_phrase_notes.pptx"))
    hits = [f for f in findings if f["check"] == "banned_phrase"]
    assert hits, "expected a banned_phrase finding from speaker notes"
    assert all(f["severity"] == "low" and f["scope"] == "notes" for f in hits)


def test_slide_cap_exceeded():
    slides = load("slide_cap_exceeded.pptx")
    findings = sc.check_slide_cap(slides, BRAND, "default")
    assert len(slides) == 12
    assert has(findings, "slide_cap_exceeded")


def test_slide_cap_not_exceeded_for_clean_deck():
    slides = load("clean.pptx")
    findings = sc.check_slide_cap(slides, BRAND, "default")
    assert findings == []


def test_font_size_unresolved_is_info_not_blocking():
    slides = load("font_size_unresolved.pptx")
    findings = sc.check_font_sizes(slides, BRAND)
    assert has(findings, "font_size_unresolved")
    assert all(f["severity"] == "info" for f in findings if f["check"] == "font_size_unresolved")


def test_missing_footer_only_checked_when_client_facing():
    slides = load("missing_footer.pptx")
    assert sc.check_footer(slides, BRAND, client_facing=False) == []
    findings = sc.check_footer(slides, BRAND, client_facing=True)
    assert has(findings, "missing_footer")


def test_footer_present_on_clean_deck():
    slides = load("clean.pptx")
    findings = sc.check_footer(slides, BRAND, client_facing=True)
    assert not has(findings, "missing_footer")


def test_numeric_claims_are_info_only():
    slides = load("clean.pptx")
    findings = sc.check_numeric_claims(slides)
    assert findings, "expected numeric claims to be surfaced"
    assert all(f["severity"] == "info" for f in findings)


TEST_BRAND_PATH = str(FIXTURES / "brand.yaml")


def test_run_exits_zero_on_clean_deck():
    code = sc.run(str(FIXTURES / "clean.pptx"), "default", True, TEST_BRAND_PATH, strict=False, as_json=False)
    assert code == 0


def test_run_exits_nonzero_on_blocking_findings():
    code = sc.run(str(FIXTURES / "banned_phrase.pptx"), "default", False, TEST_BRAND_PATH, strict=False, as_json=False)
    assert code == 1


def test_run_exits_2_on_missing_file():
    code = sc.run(str(FIXTURES / "does_not_exist.pptx"), "default", False, TEST_BRAND_PATH, strict=False, as_json=False)
    assert code == 2

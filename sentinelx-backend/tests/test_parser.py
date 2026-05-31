from app.services.parser_service import ParserService


def test_redact_sensitive_text_masks_api_keys():
    # Assembled at runtime so push scanners do not flag a Stripe-shaped test value.
    fake_key = "".join(("sk", "_live_", "abcdefghijklmnopqrstuvwxyz"))
    text = f"Found key {fake_key} in page"
    redacted = ParserService.redact_sensitive_text(text)
    assert "sk_live_" not in redacted
    assert "[REDACTED_API_KEY]" in redacted


def test_redact_sensitive_text_masks_aws_keys():
    text = "AKIAIOSFODNN7EXAMPLE leaked"
    redacted = ParserService.redact_sensitive_text(text)
    assert "AKIA" not in redacted
    assert "[REDACTED_AWS_KEY]" in redacted

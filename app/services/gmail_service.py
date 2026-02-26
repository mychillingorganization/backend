from app.models.generated_asset import GeneratedAssets


class GmailService:
    """Minimal service for sending certificate emails.

    The real implementation would use Google APIs to send a message with an
    attachment/link. For module‑5 purposes we'll simulate success and simply
    return True.
    """

    async def send_generated_asset(self, asset: GeneratedAssets) -> bool:
        # TODO: integrate with Gmail API and build email content + PDF link.
        # For now we assume the send always succeeds.
        # you could add logging or inspect asset fields for debugging.
        return True

"""Centralized UI selectors for NotebookLM.

Selectors need manual discovery via browser DevTools.
Update when UI changes - run `notebooklm-automator test-selectors` to verify.
"""

from __future__ import annotations


class Selectors:
    """UI selectors for NotebookLM automation."""

    # Navigation & Auth - must be specific to logged-in state
    LOGGED_IN_INDICATOR = (
        'button:has-text("Create new"), '  # create button (logged-in only)
        ':text("Recent notebooks"), '  # heading on home page
        ':text("My notebooks")'  # tab on home page
    )
    LOGIN_BUTTON = 'button:has-text("Sign in"), button:has-text("Get started"), a:has-text("Sign in")'

    # Notebook management
    NEW_NOTEBOOK_BTN = (
        'button[aria-label*="Create"], '
        'button[aria-label*="New"], '
        'button:has-text("Create"), '
        'button:has-text("New notebook"), '
        '[data-action="create"]'
    )
    NOTEBOOK_TITLE_INPUT = (
        'input[aria-label*="title"], '
        'input[aria-label*="name"], '
        'input[placeholder*="Untitled"], '
        'input[type="text"]'
    )
    NOTEBOOK_LIST_ITEM = "project-button"

    # Sources panel
    ADD_SOURCE_BTN = (
        'button:has-text("Add source"), '
        'button:has-text("Add"), '
        '[aria-label*="Add source"]'
    )
    SOURCE_URL_OPTION = (
        'button:has-text("Website"), '
        'button:has-text("Link"), '
        'button:has-text("URL"), '
        '[data-action="website"]'
    )
    SOURCE_PDF_OPTION = 'button:has-text("PDF"), [data-action="pdf"]'
    SOURCE_FILE_UPLOAD_OPTION = (
        'button:has-text("Upload"), button:has-text("File"), [data-action="upload"]'
    )
    SOURCE_FILE_INPUT = 'input[type="file"]'
    SOURCE_URL_INPUT = (
        'input[type="url"], '
        'input[type="text"], '
        'input[placeholder*="URL"], '
        'input[placeholder*="http"], '
        'input[placeholder*="paste"]'
    )
    SOURCE_ADD_CONFIRM = (
        'button:has-text("Insert"), '
        'button:has-text("Add"), '
        'button:has-text("Upload"), '
        'button[type="submit"]'
    )
    SOURCE_PROCESSING = '[data-source-status="processing"]'
    SOURCE_READY = '[data-source-status="ready"]'
    SOURCE_LIST_ITEM = "[data-source-id]"

    # Audio Overview (Studio panel)
    AUDIO_OVERVIEW_BTN = (
        ':has-text("Audio Overview") >> nth=0, '
        '[data-test-id="audio-overview"], '
        'div:has-text("Audio Overview")'
    )
    AUDIO_GENERATE_BTN = 'button:has-text("Generate"), button:has-text("Create")'
    AUDIO_CUSTOMIZE_BTN = 'button:has-text("Customize")'
    AUDIO_PROMPT_INPUT = (
        'textarea[aria-label*="instruction"], '
        'textarea[placeholder*="instruction"], '
        "textarea"
    )
    AUDIO_LANGUAGE_DROPDOWN = 'button[aria-label*="language"], [role="listbox"], select'
    AUDIO_READY_INDICATOR = (
        '[data-audio-status="ready"], '
        'button[aria-label="Play"], '
        'button:has-text("Listen")'
    )
    AUDIO_GENERATING_INDICATOR = (
        '[data-audio-status="generating"], '
        ':has-text("Generating"), '
        ':has-text("Creating audio")'
    )
    AUDIO_LIMIT_INDICATOR = (
        ':has-text("reached your limit"), '
        ':has-text("daily limit"), '
        ':has-text("generation limit")'
    )
    AUDIO_DOWNLOAD_BTN = (
        'button[aria-label="Download"], '
        'button:has-text("Download"), '
        '[aria-label="More options"] >> button:has-text("Download")'
    )
    AUDIO_PLAYER = "audio"

    # Chat/Prompt area
    CHAT_INPUT = (
        'textarea[placeholder*="Ask"], '
        'textarea[aria-label*="Ask"], '
        'textarea[placeholder*="Type"], '
        'textarea[aria-label*="chat" i], '
        'textarea[aria-label*="message" i], '
        '[role="textbox"], '
        'div[contenteditable="true"], '
        '[contenteditable="true"]'
    )
    CHAT_SEND_BTN = 'button[aria-label="Send"], button[type="submit"]'
    CHAT_RESPONSE = '[data-message-role="assistant"], .response-message'
    CHAT_LOADING = '[data-loading="true"], .loading-indicator'

    # Export/Download
    EXPORT_BTN = 'button:has-text("Export"), button[aria-label="Export"]'
    EXPORT_PDF_OPTION = 'button:has-text("PDF"), [data-format="pdf"]'
    DOWNLOAD_LINK = 'a[download], a:has-text("Download")'

    # Common UI elements
    MODAL_OVERLAY = '[role="dialog"], .modal-overlay'
    MODAL_CLOSE_BTN = 'button[aria-label="Close"], button:has-text("Cancel")'
    LOADING_SPINNER = ".spinner, [data-loading], .loading"
    ERROR_MESSAGE = '[role="alert"], .error-message'
    SUCCESS_MESSAGE = '.success-message, [data-status="success"]'

    @classmethod
    def get_all(cls) -> dict[str, str]:
        """Return all selectors as dict for debugging."""
        return {
            name: value
            for name, value in vars(cls).items()
            if isinstance(value, str) and not name.startswith("_")
        }

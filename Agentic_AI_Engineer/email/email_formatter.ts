function escapeHtml(text: string): string {
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

export function formatEmail(
    subject: string,
    content: string
) {
    const safeContent = escapeHtml(content);

    return {
        subject,
        body: `
            <pre style="
                font-family: Arial, sans-serif;
                white-space: pre-wrap;
                font-size: 14px;
            ">${safeContent}</pre>
        `
    };
}
export function looksLikeEmailRequest(text: string): boolean {
    return /\b(email|e-mail|send\s+me\s+an?\s+email|send\s+this\s+to\s+my\s+email)\b/i.test(text);
}
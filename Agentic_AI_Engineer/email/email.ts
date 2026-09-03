import "dotenv/config";
import nodemailer from "nodemailer";

const transporter = nodemailer.createTransport({
    service: "gmail",
    auth: {
        user: process.env.EMAIL_USER,
        pass: process.env.EMAIL_PASSWORD
    }
});

interface EmailDraft {
    draft: {
        to: string;
        subject: string;
        body: string;
    };
    status: "pending_approval" | "approved" | "rejected";
}
export function draftEmail(
    to: string,
    subject: string,
    body: string
): EmailDraft {
    return {
        draft: {
            to,
            subject,
            body
        },
        status: "pending_approval"
    };
}

export function approveEmail(email: EmailDraft, approved: boolean): EmailDraft {
    if (approved !== true) {
        return {
            ...email,
            status: "rejected"
        };
    }
    return {
        ...email,
        status: "approved"
    };
}

export async function sendApprovedEmail(email: EmailDraft) {
    if (email.status !== "approved") {
        return {
            success: false,
            message: "Email cannot be sent without explicit approval."
        };
    }
    try {
        await transporter.sendMail({
            from: process.env.EMAIL_USER,
            to: email.draft.to,
            subject: email.draft.subject,
            html: email.draft.body
        });

        return {
            success: true,
            message: "Email sent successfully."
        };
    } catch (error) {
        console.error("Email sending failed:", error);

        return {
            success: false,
            message: "Failed to send email."
        };
    }
}
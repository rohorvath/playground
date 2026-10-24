#!/usr/bin/env python3
"""Send the "merge to main" notification email through Gmail SMTP.

All input comes from environment variables, so workflow data (commit message,
actor, ...) is never interpolated into shell code.

Usage: send-mail.py [--dry-run]    (--dry-run prints the message instead of sending)
"""
import os
import smtplib
import ssl
import sys
from email.message import EmailMessage

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
TIMEOUT_SECONDS = 30
JOBS = ("build", "test", "release", "deploy", "github-release")


def build_message(env):
    user = env["SMTP_USERNAME"]
    repo = env["REPO"]
    tag = env.get("RELEASE_TAG", "")

    lines = [
        f"A change was merged to main in {repo}.",
        "",
        f"Commit:  {env.get('COMMIT_MESSAGE', '')}",
        f"By:      {env.get('ACTOR', '')}",
        f"SHA:     {env.get('SHA', '')}",
        f"Release: {tag or 'not created'}",
        "",
        "Job results",
    ]
    for job in JOBS:
        result = env.get("RESULT_" + job.upper().replace("-", "_"), "unknown")
        lines.append(f"{job + ':':<16}{result}")
    lines += ["", f"Run: {env.get('RUN_URL', '')}"]

    msg = EmailMessage()
    msg["Subject"] = f"[{repo}] merge to main: {tag or 'no release'}"
    msg["From"] = f"GitHub Actions <{user}>"
    msg["To"] = user
    msg.set_content("\n".join(lines))
    return msg


def main():
    msg = build_message(os.environ)
    if "--dry-run" in sys.argv:
        print(msg)
        return
    with smtplib.SMTP_SSL(
        SMTP_HOST, SMTP_PORT, context=ssl.create_default_context(), timeout=TIMEOUT_SECONDS
    ) as smtp:
        smtp.login(os.environ["SMTP_USERNAME"], os.environ["SMTP_PASSWORD"])
        smtp.send_message(msg)
    print(f"Sent notification to {msg['To']}")


if __name__ == "__main__":
    main()

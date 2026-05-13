// Cloudflare Pages Function: POST /api/contact
// Receives the contact-form submission, validates it, sends an email to
// grant@windstorminstitute.org via the Resend API.
//
// Env required:
//   RESEND_API_KEY  — Resend API key (set in CF Pages > Settings > Environment variables)

const FROM = "Windstorm Institute <hello@windstorminstitute.org>";
const TO = ["grant@windstorminstitute.org"];
const MIN_FILL_MS = 1500;       // <1.5s = bot
const MAX_MESSAGE_LEN = 8000;   // 8 KB cap
const MAX_FIELD_LEN = 200;      // name/email/subject cap

const json = (status, body) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" },
  });

const esc = (s) =>
  String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

function isValidEmail(s) {
  if (typeof s !== "string" || s.length > MAX_FIELD_LEN) return false;
  return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(s);
}

export async function onRequestPost({ request, env }) {
  // Content-Type sanity
  const ct = request.headers.get("Content-Type") || "";
  let data = {};
  try {
    if (ct.includes("application/json")) {
      data = await request.json();
    } else if (ct.includes("application/x-www-form-urlencoded") || ct.includes("multipart/form-data")) {
      const fd = await request.formData();
      data = Object.fromEntries(fd.entries());
    } else {
      return json(415, { ok: false, error: "Unsupported content type" });
    }
  } catch {
    return json(400, { ok: false, error: "Malformed body" });
  }

  // Honeypot — bots fill the "website" field; humans never see it
  if (typeof data.website === "string" && data.website.trim() !== "") {
    // Silent success: pretend we sent it, but don't actually send. Bot moves on.
    return json(200, { ok: true });
  }

  // Form-fill time check (frontend stamps `t` with form-render time)
  const t = Number(data.t);
  if (Number.isFinite(t) && Date.now() - t < MIN_FILL_MS) {
    return json(200, { ok: true });
  }

  // Required fields
  const name = String(data.name || "").trim();
  const email = String(data.email || "").trim();
  const subject = String(data.subject || "").trim();
  const message = String(data.message || "").trim();

  if (!name || name.length > MAX_FIELD_LEN) return json(400, { ok: false, error: "Name is required (and under 200 chars)." });
  if (!isValidEmail(email)) return json(400, { ok: false, error: "Valid email is required." });
  if (!subject || subject.length > MAX_FIELD_LEN) return json(400, { ok: false, error: "Subject is required (and under 200 chars)." });
  if (!message || message.length > MAX_MESSAGE_LEN) return json(400, { ok: false, error: "Message is required (and under 8 KB)." });

  if (!env.RESEND_API_KEY) {
    return json(500, { ok: false, error: "Server is missing RESEND_API_KEY env var." });
  }

  // Build the email body
  const ip = request.headers.get("CF-Connecting-IP") || "?";
  const ua = request.headers.get("User-Agent") || "?";
  const country = request.cf && request.cf.country ? request.cf.country : "?";

  const subjectFinal = `[Contact] ${subject.slice(0, 140)}`;
  const textBody =
`Contact form submission from windstorminstitute.org

From:    ${name} <${email}>
Subject: ${subject}

${message}

---
Sender IP:    ${ip}
Country:      ${country}
User-Agent:   ${ua}
`;

  const htmlBody = `<!doctype html>
<html>
<body style="font-family:-apple-system,BlinkMacSystemFont,Inter,sans-serif;font-size:15px;line-height:1.55;color:#1a1a18;max-width:640px;margin:0 auto;padding:24px;">
  <p style="font-family:monospace;font-size:11px;color:#6b6b67;letter-spacing:0.1em;text-transform:uppercase;margin:0 0 16px;">Contact form &middot; windstorminstitute.org</p>
  <p style="margin:0 0 8px;"><strong>From:</strong> ${esc(name)} &lt;<a href="mailto:${esc(email)}" style="color:#185fa5;">${esc(email)}</a>&gt;</p>
  <p style="margin:0 0 8px;"><strong>Subject:</strong> ${esc(subject)}</p>
  <hr style="border:none;border-top:1px solid #e5e5e3;margin:16px 0;">
  <div style="white-space:pre-wrap;font-size:15px;line-height:1.6;">${esc(message)}</div>
  <hr style="border:none;border-top:1px solid #e5e5e3;margin:24px 0 16px;">
  <p style="font-size:12px;color:#9b9b95;margin:0;">Sender IP: ${esc(ip)} &middot; Country: ${esc(country)}<br>User-Agent: ${esc(ua)}</p>
</body>
</html>`;

  // Send via Resend
  const r = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${env.RESEND_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      from: FROM,
      to: TO,
      reply_to: email,
      subject: subjectFinal,
      text: textBody,
      html: htmlBody,
    }),
  });

  if (!r.ok) {
    const errText = await r.text().catch(() => "");
    return json(502, { ok: false, error: `Resend returned ${r.status}`, detail: errText.slice(0, 400) });
  }

  return json(200, { ok: true });
}

// Reject all non-POST methods cleanly
export function onRequestGet() {
  return json(405, { ok: false, error: "POST only" });
}

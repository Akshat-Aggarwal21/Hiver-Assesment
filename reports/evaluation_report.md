# Hiver AI Email Evaluation & Benchmark Report

## Executive Summary
- **Total Tickets Evaluated**: 20
- **Overall Mean HEQI Score**: **83.18 / 100**
- **Policy & Factual Adherence**: 84.92%
- **Intent Resolution & Completeness**: 72.06%
- **Tone & Empathy**: 95.75%
- **Actionability & Clarity**: 86.0%
- **Semantic Similarity to Ground Truth**: 76.37%
- **ROUGE-L F1**: 0.5591
- **High Confidence Drafts (HEQI ≥ 85)**: 8 / 20

## Category Performance Breakdown
| Category | Count | Mean HEQI Score |
| :--- | :---: | :---: |
| `cancellation_refund` | 3.0 | **88.35** |
| `technical_issue` | 5.0 | **81.04** |
| `account_access` | 3.0 | **80.7** |
| `billing` | 3.0 | **86.87** |
| `sla_escalation` | 2.0 | **78.72** |
| `feature_request` | 2.0 | **83.59** |
| `onboarding` | 2.0 | **82.97** |

## Customer Sentiment Breakdown
| Sentiment | Count | Mean HEQI Score |
| :--- | :---: | :---: |
| `frustrated` | 5.0 | **84.81** |
| `angry` | 3.0 | **84.84** |
| `urgent` | 4.0 | **80.61** |
| `neutral` | 4.0 | **85.44** |
| `confused` | 4.0 | **80.19** |

## Detailed Per-Ticket Evaluation Results

### Ticket: `TICK-101` (cancellation_refund)
- **Composite HEQI**: **89.35/100**
- **Sub-scores**: Policy: 100.0 | Intent: 71.67 | Tone: 100.0 | Actionability: 90.0 | Semantic: 79.37%
- **ROUGE-L**: 0.5992 | **BLEU**: 37.83
- **Strengths**: Strong policy adherence (4 required facts covered), Excellent empathetic tone and de-escalation demeanor, Clear actionable steps and diagnostic instructions provided
- **Improvements**: Did not fully address: Acknowledge finance audit requirement

<details>
<summary>Click to view Generated Reply vs Ground Truth</summary>

**Generated Reply:**
```text
Hi Sarah,

Thank you for contacting Hiver Support, and I completely understand how frustrating this situation is for your team. Let's get this resolved right away.

Because your charge occurred just 4 days ago, your request falls squarely within our 14-day full refund guarantee.

I have taken the following actions immediately:
1. **Full Refund Processed**: Initiated a complete refund of $1440.00 back to your original payment method. Please allow 3-5 business days for your bank to reflect the credited funds.
2. **Subscription Cancelled**: Cancelled your auto-renewal so no future charges will ever occur.

A formal credit note and receipt have been dispatched to your billing email.

Best regards,
Hiver Customer Support
```

**Ground Truth Reference:**
```text
Hi Sarah,

Thank you for reaching out, and I completely understand the urgency around this renewal charge.

Because your renewal occurred just 4 days ago, your request falls well within our 14-day full refund guarantee. I have gone ahead and processed a full refund of $1,440.00 back to your original American Express card.

Please allow 3-5 business days for your banking institution to reflect the credited funds. Additionally, I have cancelled the auto-renewal on your Pro subscription so you won't incur any future charges.

A formal credit note receipt has also been sent to your billing email for your finance audit. Please let me know if you need anything else!

Best regards,
Customer Success Team
```
</details>

---

### Ticket: `TICK-102` (technical_issue)
- **Composite HEQI**: **85.36/100**
- **Sub-scores**: Policy: 75.0 | Intent: 85.0 | Tone: 100.0 | Actionability: 96.0 | Semantic: 72.12%
- **ROUGE-L**: 0.5475 | **BLEU**: 23.89
- **Strengths**: Comprehensive intent coverage addressing customer questions, Excellent empathetic tone and de-escalation demeanor, Clear actionable steps and diagnostic instructions provided
- **Improvements**: Ensure all required policy terms and timelines are explicitly mentioned

<details>
<summary>Click to view Generated Reply vs Ground Truth</summary>

**Generated Reply:**
```text
Dear David,

Thank you for reaching out to Enterprise Support. I want to apologize directly and unreservedly for this disruption -- given your Enterprise agreement, I am taking personal ownership of this ticket.

Our telemetry indicates an OAuth token refresh timeout for your connected Google Workspace inbox.

To restore real-time sync immediately:
1. Have a Google Workspace Admin navigate to **Integrations > Gmail** in Hiver.
2. Click **'Re-authorize Account'** to refresh the OAuth handshake.
3. All pending queued emails will back-populate within 3-5 minutes with zero data loss.

Our Tier 2 on-call engineers are monitoring your mailbox queue directly until sync is confirmed.

Warm regards,
Hiver Enterprise Support Team
```

**Ground Truth Reference:**
```text
Hi David,

I sincerely apologize for the disruption and frustration this sync interruption has caused your team today. Given your Enterprise SLA, I am prioritizing this directly.

Our telemetry indicates that Google Workspace OAuth tokens for 'support@apexlogistics.com' experienced a credential refresh timeout approximately 2 hours ago. 

To restore real-time sync immediately, please take the following step:
1. Have a Google Workspace Admin navigate to Integrations > Gmail in the Hiver dashboard and click 'Re-authorize Account'.
2. This refreshes the OAuth handshake, and all pending queued emails will back-populate within 3-5 minutes without any data loss.

I have also engaged our Tier 2 on-call engineers to monitor your inbox queue directly. I will stay on this thread until we verify incoming mail flows smoothly. If you prefer a live bridge, reply here and I will generate an instant Google Meet link.

Warm regards,
Senior Enterprise Support
```
</details>

---

### Ticket: `TICK-103` (account_access)
- **Composite HEQI**: **81.03/100**
- **Sub-scores**: Policy: 100.0 | Intent: 43.33 | Tone: 90.0 | Actionability: 96.0 | Semantic: 77.97%
- **ROUGE-L**: 0.5736 | **BLEU**: 35.23
- **Strengths**: Strong policy adherence (3 required facts covered), Excellent empathetic tone and de-escalation demeanor, Clear actionable steps and diagnostic instructions provided
- **Improvements**: Did not fully address: Address urgent lockout with empathy, Provide fast path via Admin reset

<details>
<summary>Click to view Generated Reply vs Ground Truth</summary>

**Generated Reply:**
```text
Hi Elena,

I understand the urgency of this request, and I am treating this with immediate priority.

For user data security and compliance, our support protocols strictly prevent agents from manually bypassing or disabling 2FA over email.

Here is how you can regain access immediately:
1. Your Workspace Admin (admin@cloudtech.io) can reset your 2FA in under 30 seconds by navigating to **Settings > Teammates > [Your Name] > 'Reset 2FA'**.
2. Upon reset, you will receive an automated one-time link to configure your new authenticator device upon next login.

I have CC'd your administrator on this thread to help expedite their action.

Best regards,
Hiver Customer Support
```

**Ground Truth Reference:**
```text
Hi Elena,

I am sorry to hear about your lost phone—I know being locked out when urgent customer emails are waiting is stressful.

To safeguard your organization's sensitive customer communications, our security compliance protocols strictly prevent support agents from manually bypassing or disabling 2FA over email.

Here is how you can regain access quickly:
1. Your Workspace Admin (admin@cloudtech.io) has full authority to reset your 2FA from the Hiver console by going to Settings > Teammates > Elena Rostova > 'Reset 2FA'. This takes less than 30 seconds.
2. Once they trigger the reset, you will receive an automated one-time activation link to register a new authenticator device upon your next login.

I have also CC'd your admin team on this ticket to help expedite their action. Please let me know once they reset it if you encounter any difficulties logging in!

Best regards,
Hiver Security & Support
```
</details>

---

### Ticket: `TICK-104` (billing)
- **Composite HEQI**: **92.23/100**
- **Sub-scores**: Policy: 100.0 | Intent: 100.0 | Tone: 87.5 | Actionability: 78.0 | Semantic: 80.25%
- **ROUGE-L**: 0.6446 | **BLEU**: 38.32
- **Strengths**: Strong policy adherence (4 required facts covered), Comprehensive intent coverage addressing customer questions, Excellent empathetic tone and de-escalation demeanor
- **Improvements**: Add numbered steps or explicit next actions to improve clarity

<details>
<summary>Click to view Generated Reply vs Ground Truth</summary>

**Generated Reply:**
```text
Hi Markus,

Thank you for getting in touch with Hiver Support! I am glad to assist you with this today.

I have updated your company profile with VAT ID DE349281902 and submitted invoice #INV-2026-08 to our finance team for manual re-issuance.

Because revised tax documents require formal accounting review, processing takes 1-2 business days. As soon as the updated PDF is generated, I will email it to you directly and it will be available in Settings > Billing > Invoices.

To ensure all future invoices include your VAT ID automatically, please verify your billing address in Settings > Billing.

Best regards,
Hiver Customer Support
```

**Ground Truth Reference:**
```text
Hi Markus,

Thank you for getting in touch, and happy to help with your invoice update!

I have updated your billing profile with your German VAT ID (DE349281902) and submitted invoice #INV-2026-08 to our finance team for manual re-issuance. Because this involves past tax adjustments, revised invoices typically take 1-2 business days to process.

As soon as the updated PDF is regenerated, I will email it directly to you and it will also be downloadable from your dashboard under Settings > Billing > Invoices.

To ensure all future monthly invoices automatically include your VAT details, please confirm that your registered legal entity name and German billing address in Settings > Billing match your official corporate registration.

I will follow up here with your revised invoice as soon as it is ready!

Best regards,
Hiver Billing Operations
```
</details>

---

### Ticket: `TICK-105` (sla_escalation)
- **Composite HEQI**: **77.11/100**
- **Sub-scores**: Policy: 75.0 | Intent: 63.75 | Tone: 100.0 | Actionability: 75.0 | Semantic: 74.26%
- **ROUGE-L**: 0.5836 | **BLEU**: 39.27
- **Strengths**: Excellent empathetic tone and de-escalation demeanor
- **Improvements**: Ensure all required policy terms and timelines are explicitly mentioned, Did not fully address: Provide immediate recovery timeline, Add numbered steps or explicit next actions to improve clarity

<details>
<summary>Click to view Generated Reply vs Ground Truth</summary>

**Generated Reply:**
```text
Dear Jonathan,

Thank you for reaching out to Enterprise Support. I want to apologize directly and unreservedly for this disruption -- given your Enterprise agreement, I am taking personal ownership of this ticket.

You are entirely correct: our 1-hour Enterprise SLA was breached, and this falls short of our standard of reliability.

I have escalated this incident to our Head of Engineering and your dedicated CSM, Rachel Vance.

**Incident Update**: A hotfix was deployed at 1:45 PM for an isolated rule queue delay. We are back-processing all unassigned emails across your 4 mailboxes, with full queue clearance expected within 20 minutes.

Your CSM will follow up by 5:00 PM EST today with a formal Post-Incident Report (PIR) and your SLA credit adjustment.

Warm regards,
Hiver Enterprise Support Team
```

**Ground Truth Reference:**
```text
Dear Jonathan,

I want to apologize directly and unreservedly for the delay in responding to your ticket today. You are entirely correct: our 1-hour Enterprise SLA was breached, and this falls short of the high standard of reliability you expect and deserve from Hiver.

I have personally escalated this incident to our Head of Engineering and your dedicated Customer Success Manager, Rachel Vance. 

Regarding the root cause: an isolated latency spike in our rule execution queue delayed webhook triggers between 11:00 AM and 1:30 PM. A hotfix was deployed at 1:45 PM, and automated assignments have fully resumed. We are currently back-processing all unassigned emails in your 4 mailboxes in chronological order, with complete queue clearance estimated within the next 20 minutes.

Rachel Vance will also reach out by 5:00 PM EST today with a formal Post-Incident Report (PIR) and details regarding your Enterprise SLA credit adjustment. I am monitoring your queue live and will confirm the moment all backlogs clear.

Sincerely,
Director of Customer Experience
```
</details>

---

### Ticket: `TICK-106` (feature_request)
- **Composite HEQI**: **87.2/100**
- **Sub-scores**: Policy: 100.0 | Intent: 85.0 | Tone: 87.5 | Actionability: 68.0 | Semantic: 82.54%
- **ROUGE-L**: 0.6207 | **BLEU**: 34.64
- **Strengths**: Strong policy adherence (3 required facts covered), Comprehensive intent coverage addressing customer questions, Excellent empathetic tone and de-escalation demeanor
- **Improvements**: Add numbered steps or explicit next actions to improve clarity

<details>
<summary>Click to view Generated Reply vs Ground Truth</summary>

**Generated Reply:**
```text
Hi Clara,

Thank you for getting in touch with Hiver Support! I am glad to assist you with this today.

A native bi-directional HubSpot contact and timeline sync is one of our top requests, and our Product team has scheduled it for active development in Q4!

I have linked your account (ACC-64019) to the feature ticket so you will receive an invitation when our closed beta opens in November.

In the interim, many teams use our Zapier or Webhook template to automatically sync customer emails to HubSpot deals. Let me know if you'd like our Solutions team to send over that template!

Best regards,
Hiver Customer Support
```

**Ground Truth Reference:**
```text
Hi Clara,

Thank you for reaching out and for your kind words about Hiver! It's fantastic to hear that your team is getting value from our shared inbox.

A native bi-directional HubSpot contact and timeline sync is indeed one of our most requested capabilities, and I have great news: our Product team has scheduled native HubSpot integration for active development in Q4!

I have officially linked your account (ACC-64019) to the feature request ticket. This ensures you will automatically receive an invitation when our closed beta opens in late November, giving your team early access to test the sync.

In the interim, many of our customers use our Zapier or Webhook integration to automatically log incoming customer threads to HubSpot deals and contacts. If you would like our Solutions team to share a pre-built Zapier template for this, please let me know!

Best regards,
Hiver Product Operations
```
</details>

---

### Ticket: `TICK-107` (onboarding)
- **Composite HEQI**: **80.38/100**
- **Sub-scores**: Policy: 100.0 | Intent: 42.5 | Tone: 97.5 | Actionability: 83.0 | Semantic: 78.09%
- **ROUGE-L**: 0.5197 | **BLEU**: 27.04
- **Strengths**: Strong policy adherence (3 required facts covered), Excellent empathetic tone and de-escalation demeanor, Clear actionable steps and diagnostic instructions provided
- **Improvements**: Did not fully address: Provide actionable resolution steps

<details>
<summary>Click to view Generated Reply vs Ground Truth</summary>

**Generated Reply:**
```text
Hi Liam,

Thank you for reaching out! Happy to clarify this for you and guide you through the exact steps.

When new teammates accept workspace invitations, two quick steps are required:

1. **Install Hiver Chrome Extension**: Each agent must install the extension from hiverhq.com/extension to render shared inboxes inside Gmail.
2. **Mailbox Member Assignment**: In Settings > Shared Mailboxes > 'Support' > Teammates, ensure all 3 new agents are toggled ON as active members.

Once they install the extension and refresh Gmail, the mailbox will appear immediately in their sidebar.

Best regards,
Hiver Customer Support
```

**Ground Truth Reference:**
```text
Hi Liam,

Welcome aboard, and thank you for contacting Hiver Support!

This is a common question during onboarding. When new teammates accept the workspace invitation, there are two quick steps needed before shared mailboxes appear inside Gmail:

1. **Install the Hiver Chrome Extension**: Each new agent must install our Chrome Extension from the Chrome Web Store (hiverhq.com/extension). The shared inbox panel is rendered directly by the extension inside Gmail.
2. **Shared Mailbox Permission Assignment**: As an Admin, please go to Settings > Shared Mailboxes > 'Support' > Teammates, and ensure that Tim, Mia, and Alex are toggled ON as active members of that specific mailbox.

Once they install the extension and refresh Gmail, the 'Support' shared mailbox will appear immediately in their left-hand Gmail sidebar.

If any of them still don't see it after these steps, please let me know and I'd be happy to jump on a quick screen share to verify!

Warm regards,
Hiver Onboarding Specialist
```
</details>

---

### Ticket: `TICK-108` (technical_issue)
- **Composite HEQI**: **68.79/100**
- **Sub-scores**: Policy: 75.0 | Intent: 28.33 | Tone: 97.5 | Actionability: 83.0 | Semantic: 72.59%
- **ROUGE-L**: 0.5064 | **BLEU**: 27.86
- **Strengths**: Excellent empathetic tone and de-escalation demeanor, Clear actionable steps and diagnostic instructions provided
- **Improvements**: Ensure all required policy terms and timelines are explicitly mentioned, Did not fully address: Explain why collision alert didn't trigger, Provide preventative configuration steps

<details>
<summary>Click to view Generated Reply vs Ground Truth</summary>

**Generated Reply:**
```text
Hi Priya,

Thank you for reaching out! Happy to clarify this for you and guide you through the exact steps.

Collision detection relies on an active WebSocket connection over port 443 to broadcast real-time agent presence.

Here are the two most common reasons a collision banner may fail:
1. **WebSocket Interruption (Firewall/VPN)**: If either agent was connected via corporate VPN, presence packets may have been throttled.
2. **Extension Cache**: Ensure both reps visit `chrome://extensions`, toggle Developer Mode, and click 'Update' to run the latest version.

If you can share the email message-ID or timestamps, our engineers will inspect the WebSocket session logs right away.

Best regards,
Hiver Customer Support
```

**Ground Truth Reference:**
```text
Hi Priya,

I completely understand how uncomfortable that situation is with your client—preventing duplicate replies is one of Hiver's core promises, so let's get this sorted out right away.

Collision detection relies on an active WebSocket connection over secure port 443 to broadcast real-time agent presence (viewing and typing). Here are the primary reasons a collision banner might fail to appear:

1. **WebSocket Interruption (Firewall / VPN)**: If either agent was connected via a corporate VPN or strict firewall, WebSocket packets may have been throttled or blocked, causing presence heartbeats to fail.
2. **Extension Version Mismatch**: If one agent was running an older cached version of the Hiver Chrome extension, live presence signals may not sync.
3. **Quick Diagnostic**: Ask both agents to visit `chrome://extensions`, verify 'Developer Mode' is not conflicting, and click 'Update' to guarantee they are on version 8.14+.

We also recommend checking Settings > Email Collaboration > 'Collision Alerts' to ensure alerts are configured to 'Prominent Banner + Lock'. 

If you can share the email message-ID or timestamps, our engineers can review the WebSocket logs for those two user sessions to pinpoint the exact drop. Let me know!

Best regards,
Hiver Technical Support
```
</details>

---

### Ticket: `TICK-109` (cancellation_refund)
- **Composite HEQI**: **83.63/100**
- **Sub-scores**: Policy: 100.0 | Intent: 56.67 | Tone: 100.0 | Actionability: 78.0 | Semantic: 77.63%
- **ROUGE-L**: 0.5436 | **BLEU**: 32.1
- **Strengths**: Strong policy adherence (4 required facts covered), Excellent empathetic tone and de-escalation demeanor
- **Improvements**: Did not fully address: Provide fair resolution and stop recurring billing, Add numbered steps or explicit next actions to improve clarity

<details>
<summary>Click to view Generated Reply vs Ground Truth</summary>

**Generated Reply:**
```text
Hi Tom,

Thank you for contacting Hiver Support, and I completely understand how frustrating this situation is for your team. Let's get this resolved right away.

I reviewed your account history: while no prior cancellation was recorded via Settings > Billing, I can confirm zero account activity over the past 6 months.

Per standard policy, past monthly charges are non-refundable. However, in light of your zero usage and as a gesture of goodwill, I have secured management approval to issue a 50% refund ($135.00) directly back to your payment card (settling in 3-5 business days), and applied the remaining $135.00 as non-expiring credit.

Your subscription has been terminated immediately so you will not be billed again.

Best regards,
Hiver Customer Support
```

**Ground Truth Reference:**
```text
Hi Tom,

Thank you for reaching out, and I understand how frustrating it is to discover ongoing recurring charges for software your team was not actively using.

I reviewed your account audit log: while there was no recorded cancellation submitted through Settings > Billing back in March, I can clearly see that account activity was zero across these past 6 months.

Per our standard billing policy, past monthly charges beyond 14 days are non-refundable. However, in light of your zero usage and as a gesture of goodwill, I have secured special management approval to issue a full 50% refund ($135.00) back to your card, and I have credited the remaining $135.00 as lifetime credit on your file should you ever return.

Furthermore, I have immediately terminated the subscription today to ensure zero future charges occur.

The $135.00 refund will appear on your statement in 3-5 business days. Please let me know if you need an itemized final zero-balance statement for your records.

Warm regards,
Hiver Billing Support
```
</details>

---

### Ticket: `TICK-110` (technical_issue)
- **Composite HEQI**: **84.26/100**
- **Sub-scores**: Policy: 75.0 | Intent: 85.0 | Tone: 100.0 | Actionability: 83.0 | Semantic: 80.57%
- **ROUGE-L**: 0.5765 | **BLEU**: 35.09
- **Strengths**: Comprehensive intent coverage addressing customer questions, Excellent empathetic tone and de-escalation demeanor, Clear actionable steps and diagnostic instructions provided
- **Improvements**: Ensure all required policy terms and timelines are explicitly mentioned

<details>
<summary>Click to view Generated Reply vs Ground Truth</summary>

**Generated Reply:**
```text
Hi Amira,

Thank you for contacting Hiver Support, and I completely understand how frustrating this situation is for your team. Let's get this resolved right away.

Thank you for alerting us to this, and I sincerely apologize for the concern this is causing your team. Disappearing tags on urgent customer communications is serious, and I am here to help you resolve this promptly.

When a shared tag disappears seconds after being applied, it is almost always caused by:
1. **Gmail Native Label Conflict**: If a personal Gmail label named 'Urgent' is set to auto-filter, Gmail's IMAP sync overwrites the shared tag.
2. **Competing Rule Overlap**: Check Settings > Automation Rules to ensure another rule doesn't have an action removing tags.

**Quick fix**: Renaming the shared tag to 'P1-Urgent' decouples it immediately from Gmail's personal labels.

I have checked our event logs for your account and would be glad to perform a comprehensive backend rule review for you—just reply with permission to inspect your settings.

Best regards,
Hiver Customer Support
```

**Ground Truth Reference:**
```text
Hi Amira,

Thank you for alerting us to this, and I apologize for the concern this is causing your support operations. Disappearing tags on urgent emails is serious, and I am here to help you get this resolved promptly.

When a tag vanishes within seconds of application, it almost always points to one of two root causes:

1. **Gmail Native Label Conflict**: If Gmail has a native user label with the identical name 'Urgent' that is set to auto-archive or auto-filter, Gmail's IMAP sync may overwrite Hiver's shared tag metadata. 
2. **Competing Rule Overlap**: If another Hiver automation rule has a trigger like 'On agent assignment -> Remove tag', it may immediately strip the tag.

To diagnose this right now:
- Navigate to Settings > Automation Rules and check if any secondary rule has an action that removes tags.
- In Gmail Settings > Labels, check if a personal label named 'Urgent' exists. If so, renaming the Hiver shared tag to 'P1-Urgent' immediately decouples it from Gmail's personal label filter.

I have also checked our backend event logs for your workspace (ACC-55193) and can see rule executions triggering. If you'd like, I can inspect the exact rule IDs for you—just reply with permission to review your automation settings.

Best regards,
Hiver Technical Support
```
</details>

---

### Ticket: `TICK-111` (billing)
- **Composite HEQI**: **86.03/100**
- **Sub-scores**: Policy: 100.0 | Intent: 56.67 | Tone: 97.5 | Actionability: 96.0 | Semantic: 79.62%
- **ROUGE-L**: 0.6432 | **BLEU**: 36.35
- **Strengths**: Strong policy adherence (4 required facts covered), Excellent empathetic tone and de-escalation demeanor, Clear actionable steps and diagnostic instructions provided
- **Improvements**: Did not fully address: Explain the $52.50 charge reason

<details>
<summary>Click to view Generated Reply vs Ground Truth</summary>

**Generated Reply:**
```text
Hi Marcus,

Thank you for reaching out! Happy to clarify this for you and guide you through the exact steps.

The $52.50 transaction represents pro-rated billing for 3 new team seats added midway through your monthly cycle.

Here is the breakdown:
- Pro seat rate: $25.00/seat/month.
- 3 seats × $25 × (remaining 21 days / 30) = exactly $52.50.

On your next regular monthly renewal (October 1st), all seats will be consolidated into a single standard invoice. You can download the itemized invoice under Settings > Billing > Invoices.

Best regards,
Hiver Customer Support
```

**Ground Truth Reference:**
```text
Hi Marcus,

Thank you for reaching out, and happy to clarify this charge for you!

The $52.50 transaction on September 14th represents pro-rated billing for 3 new team members added to your Pro plan midway through your billing cycle.

Here is how that breaks down:
- Standard Pro seat rate: $25.00/seat/month.
- On September 14th, 3 seats were invited, with 21 days remaining in your monthly billing cycle.
- 3 seats × $25 × (21/30 days) = exactly $52.50.

Moving forward, on your next regular billing cycle (October 1st), these 3 seats will simply be consolidated into your regular single monthly invoice.

You can always download the itemized invoice for this charge under Settings > Billing > Invoices. Let me know if you have any other questions about your subscription!

Best regards,
Hiver Billing Team
```
</details>

---

### Ticket: `TICK-112` (technical_issue)
- **Composite HEQI**: **81.07/100**
- **Sub-scores**: Policy: 75.0 | Intent: 71.67 | Tone: 100.0 | Actionability: 89.0 | Semantic: 73.03%
- **ROUGE-L**: 0.4842 | **BLEU**: 29.65
- **Strengths**: Excellent empathetic tone and de-escalation demeanor, Clear actionable steps and diagnostic instructions provided
- **Improvements**: Ensure all required policy terms and timelines are explicitly mentioned, Did not fully address: Reference provided details (v8.11.2 on macOS)

<details>
<summary>Click to view Generated Reply vs Ground Truth</summary>

**Generated Reply:**
```text
Hi Natalie,

Thank you for contacting Hiver Support, and I completely understand how frustrating this situation is for your team. Let's get this resolved right away.

Thank you for confirming your extension version and troubleshooting steps.

That specific 504 error on version 8.11.2 was related to an endpoint upgrade and is fully patched in version 8.14.3.

To fix this immediately:
1. Open Chrome and navigate to `chrome://extensions`.
2. Toggle on **Developer mode** in the top right.
3. Click **Update** to download version 8.14.3+.
4. Refresh Gmail with `Cmd + Shift + R` (or `Ctrl + Shift + R`).

I will keep this ticket open to ensure your inbox loads normally without further crashes.

Best regards,
Hiver Customer Support
```

**Ground Truth Reference:**
```text
Hi Natalie,

Thank you for checking those details so quickly, and I apologize for the disruption this 504 crash is causing to your daily workflow.

That specific error on version 8.11.2 was caused by an outdated API endpoint that was deprecated in our recent infrastructure release. We patched this in version 8.14.3.

Here is how to resolve it in under 60 seconds:
1. Open Google Chrome and go to `chrome://extensions` in your address bar.
2. In the top-right corner, toggle on **Developer mode**.
3. Click the **Update** button that appears in the top menu.
4. Verify that Hiver updates to version 8.14.3 (or later), then reload Gmail (`Cmd + Shift + R`).

This will re-establish the connection to our updated gateway endpoints and eliminate the 504 error completely.

I will keep this ticket open until you reply to confirm your inbox is loading normally without crashes. Thank you for your patience!

Best regards,
Hiver Technical Operations
```
</details>

---

### Ticket: `TICK-113` (account_access)
- **Composite HEQI**: **80.47/100**
- **Sub-scores**: Policy: 65.0 | Intent: 85.0 | Tone: 95.0 | Actionability: 90.0 | Semantic: 72.25%
- **ROUGE-L**: 0.5413 | **BLEU**: 27.16
- **Strengths**: Comprehensive intent coverage addressing customer questions, Excellent empathetic tone and de-escalation demeanor, Clear actionable steps and diagnostic instructions provided
- **Improvements**: Ensure all required policy terms and timelines are explicitly mentioned, Policy violation detected: Immediately transferring root ownership without domain/officer verification

<details>
<summary>Click to view Generated Reply vs Ground Truth</summary>

**Generated Reply:**
```text
Hi Caroline,

I understand the urgency of this request, and I am treating this with immediate priority.

Because Account Ownership grants root access to corporate communications, billing, and audit logs, we follow a strict security compliance verification protocol:

1. **Officer Authorization**: To satisfy security compliance requirements, please provide an email confirmation from a C-level executive or verified corporate legal officer from your verified domain.
2. **Alternative Fast Path (Expedited Enterprise Protocol)**: If your Google Workspace Super Admin approves via Google Admin SSO vouching, we can execute the transfer within 30 minutes under our expedited Enterprise protocol.

All existing shared mailboxes, tags, and analytics will be fully preserved without any downtime, tag loss, or data disruption.

Warm regards,
Hiver Enterprise Support Team
```

**Ground Truth Reference:**
```text
Hi Caroline,

Thank you for contacting Enterprise Support, and I can certainly facilitate this ownership transfer for your organization today.

Because Account Ownership grants root access to corporate communications, billing details, and audit records, we follow a strict verification protocol when the previous owner is unavailable:

1. **Authorized Officer Authorization**: We require an email confirmation from a C-level executive (CEO, CFO, COO) or verified corporate legal officer from your domain (`venturecapital.com`) confirming the ownership transfer to `caroline.foster@venturecapital.com`.
2. **Verification Form**: Please complete our 1-page expedited [Enterprise Ownership Transfer Affidavit] (attached) signed by an officer.

Alternatively, if your Google Workspace Super Admin can temporarily alias Jason's former address or approve via Google Admin SSO vouching, we can execute the transfer within 30 minutes.

Once received, our Security Compliance team will migrate primary ownership while preserving all existing shared inboxes, tags, templates, and analytics without any downtime. I am monitoring this thread continuously—please reply with the officer approval or let me know if your Google Super Admin can vouch!

Warm regards,
Hiver Enterprise Security Team
```
</details>

---

### Ticket: `TICK-114` (cancellation_refund)
- **Composite HEQI**: **92.06/100**
- **Sub-scores**: Policy: 100.0 | Intent: 85.0 | Tone: 100.0 | Actionability: 90.0 | Semantic: 73.05%
- **ROUGE-L**: 0.4797 | **BLEU**: 31.27
- **Strengths**: Strong policy adherence (4 required facts covered), Comprehensive intent coverage addressing customer questions, Excellent empathetic tone and de-escalation demeanor, Clear actionable steps and diagnostic instructions provided
- **Improvements**: None required

<details>
<summary>Click to view Generated Reply vs Ground Truth</summary>

**Generated Reply:**
```text
Hi Bradley,

Thank you for contacting Hiver Support, and I completely understand how frustrating this situation is for your team. Let's get this resolved right away.

Because your charge occurred just 0 days ago, your request falls squarely within our 14-day full refund guarantee.

I have taken the following actions immediately:
1. **Full Refund Processed**: Initiated a complete refund of $300.00 back to your original payment method. Please allow 3-5 business days for your bank to reflect the credited funds.
2. **Subscription Cancelled**: Cancelled your auto-renewal so no future charges will ever occur.

A formal credit note and receipt have been dispatched to your billing email.

Best regards,
Hiver Customer Support
```

**Ground Truth Reference:**
```text
Hi Bradley,

I understand your surprise and frustration seeing that $300 charge this morning, and I am glad to resolve this for you right away.

Because your trial converted only yesterday and you did not intend to continue, you are 100% eligible under our 14-day refund guarantee. 

I have taken the following actions immediately:
1. **Full Refund**: Processed a complete refund of $300.00 back to your original payment method. You should see this credit reflect in your account within 3-5 business days.
2. **Immediate Cancellation**: Cancelled your subscription and deactivated the workspace so no future automated charges will ever occur.

I also apologize if our automated 3-day trial expiration notice did not reach your primary inbox. A confirmation receipt for the $300 refund has been sent to your email. Thank you for giving Hiver a try, and I wish you and Urban Boutique all the best!

Warm regards,
Hiver Customer Support
```
</details>

---

### Ticket: `TICK-115` (sla_escalation)
- **Composite HEQI**: **80.32/100**
- **Sub-scores**: Policy: 75.0 | Intent: 85.0 | Tone: 95.0 | Actionability: 68.0 | Semantic: 73.74%
- **ROUGE-L**: 0.51 | **BLEU**: 27.34
- **Strengths**: Comprehensive intent coverage addressing customer questions, Excellent empathetic tone and de-escalation demeanor
- **Improvements**: Ensure all required policy terms and timelines are explicitly mentioned, Add numbered steps or explicit next actions to improve clarity

<details>
<summary>Click to view Generated Reply vs Ground Truth</summary>

**Generated Reply:**
```text
Hi Jessica,

I understand the urgency of this request, and I am treating this with immediate priority.

Here is your emergency live bridge right now: https://meet.google.com/hiv-ent-escalate

Our Lead On-Call Infrastructure Engineer and I are already in the meeting room.

Our engineers have applied a live query cache override to your mailbox queue, which is clearing the loading delay. Please have 1-2 reps perform a hard refresh (`Cmd + Shift + R`) right now. We will remain on the live bridge with you throughout the launch.

Warm regards,
Hiver Enterprise Support Team
```

**Ground Truth Reference:**
```text
Dear Jessica,

I am jumping on this immediately with top-tier priority. Here is your immediate emergency live bridge: https://meet.google.com/hiv-ent-escalate

I am already joined in that room along with our On-Call Lead Infrastructure Engineer, and we are ready to assist you right this second.

While you join, our backend monitoring confirms that our core API is operational, but your workspace experienced an un-indexed tag query spike caused by a bulk import earlier this afternoon. Our engineers have already applied an immediate query cache override to your mailbox (ACC-22910), which is flushing the hang.

Please have 1-2 reps do a hard refresh (`Cmd + Shift + R` or `Ctrl + Shift + R`) right now. We will verify stability together on the live Meet bridge and remain on standby with you throughout the entire 4:00 PM launch.

See you on the Meet bridge immediately,
Senior Enterprise Incident Commander
```
</details>

---

### Ticket: `TICK-116` (feature_request)
- **Composite HEQI**: **79.98/100**
- **Sub-scores**: Policy: 66.67 | Intent: 85.0 | Tone: 87.5 | Actionability: 86.0 | Semantic: 83.3%
- **ROUGE-L**: 0.6403 | **BLEU**: 41.21
- **Strengths**: Comprehensive intent coverage addressing customer questions, Excellent empathetic tone and de-escalation demeanor, Clear actionable steps and diagnostic instructions provided
- **Improvements**: Ensure all required policy terms and timelines are explicitly mentioned

<details>
<summary>Click to view Generated Reply vs Ground Truth</summary>

**Generated Reply:**
```text
Hi Danielle,

Thank you for getting in touch with Hiver Support! I am glad to assist you with this today.

Yes, absolutely! Hiver offers native mobile apps for both iOS and Android designed specifically for field teams.

With the Hiver app, your technicians can:
- View and assign shared inbox emails in real-time.
- Add internal notes to collaborate without emailing back and forth.
- Reply directly to clients using shared email templates.

Download links:
- **iOS**: Search 'Hiver: Shared Inbox' on the App Store or visit hiverhq.com/ios
- **Android**: Search 'Hiver' on Google Play or visit hiverhq.com/android

Technicians simply sign in with their Google Workspace credentials.

Best regards,
Hiver Customer Support
```

**Ground Truth Reference:**
```text
Hi Danielle,

Thank you for reaching out! Yes, absolutely—Hiver offers fully functional native mobile apps for both iOS and Android designed specifically for teams on the go.

With the Hiver mobile app, your field technicians can:
- View all shared inboxes and unassigned emails in real-time.
- Assign emails to themselves or other teammates.
- Add internal notes to collaborate without emailing back and forth.
- Reply directly to customers using shared email templates.

You can download the apps directly from:
- **Apple App Store (iOS)**: Search for 'Hiver: Shared Inbox' or visit hiverhq.com/ios
- **Google Play Store (Android)**: Search for 'Hiver' or visit hiverhq.com/android

Your technicians simply log in using their standard Google Workspace credentials. Once authenticated, all shared mailboxes will appear automatically. Let me know if you need help getting your team set up!

Best regards,
Hiver Mobile Team
```
</details>

---

### Ticket: `TICK-117` (onboarding)
- **Composite HEQI**: **85.57/100**
- **Sub-scores**: Policy: 100.0 | Intent: 56.67 | Tone: 97.5 | Actionability: 96.0 | Semantic: 75.04%
- **ROUGE-L**: 0.5441 | **BLEU**: 39.78
- **Strengths**: Strong policy adherence (3 required facts covered), Excellent empathetic tone and de-escalation demeanor, Clear actionable steps and diagnostic instructions provided
- **Improvements**: Did not fully address: Mention availability/out-of-office handling

<details>
<summary>Click to view Generated Reply vs Ground Truth</summary>

**Generated Reply:**
```text
Hi Arjun,

Thank you for reaching out! Happy to clarify this for you and guide you through the exact steps.

Automated round-robin distribution ensures fair workload balance and rapid response times.

Here is how to configure it in under 2 minutes:
1. Go to **Settings > Shared Mailboxes > [Your Mailbox]**.
2. Select the **Auto-Assignment** tab.
3. Toggle **Round-Robin Assignment** to **ON**.
4. Select the 8 eligible teammates for the rotation.
5. *(Recommended)*: Toggle **'Exclude teammates who are Out-of-Office or Offline'**.
6. Click **Save Changes**.

Let me know if you would like me to review your configuration once saved!

Best regards,
Hiver Customer Support
```

**Ground Truth Reference:**
```text
Hi Arjun,

Welcome to Hiver! Setting up automated round-robin distribution is one of the best ways to ensure fair workload balance and speed up first response times.

Here is how you can set up round-robin assignment in less than 2 minutes:

1. Log into your Hiver Admin panel and navigate to **Settings > Shared Mailboxes > 'help@fintechscale.io'**.
2. Click on the **Auto-Assignment** tab on the left.
3. Toggle **Round-Robin Assignment** to **ON**.
4. Under 'Eligible Teammates', select the 8 agents you want included in the rotation.
5. *(Optional but recommended)*: Toggle **'Exclude teammates who are Out-of-Office or Offline'** so unassigned tickets aren't routed to agents who are away.
6. Click **Save Changes**.

From that moment forward, every new incoming thread will automatically cycle to the next available agent in sequence.

Let me know if you would like me to review your setup once configured, and I'd be glad to take a look!

Warm regards,
Hiver Customer Onboarding
```
</details>

---

### Ticket: `TICK-118` (billing)
- **Composite HEQI**: **82.36/100**
- **Sub-scores**: Policy: 75.0 | Intent: 85.0 | Tone: 87.5 | Actionability: 93.0 | Semantic: 71.64%
- **ROUGE-L**: 0.5639 | **BLEU**: 35.79
- **Strengths**: Comprehensive intent coverage addressing customer questions, Excellent empathetic tone and de-escalation demeanor, Clear actionable steps and diagnostic instructions provided
- **Improvements**: Ensure all required policy terms and timelines are explicitly mentioned

<details>
<summary>Click to view Generated Reply vs Ground Truth</summary>

**Generated Reply:**
```text
Hi Sister,

Thank you for getting in touch with Hiver Support! I am glad to assist you with this today.

I have received your IRS 501(c)(3) determination letter and California state tax exemption certificate.

Here is what has been done:
1. **Tax Exemption Active**: Your account has been designated Tax-Exempt. All future invoices will be free of state sales tax.
2. **Sales Tax Refund Credited**: A refund of $7.88 for sales tax charged on your latest invoice has been credited to your card (settling in 3-5 days).
3. A revised tax-exempt invoice is now available in Settings > Billing > Invoices.

Best regards,
Hiver Customer Support
```

**Ground Truth Reference:**
```text
Dear Sister Mary Catherine,

Thank you for reaching out and for your important community work at the Hope Community Foundation!

I have received your IRS 501(c)(3) determination letter and California state tax exemption certificate. Here is what has been completed:

1. **Tax-Exempt Status Applied**: Our finance team has validated your certificate and flagged account ACC-61028 as officially Tax-Exempt. All future monthly invoices will be 100% free of sales tax.
2. **Sales Tax Refund Credited**: I have processed a direct credit of the $7.88 sales tax charged on your latest invoice back to your payment card (expected in 3-5 business days).
3. **Updated Invoices**: A revised zero-tax receipt for your August billing has been generated and is now accessible under Settings > Billing > Invoices.

Please let me know if you need anything further, and thank you for being a valued part of the Hiver community!

Warm regards,
Hiver Billing Operations
```
</details>

---

### Ticket: `TICK-119` (account_access)
- **Composite HEQI**: **80.61/100**
- **Sub-scores**: Policy: 66.67 | Intent: 85.0 | Tone: 95.0 | Actionability: 83.0 | Semantic: 79.08%
- **ROUGE-L**: 0.5833 | **BLEU**: 34.74
- **Strengths**: Comprehensive intent coverage addressing customer questions, Excellent empathetic tone and de-escalation demeanor, Clear actionable steps and diagnostic instructions provided
- **Improvements**: Ensure all required policy terms and timelines are explicitly mentioned

<details>
<summary>Click to view Generated Reply vs Ground Truth</summary>

**Generated Reply:**
```text
Hi Devin,

I understand the urgency of this request, and I am treating this with immediate priority.

The 'Audience URI mismatch' error occurs when the Entity ID inside Okta does not match Hiver's exact SP entity format.

Here is the exact fix for your Okta SAML configuration:
1. In Okta Admin Console > Hiver App > SAML Settings, set **Audience URI (SP Entity ID)** to:
   `https://hiverhq.com/saml/metadata/ACC-91204` (no trailing slash)
2. Set **Single Sign-On URL (ACS URL)** to:
   `https://hiverhq.com/saml/acs/ACC-91204`
3. Save changes in Okta and have a user test login in an incognito window.

I will remain active on this thread to verify successful authentication.

Warm regards,
Hiver Enterprise Support Team
```

**Ground Truth Reference:**
```text
Hi Devin,

Thank you for reaching out to Enterprise Support—I know how critical SSO rollout day is, and let's get your 60 reps authenticated immediately.

The 'Audience URI mismatch' error occurs when the Entity ID configured inside Okta does not match Hiver's exact SP (Service Provider) entity string format.

Here is how to fix this in Okta within 2 minutes:
1. Log into your **Okta Admin Console** and open your **Hiver SAML App** configuration.
2. Navigate to **General > SAML Settings > Edit**.
3. Check the field **Audience URI (SP Entity ID)**:
   - It should be set exactly to: `https://hiverhq.com/saml/metadata/ACC-91204` (case sensitive, no trailing slash).
4. Check the **Single Sign-On URL (ACS URL)**:
   - It must be: `https://hiverhq.com/saml/acs/ACC-91204`
5. Save changes in Okta.

Once saved, have one user test login in an incognito window. The assertion handshake will match immediately.

I will remain active on this ticket to monitor your team's successful logins. If you'd like our identity engineer on a screen share to double-check attributes, let me know!

Best regards,
Hiver Enterprise Identity Team
```
</details>

---

### Ticket: `TICK-120` (technical_issue)
- **Composite HEQI**: **85.73/100**
- **Sub-scores**: Policy: 75.0 | Intent: 85.0 | Tone: 100.0 | Actionability: 99.0 | Semantic: 71.27%
- **ROUGE-L**: 0.4762 | **BLEU**: 26.51
- **Strengths**: Comprehensive intent coverage addressing customer questions, Excellent empathetic tone and de-escalation demeanor, Clear actionable steps and diagnostic instructions provided
- **Improvements**: Ensure all required policy terms and timelines are explicitly mentioned

<details>
<summary>Click to view Generated Reply vs Ground Truth</summary>

**Generated Reply:**
```text
Hi Siddharth,

Thank you for contacting Hiver Support, and I completely understand how frustrating this situation is for your team. Let's get this resolved right away.

Browser-based exports of over 20,000 records frequently encounter HTTP browser timeout limits.

To ensure you have your full 12-month data ready for tomorrow morning's executive review, I have generated the export directly through our backend pipeline:
1. **Secure Download Link**: https://vault.hiverhq.com/exports/ACC-43901-FullExport.zip (valid for 72 hours).
2. The file contains all conversation records and tags, encrypted with AES-256 (decryption code sent to your registered mobile phone).

Please let me know once you download and verify the file!

Best regards,
Hiver Customer Support
```

**Ground Truth Reference:**
```text
Hi Siddharth,

Thank you for providing the volume context, and I completely understand why you need the complete 12-month dataset ready for tomorrow's executive review.

Browser-based exports over 20,000 records frequently encounter HTTP timeout limits imposed by local browser sessions. To spare you the tedious manual work of downloading month-by-month, I have generated the export directly through our backend data pipeline.

Here is what I've done:
1. Compiled your complete 12-month dataset (all 35,214 tickets with tags, resolution times, and agent notes) into an encrypted zip archive.
2. Uploaded it to our secure temporary download vault:
   **Download Link**: `https://vault.hiverhq.com/exports/ACC-43901-FY2026-FullExport.zip` *(link active for 72 hours)*.
3. The file is encrypted with AES-256; I have sent the one-time decryption key via SMS to your registered phone number.

Please verify that the file downloads smoothly and that all metrics align with your expectations. Best of luck with tomorrow's executive presentation!

Warm regards,
Hiver Technical Operations
```
</details>

---

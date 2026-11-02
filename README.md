# The Morning Distraction 🎙️

A free experimental daily original British audio podcast, written by **ChatGPT** and spoken by an offline **Piper** voice on GitHub Actions. **No Gemini, API key or payment card required.**

## The plan
1. An independent, scheduled ChatGPT task researches and writes a fresh 3,600–5,400 word episode into `episodes/YYYY-MM-DD.txt` using the connected GitHub app.
2. At 03:45 UTC GitHub Actions looks for today's script and synthesizes it to MP3 using Piper. Pushing the script also triggers the workflow.
3. A GitHub Release stores the audio, and GitHub Pages hosts a podcast feed.
4. Add `https://cooprush.github.io/morning-distraction/feed.xml` in AntennaPod on Android, and enable automatic downloading.

## One-time manual setting
Go to **Settings → Pages → Build and deployment** and select **GitHub Actions** as Source. No billing or secrets needed.

## Honest limitations
This is experimental and has **not yet produced a verified daily episode**. Scheduled ChatGPT tasks and GitHub Actions can run late or fail. A GitHub App's permissions can change. Piper voice quality is basic compared with premium TTS. The MP3 length is measured and recordings shorter than 25 minutes are rejected, rather than being misrepresented as 30 minutes. We will test the end-to-end pipeline before treating it as dependable.

The repository, generated scripts and podcast recordings are **public**. All content is about general entertainment tastes and verified public topics, without family, pupil, school, medical, financial or other personal data.

The existing 7am ChatGPT **Morning Listening Stack** continues to offer verified third-party listening suggestions as a fallback. This project is separate from that task.

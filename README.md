# Take-Home: URL Shortener API

**Time:** 2–3 hours. Using Claude / Copilot / Cursor is **encouraged**.

Build a small HTTP service that shortens URLs.

## Minimum requirements
- `POST /shorten` with `{"url": "https://..."}` returns a short code.
- `GET /{code}` redirects (HTTP 302) to the original URL.

That's the whole spec. We left it deliberately short.

## Notes
- A tiny Flask skeleton is in `app/` to save you boilerplate. Use it or replace it.
- Ship something running, with a short `NOTES.md` covering the decisions and trade-offs
  you made and what you'd do next with more time.

We're less interested in a feature-complete product than in *how you think about the parts
of the problem we didn't spell out.*

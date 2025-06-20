# The Fax Machine – Discord Bot
> A modular, self-updating Discord bot built in Python, originally hosted on Replit and now running locally on a Raspberry Pi 5.

Overview:
The Fax Machine began as a Replit-hosted utility bot but has since evolved into a self-hosted, always-on system using a Raspberry Pi 5. It checks this GitHub repository for updates and automatically applies them live—no manual restarts required.

### Features:

- Live update system pulling from GitHub
- Multi-token environment: production + test version always online
- In-progress configuration panel (currently ~80% done)
- Clean UI with detailed tooltips and explanations
- Easily customize features without touching code

### Development Workflow:
> Two versions of the bot are maintained:

- Production: Active on Discord, updated via this repo
- Development/Test: Local-only prototype using a second bot token for safe testing

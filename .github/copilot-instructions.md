<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

This project is a Python script that uses the `cloudflare-ddns` package to implement a custom DDNS provider compatible with Synology's custom DDNS protocol. The script should:
- Accept parameters for hostname, IP, username, and password (as required by Synology's DDNS custom provider format).
- Use the `cloudflare-ddns` package to update DNS records on Cloudflare.
- Be documented and easy to configure for Synology DSM custom DDNS integration.

import openai
import os

# Get your OpenAI API key from the environment (GitHub secret)
api_key = os.getenv('OPENAI_API_KEY')

# Your Google Ads code
GOOGLE_ADS = '''
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9524791500754717"
     crossorigin="anonymous"></script>
'''

# Your referral links
REFERRAL_LINKS = '''
<div class="platform-list">
  <h3>My Trusted Crypto Platforms</h3>
  <ul>
    <li><a href="https://accounts.binance.com/register?ref=C4VUXGQJ&utm_medium=web_share_copy" target="_blank">Binance – Best Overall</a></li>
    <li><a href="https://partner.bybit.com/b/81181" target="_blank">Bybit – Copy Trading & Derivatives</a></li>
    <li><a href="https://partner.bitget.com/bg/gpty4gc4" target="_blank">Bitget – Futures Pro Tools</a></li>
    <li><a href="https://www.okx.com/join/TRADELENSAI" target="_blank">OKX – Smart DeFi Trading</a></li>
    <li><a href="https://promote.mexc.com/a/cTMqmWi6" target="_blank">MEXC – Instant No-KYC Access</a></li>
  </ul>
</div>
'''

# Affiliate disclaimer
DISCLAIMER = '''
<p style="font-size: 0.9rem; color: #B7BDC6;">
  <strong>Disclaimer:</strong> This blog post contains affiliate links. If you sign up through these links, we may earn a small commission, which helps support our content.
</p>
'''

# Binance-inspired HTML template
def make_html(title, content):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  {GOOGLE_ADS}
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <style>
    body {{ background: #181A20; color: #EAECEF; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 800px; margin: auto; padding: 2rem; }}
    h1 {{ color: #F0B90B; }}
    a {{ color: #F0B90B; }}
    .button {{ background: #F0B90B; color: #181A20; padding: 1rem 2rem; border-radius: 8px; text-decoration: none; font-weight: bold; display: inline-block; margin: 2rem 0; }}
    .platform-list h3 {{ color: #F0B90B; }}
    .platform-list ul {{ list-style: none; padding: 0; }}
    .platform-list li {{ margin: 1rem 0; }}
    .platform-list a {{ color: #F0B90B; text-decoration: none; font-weight: bold; }}
  </style>
</head>
<body>
  <h1>{title}</h1>
  {content}
  {REFERRAL_LINKS}
  {DISCLAIMER}
  <a href="/index.html" class="button">← Back to Home</a>
  <footer style="margin-top:40px; color:#B7BDC6;">Powered by RJ & AI Dev Partner | Affiliate links may earn us a commission.</footer>
</body>
</html>
"""

# Function to generate a blog post using OpenAI (new API)
def generate_blog(topic):
    prompt = f"Write a detailed, original crypto blog post about: {topic}. Make it engaging, helpful, and beginner-friendly."
    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=900
    )
    return response.choices[0].message.content

# Main automation
def main():
    os.makedirs("blog", exist_ok=True)
    topic = "The Future of Bitcoin in 2025"
    title = topic
    content = generate_blog(topic)
    content_html = "<p>" + content.replace('\n', '</p><p>') + "</p>"
    html = make_html(title, content_html)
    filename = f"blog/ai-post-single.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated: {filename}")

if __name__ == "__main__":
    main()

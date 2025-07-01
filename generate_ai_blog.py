import os
import random
import itertools
import time
import subprocess
import openai

api_key = os.getenv('OPENAI_API_KEY')

GOOGLE_ADS = '''
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9524791500754717"
     crossorigin="anonymous"></script>
'''

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

DISCLAIMER = '''
<p style="font-size: 0.9rem; color: #B7BDC6;">
  <strong>Disclaimer:</strong> This blog post contains affiliate links. If you sign up through these links, we may earn a small commission, which helps support our content.
</p>
'''

TOPIC_FILE = "crypto_topics_10000.txt"

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

def generate_blog(topic):
    prompt = f"Write a detailed, original crypto blog post about: {topic}. Make it engaging, helpful, and beginner-friendly."
    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=900
    )
    return response.choices[0].message.content

def git_commit_and_push():
    try:
        subprocess.run(["git", "config", "user.name", "github-actions[bot]"], check=True)
        subprocess.run(["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"], check=True)
        subprocess.run(["git", "add", "blog/"], check=True)
        subprocess.run(["git", "commit", "-m", "Auto-generated 50 crypto blog posts"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("Changes committed and pushed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e}")
        print("Maybe no changes to commit or push.")

def generate_topic_list():
    subjects = [
        "Bitcoin", "Ethereum", "Altcoins", "NFTs", "DeFi", "Crypto Wallets", "Crypto Mining",
        "Stablecoins", "Smart Contracts", "Blockchain", "Crypto Exchanges", "Crypto Trading",
        "Crypto Security", "Crypto Taxes", "Crypto Regulations", "Crypto Scams", "Crypto Portfolio",
        "Crypto Lending", "Crypto Staking", "Crypto Airdrops", "Crypto Governance", "Crypto Gaming",
        "Crypto Privacy", "Crypto Charts", "Crypto Market", "Crypto Predictions", "Crypto Trends",
        "Crypto Adoption", "Crypto Technology", "Crypto Investing", "Crypto Education"
    ]

    actions = [
        "The Future of", "How to Use", "Top 10", "Understanding", "The Rise of", "The Impact of",
        "The Basics of", "How to Start", "The Benefits of", "The Challenges of", "The Role of",
        "How to Avoid", "How to Analyze", "The History of", "The Evolution of", "How to Secure",
        "How to Build", "How to Participate in", "The Importance of", "How to Spot", "The Best",
        "How to Get Started with", "The Growth of", "The Decline of", "The Potential of", "The Risks of"
    ]

    formats = [
        "in 2025", "for Beginners", "for Investors", "Explained", "Step-by-Step", "in the Crypto Market",
        "in Blockchain Technology", "in DeFi", "in NFTs", "in Crypto Trading", "in Crypto Mining",
        "in Crypto Security", "in Crypto Taxes", "in Crypto Regulations", "in Crypto Adoption",
        "in Crypto Education", "in Crypto Gaming", "in Crypto Lending", "in Crypto Staking"
    ]

    topics = set()
    for action, subject, fmt in itertools.product(actions, subjects, formats):
        topic = f"{action} {subject} {fmt}"
        topics.add(topic)

    with open(TOPIC_FILE, "w", encoding="utf-8") as f:
        for topic in sorted(topics):
            f.write(topic + "\n")

    print(f"Generated {len(topics)} unique crypto topics.")

def load_topics():
    if not os.path.exists(TOPIC_FILE):
        generate_topic_list()
    with open(TOPIC_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines()]

def main():
    os.makedirs("blog", exist_ok=True)
    topics = load_topics()
    random.shuffle(topics)
    daily_topics = topics[:50]  # 50 posts daily

    for i, topic in enumerate(daily_topics, 1):
        title = f"{topic} - Part {i}"
        print(f"Generating blog post {i}: {title}")
        content = generate_blog(topic)
        # Fix: replace newlines outside f-string to avoid syntax error
        content_html = "<p>" + content.replace('\n', '</p><p>') + "</p>"
        html = make_html(title, content_html)
        filename = f"blog/ai-post-{i}.html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Saved {filename}")
        time.sleep(28 * 60)  # 28 minutes delay between posts

    git_commit_and_push()

if __name__ == "__main__":
    main()

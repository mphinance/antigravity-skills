import os
import glob
import asyncio
import aiohttp
import yaml
import subprocess
from pathlib import Path

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
SKILLS_DIR = os.environ.get("SKILLS_DIR", "./skills")

WORKER_MODELS = ["x-ai/grok-4-fast", "deepseek/deepseek-v4-pro"]
MANAGER_MODEL = "anthropic/claude-sonnet-4.6"

async def call_openrouter(session, model, prompt, system="You are an expert AI skill auditor."):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ]
    }
    async with session.post(url, headers=headers, json=payload) as resp:
        if resp.status == 200:
            data = await resp.json()
            return data["choices"][0]["message"]["content"]
        else:
            return f"Error: {resp.status}"

def extract_skill_data(filepath):
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = yaml.safe_load(parts[1])
                return frontmatter.get('name', 'Unknown'), frontmatter.get('description', 'No description')
    except Exception:
        pass
    return Path(filepath).parent.name, "Unparsed"

async def process_chunk(session, chunk_id, skills_chunk):
    prompt = "Review these AI agent skills. Identify systemic patterns, overlapping functionality, or major missing gaps.\n\nSkills:\n"
    for name, desc in skills_chunk:
        prompt += f"- **{name}**: {desc}\n"
    tasks = [call_openrouter(session, model, prompt) for model in WORKER_MODELS]
    results = await asyncio.gather(*tasks)
    return {
        "chunk_id": chunk_id,
        "skills": [s[0] for s in skills_chunk],
        "reviews": dict(zip(WORKER_MODELS, results))
    }

async def main():
    if not OPENROUTER_API_KEY:
        print("No OPENROUTER_API_KEY found.")
        return

    skill_files = glob.glob(f"{SKILLS_DIR}/*/SKILL.md")
    all_skills = [extract_skill_data(f) for f in skill_files]
    chunks = [all_skills[i:i+10] for i in range(0, len(all_skills), 10)]
    
    async with aiohttp.ClientSession() as session:
        chunk_tasks = [process_chunk(session, i, c) for i, c in enumerate(chunks)]
        chunk_results = await asyncio.gather(*chunk_tasks)
        
        manager_prompt = "You are the Lead Oracle Architect. Your junior models have reviewed 111 AI skills in chunks and provided their analysis. Synthesize their findings into ONE ultimate Oracle prediction for the future of this repository.\n\nIdentify:\n1. The top 3 systemic gaps across the entire repository.\n2. The next major architectural evolution (The Future).\n3. Exactly 3 new high-leverage skills the user should build next.\n\nJunior Reports:\n"
        for res in chunk_results:
            manager_prompt += f"### Chunk {res['chunk_id']}\n"
            for model, review in res["reviews"].items():
                manager_prompt += f"**{model}** said:\n{review}\n\n"
                
        final_report = await call_openrouter(session, MANAGER_MODEL, manager_prompt, system="You are an expert CTO and Oracle.")
        
        with open("oracle_report.md", "w") as f:
            f.write(final_report)
            
        subprocess.run(["gh", "issue", "create", "--title", "🔮 Daily Oracle Prophecy: Ecosystem Audit", "--body-file", "oracle_report.md", "--label", "enhancement"])

if __name__ == "__main__":
    asyncio.run(main())

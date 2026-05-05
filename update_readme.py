import os
import glob
import re

def parse_skill_md(path):
    desc = ""
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        # Frontmatter is usually between ---
        match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
        if match:
            yaml = match.group(1)
            desc_match = re.search(r'description:\s*(.*?)(?=\n[a-z_]+:|$)', yaml, re.DOTALL | re.IGNORECASE)
            if desc_match:
                desc = desc_match.group(1).strip().replace('\n', ' ')
    if not desc:
        # Fallback to first non-empty line after frontmatter or just first line
        lines = content.split('\n')
        for l in lines:
            if not l.startswith('---') and not l.startswith('name:') and not l.startswith('description:') and l.strip() != '':
                desc = l.strip()
                break
                
    # Clean up yaml multiline markers and pipes
    if desc.startswith('|'):
        desc = desc[1:].strip()
    if desc.startswith('>'):
        desc = desc[1:].strip()
    desc = desc.replace('|', '-')
    return desc

def main():
    repo_dir = "/home/mph/Antigravity/tradier/ibkr/antigravity-skills"
    skills_dir = os.path.join(repo_dir, "skills")
    readme_path = os.path.join(repo_dir, "README.md")
    
    skills = []
    for skill_path in sorted(glob.glob(os.path.join(skills_dir, "*", "SKILL.md"))):
        skill_name = os.path.basename(os.path.dirname(skill_path))
        desc = parse_skill_md(skill_path)
        # Clean up description (remove quotes)
        if desc.startswith('"') and desc.endswith('"'):
            desc = desc[1:-1]
        elif desc.startswith("'") and desc.endswith("'"):
            desc = desc[1:-1]
            
        skills.append((skill_name, desc))
    
    # Generate markdown table
    md = "\n\n## 📚 Full Skills Directory\n\n"
    md += "A complete index of all available skills in this repository.\n\n"
    md += "| Skill | Description |\n"
    md += "|-------|-------------|\n"
    for name, desc in skills:
        md += f"| **[{name}](skills/{name}/)** | {desc} |\n"
        
    # Append to README
    with open(readme_path, 'a', encoding='utf-8') as f:
        f.write(md)
        
    print(f"Appended {len(skills)} skills to README.md")

if __name__ == '__main__':
    main()

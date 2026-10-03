import os
import math

out_dir = r"d:\github3d\assets"
os.makedirs(out_dir, exist_ok=True)

# Helper for standard SVG wrapper
def svg_wrap(width, height, content, bg=None):
    bg_rect = f'<rect width="100%" height="100%" fill="{bg}"/>' if bg else ''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" style="font-family: 'Segoe UI', system-ui, sans-serif;">
  <defs>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#0a192f" flood-opacity="0.15"/>
    </filter>
    <filter id="glow-cyan" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="6" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
    <filter id="glow-blue" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="6" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
    <linearGradient id="cloud-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#e2e8f0"/>
    </linearGradient>
    <linearGradient id="glass-dark" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="rgba(255,255,255,0.08)"/>
      <stop offset="100%" stop-color="rgba(255,255,255,0.02)"/>
    </linearGradient>
  </defs>
  {bg_rect}
  {content}
</svg>'''

# 1. Hero 3D (Light)
def gen_hero():
    content = '''
    <g transform="translate(50, 100)">
        <!-- 3D Cloud Center -->
        <g transform="translate(450, 50)">
            <ellipse cx="150" cy="150" rx="200" ry="80" fill="url(#cloud-grad)" filter="url(#shadow)"/>
            <ellipse cx="150" cy="140" rx="180" ry="70" fill="#f8fafc"/>
            
            <!-- Nodes -->
            <g transform="translate(150, 90)">
                <rect x="-40" y="-20" width="80" height="40" rx="8" fill="#0078d4" filter="url(#glow-blue)"/>
                <text x="0" y="5" fill="white" font-size="14" font-weight="bold" text-anchor="middle">AZURE</text>
            </g>
            
            <g transform="translate(40, 180)">
                <rect x="-40" y="-20" width="80" height="40" rx="8" fill="#326ce5"/>
                <text x="0" y="5" fill="white" font-size="14" font-weight="bold" text-anchor="middle">AKS</text>
            </g>
            
            <g transform="translate(150, 210)">
                <rect x="-40" y="-20" width="80" height="40" rx="8" fill="#8661c5"/>
                <text x="0" y="5" fill="white" font-size="14" font-weight="bold" text-anchor="middle">TERRAFORM</text>
            </g>
            
            <g transform="translate(260, 180)">
                <rect x="-40" y="-20" width="80" height="40" rx="8" fill="#00b294"/>
                <text x="0" y="5" fill="white" font-size="14" font-weight="bold" text-anchor="middle">MONITOR</text>
            </g>
            
            <g transform="translate(150, 150)">
                <rect x="-30" y="-15" width="60" height="30" rx="15" fill="#1e293b"/>
                <text x="0" y="4" fill="#00b7c3" font-size="10" font-weight="bold" text-anchor="middle">CI/CD</text>
            </g>
            
            <!-- Connections -->
            <path d="M 150 110 L 150 135 M 40 160 L 120 150 M 260 160 L 180 150 M 150 165 L 150 190" stroke="#0078d4" stroke-width="2" stroke-dasharray="4 4">
                <animate attributeName="stroke-dashoffset" values="8;0" dur="1s" repeatCount="indefinite"/>
            </path>
        </g>
    </g>
    '''
    return svg_wrap(900, 400, content)

# 2. About Dark Panel
def gen_about():
    content = '''
    <g transform="translate(50, 30)">
        <rect width="800" height="140" rx="16" fill="#0a192f" filter="url(#shadow)"/>
        <rect width="800" height="140" rx="16" fill="url(#glass-dark)" stroke="rgba(0,183,195,0.3)" stroke-width="1"/>
        <text x="40" y="45" fill="#00b7c3" font-size="14" font-weight="bold" letter-spacing="2">ABOUT ME</text>
        <text x="40" y="75" fill="#e2e8f0" font-size="16">I am an Azure DevOps Engineer with around 5.7 years of experience working with Azure cloud</text>
        <text x="40" y="95" fill="#e2e8f0" font-size="16">infrastructure, Infrastructure as Code, CI/CD automation and container platforms.</text>
        <text x="40" y="115" fill="#94a3b8" font-size="14">My work focuses on building reusable infrastructure with Terraform, automating deployments</text>
        <text x="40" y="135" fill="#94a3b8" font-size="14">through Azure DevOps, and working with Azure services, Kubernetes/AKS, security and monitoring.</text>
    </g>
    '''
    return svg_wrap(900, 200, content)

# 3. Pipeline Dark
def gen_pipeline():
    content = '''
    <rect width="100%" height="100%" fill="#0a192f"/>
    <text x="50" y="40" fill="#00b7c3" font-size="14" font-weight="bold" letter-spacing="2">DEVOPS PIPELINE</text>
    <g transform="translate(50, 80)">
        <path d="M 0 20 L 800 20" stroke="rgba(0,183,195,0.2)" stroke-width="4"/>
        <path d="M 0 20 L 800 20" stroke="#00b7c3" stroke-width="4" stroke-dasharray="800" stroke-dashoffset="800" filter="url(#glow-cyan)">
            <animate attributeName="stroke-dashoffset" values="800;0" dur="4s" repeatCount="indefinite"/>
        </path>
        
        <!-- Nodes -->
        <circle cx="0" cy="20" r="10" fill="#0078d4" filter="url(#glow-blue)"/>
        <text x="0" y="50" fill="white" font-size="12" text-anchor="middle">Dev</text>
        
        <circle cx="100" cy="20" r="10" fill="#0078d4"/>
        <text x="100" y="50" fill="white" font-size="12" text-anchor="middle">Git</text>
        
        <circle cx="200" cy="20" r="10" fill="#8661c5"/>
        <text x="200" y="50" fill="white" font-size="12" text-anchor="middle">Az DevOps</text>
        
        <circle cx="300" cy="20" r="10" fill="#eab308"/>
        <text x="300" y="50" fill="white" font-size="12" text-anchor="middle">SAST/IaC</text>
        
        <circle cx="400" cy="20" r="10" fill="#8661c5"/>
        <text x="400" y="50" fill="white" font-size="12" text-anchor="middle">TF Plan</text>
        
        <circle cx="500" cy="20" r="10" fill="#00b294"/>
        <text x="500" y="50" fill="white" font-size="12" text-anchor="middle">Approval</text>
        
        <circle cx="600" cy="20" r="10" fill="#8661c5"/>
        <text x="600" y="50" fill="white" font-size="12" text-anchor="middle">TF Apply</text>
        
        <circle cx="700" cy="20" r="10" fill="#0078d4"/>
        <text x="700" y="50" fill="white" font-size="12" text-anchor="middle">AKS</text>
        
        <circle cx="800" cy="20" r="10" fill="#00b7c3" filter="url(#glow-cyan)"/>
        <text x="800" y="50" fill="white" font-size="12" text-anchor="middle">Monitor</text>
    </g>
    '''
    return svg_wrap(900, 160, content)

# Generate and save
with open(os.path.join(out_dir, "hero-3d.svg"), "w") as f:
    f.write(gen_hero())
with open(os.path.join(out_dir, "about-dark.svg"), "w") as f:
    f.write(gen_about())
with open(os.path.join(out_dir, "pipeline-dark.svg"), "w") as f:
    f.write(gen_pipeline())

readme_content = """<div align="center">

<img src="./assets/hero-3d.svg" alt="Azure DevOps Engineering Control Center" width="900" />

<br><br>

<img src="./assets/about-dark.svg" alt="About Me" width="900" />

<br><br>

## ⚙️ TECHNOLOGY STACK

<img src="https://skillicons.dev/icons?i=azure,terraform,kubernetes,docker,git,linux,powershell,githubactions,react&perline=9" />

<br><br>

<img src="./assets/pipeline-dark.svg" alt="DevOps Pipeline" width="900" />

<br><br>

## 🚀 FEATURED ENGINEERING PROJECTS

<br>

### 01 — [Terraform Infrastructure](https://github.com/Raju089-ui/Terraform_infra)
**Terraform AKS Enterprise Infrastructure**  
Reusable Terraform modules for enterprise Azure AKS infrastructure including networking, NSGs, AKS, ACR, Key Vault, Log Analytics and Application Gateway.
<br>`Azure` `Terraform` `AKS` `ACR` `Key Vault` `Azure Monitor`

<hr>

### 02 — BharatNet / Telecom WAR-ROOM
**Azure DevOps Infrastructure**  
Azure-based application deployment and DevOps infrastructure for a large-scale telecom connectivity monitoring platform.
<br>`Azure` `App Service` `Front Door` `AKS` `Event Hub` `Cosmos DB`

<hr>

### 03 — [Azure Infrastructure Automation](https://github.com/Raju089-ui/Terraform-Azure-Lifecycle-Demo)
**Consistent Deployment Patterns**  
Reusable Terraform and Azure DevOps patterns for consistent infrastructure deployment across environments.
<br>`Terraform` `Azure DevOps` `CI/CD`

<br><br>

## 📈 GITHUB ACTIVITY

<img src="./assets/3d-contrib.svg" alt="3D GitHub Contributions" width="900"/>

<br><br>

<img src="https://github-readme-stats.vercel.app/api?username=Raju089-ui&show_icons=true&hide_border=true&bg_color=f5f9ff&title_color=0078d4&icon_color=00b7c3&text_color=1a3a5c&ring_color=0078d4" alt="GitHub Stats" height="180"/>
&nbsp;&nbsp;
<img src="https://github-readme-stats.vercel.app/api/top-langs/?username=Raju089-ui&layout=compact&hide_border=true&bg_color=f5f9ff&title_color=0078d4&text_color=1a3a5c" alt="Top Languages" height="180"/>

<br><br>

## 🎯 CURRENT FOCUS

☁ Advanced Azure &nbsp;&nbsp;|&nbsp;&nbsp; 🏗 Enterprise Terraform &nbsp;&nbsp;|&nbsp;&nbsp; ☸ Kubernetes / AKS &nbsp;&nbsp;|&nbsp;&nbsp; 🚀 CI/CD &nbsp;&nbsp;|&nbsp;&nbsp; 🔐 Cloud Security

<br><br>

<div align="center">
  <p><strong>BUILD • AUTOMATE • SECURE • OBSERVE</strong></p>
  <p><em>Azure • Terraform • DevOps • Kubernetes</em></p>
</div>

</div>
"""

with open(r"d:\github3d\README.md", "w", encoding="utf-8") as f:
    f.write(readme_content)

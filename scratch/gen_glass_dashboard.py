import math

out_file = r"d:\github3d\assets\glass-dashboard.svg"

width = 1200
height = 800

# Colors
glow_colors = ["#0078d4", "#8661c5", "#00b294", "#00b7c3", "#ff8c00"]

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" style="background:#0a0e17; font-family: 'Segoe UI', system-ui, sans-serif;">
  <defs>
    <!-- Background Blur Filters -->
    <filter id="bg-blur" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="60" />
    </filter>
    
    <!-- Neon Glows -->
    <filter id="glow-blue" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="8" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
    <filter id="glow-purple" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="8" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
    <filter id="glow-teal" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="8" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
    <filter id="glow-cyan" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="8" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>

    <linearGradient id="glass-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="rgba(255, 255, 255, 0.1)" />
      <stop offset="100%" stop-color="rgba(255, 255, 255, 0.02)" />
    </linearGradient>
  </defs>

  <!-- Abstract Blurred Background (Simulating Environment) -->
  <circle cx="200" cy="200" r="150" fill="#0078d4" opacity="0.3" filter="url(#bg-blur)" />
  <circle cx="1000" cy="150" r="200" fill="#5c2d91" opacity="0.2" filter="url(#bg-blur)" />
  <circle cx="600" cy="600" r="250" fill="#008272" opacity="0.2" filter="url(#bg-blur)" />
  <circle cx="100" cy="700" r="180" fill="#00b7c3" opacity="0.2" filter="url(#bg-blur)" />

  <!-- Dashboard Header -->
  <text x="50" y="60" fill="white" font-size="28" font-weight="600" letter-spacing="1">Dashboard</text>
  
  <!-- Right side icons (Menu, Settings, etc) -->
  <g transform="translate(1120, 40)" fill="rgba(255,255,255,0.6)">
    <circle cx="20" cy="0" r="15" fill="rgba(255,255,255,0.1)"/>
    <text x="20" y="5" text-anchor="middle" font-size="14">RS</text>
    
    <rect x="12" y="50" width="6" height="6" rx="1"/>
    <rect x="22" y="50" width="6" height="6" rx="1"/>
    <rect x="12" y="60" width="6" height="6" rx="1"/>
    <rect x="22" y="60" width="6" height="6" rx="1"/>
    
    <rect x="12" y="100" width="16" height="12" rx="2"/>
    <line x1="15" y1="104" x2="25" y2="104" stroke="rgba(255,255,255,0.6)" stroke-width="1.5"/>
    <line x1="15" y1="108" x2="20" y2="108" stroke="rgba(255,255,255,0.6)" stroke-width="1.5"/>
  </g>

'''

def create_panel(x, y, w, h, border_color="#334155", glow_filter=None):
    glow_attr = f'filter="url(#{glow_filter})"' if glow_filter else ''
    # The actual panel
    panel = f'''
    <g transform="translate({x}, {y})">
      <!-- Glow border behind -->
      <rect x="0" y="0" width="{w}" height="{h}" rx="16" fill="none" stroke="{border_color}" stroke-width="2" {glow_attr} opacity="0.8"/>
      <!-- Glass fill -->
      <rect x="0" y="0" width="{w}" height="{h}" rx="16" fill="url(#glass-gradient)" />
      <!-- Inner crisp border -->
      <rect x="0" y="0" width="{w}" height="{h}" rx="16" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="1" />
    </g>
    '''
    return panel

# Profile Panel (Top Left)
svg += create_panel(50, 100, 320, 340, "#0078d4", "glow-blue")
svg += '''
  <!-- Profile Content -->
  <g transform="translate(50, 100)">
    <circle cx="160" cy="110" r="65" fill="#1e293b" stroke="#0078d4" stroke-width="3"/>
    <text x="160" y="110" text-anchor="middle" fill="#0078d4" font-size="40" font-weight="bold" alignment-baseline="middle">RS</text>
    
    <text x="160" y="210" fill="white" font-size="24" font-weight="bold" text-anchor="middle">Raju089-ui</text>
    <text x="160" y="235" fill="rgba(255,255,255,0.6)" font-size="14" text-anchor="middle">Azure DevOps Engineer</text>
    
    <!-- Tags -->
    <rect x="180" y="20" width="120" height="22" rx="4" fill="rgba(0,120,212,0.2)" stroke="#0078d4" stroke-width="1"/>
    <text x="240" y="35" fill="#66b2ff" font-size="11" text-anchor="middle" font-weight="bold">Cloud Architect</text>
    
    <rect x="180" y="48" width="120" height="22" rx="4" fill="rgba(134,97,197,0.2)" stroke="#8661c5" stroke-width="1"/>
    <text x="240" y="63" fill="#c3a8ff" font-size="11" text-anchor="middle" font-weight="bold">Terraform Expert</text>
    
    <rect x="180" y="76" width="120" height="22" rx="4" fill="rgba(0,178,148,0.2)" stroke="#00b294" stroke-width="1"/>
    <text x="240" y="91" fill="#66ffe0" font-size="11" text-anchor="middle" font-weight="bold">K8s Administrator</text>
  </g>
'''

# Stats Panels (Top Middle & Right)
svg += create_panel(390, 100, 200, 100, "#00b7c3", "glow-cyan")
svg += '''
  <g transform="translate(390, 100)">
    <text x="20" y="30" fill="rgba(255,255,255,0.7)" font-size="14">Total Repos</text>
    <text x="20" y="80" fill="white" font-size="42" font-weight="bold">7</text>
    <text x="170" y="30" fill="rgba(255,255,255,0.5)" font-size="16">📂</text>
  </g>
'''

svg += create_panel(610, 100, 240, 100, "#8661c5", "glow-purple")
svg += '''
  <g transform="translate(610, 100)">
    <text x="20" y="30" fill="rgba(255,255,255,0.7)" font-size="14">Contributions (Year)</text>
    <text x="20" y="80" fill="white" font-size="42" font-weight="bold">842</text>
    <text x="210" y="30" fill="rgba(255,255,255,0.5)" font-size="16">📈</text>
  </g>
'''

svg += create_panel(870, 100, 200, 100, "#008272", "glow-teal")
svg += '''
  <g transform="translate(870, 100)">
    <text x="20" y="30" fill="rgba(255,255,255,0.7)" font-size="14">Followers</text>
    <text x="20" y="80" fill="white" font-size="42" font-weight="bold">2</text>
    <text x="170" y="30" fill="rgba(255,255,255,0.5)" font-size="16">👥</text>
  </g>
'''

# Activity Feed
svg += create_panel(390, 220, 680, 220, "#334155")
svg += '''
  <g transform="translate(390, 220)">
    <text x="20" y="35" fill="white" font-size="16" font-weight="bold">Recent Activity Feed</text>
    <line x1="20" y1="50" x2="660" y2="50" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>
    
    <text x="20" y="80" fill="#8661c5" font-size="14">⎇ Merged PR #42 to "Terraform_infra"</text>
    <text x="660" y="80" fill="rgba(255,255,255,0.4)" font-size="12" text-anchor="end">2h ago</text>
    
    <text x="20" y="115" fill="#8661c5" font-size="14">⎇ Merged PR #41 to "aks_infra"</text>
    <text x="660" y="115" fill="rgba(255,255,255,0.4)" font-size="12" text-anchor="end">5h ago</text>
    
    <text x="20" y="150" fill="#00b7c3" font-size="14">⟲ Committed to "k8s-supply-chain-lab"</text>
    <text x="660" y="150" fill="rgba(255,255,255,0.4)" font-size="12" text-anchor="end">1d ago</text>
    
    <text x="20" y="185" fill="#00b7c3" font-size="14">⟲ Committed to "Terraform-Azure-Lifecycle-Demo"</text>
    <text x="660" y="185" fill="rgba(255,255,255,0.4)" font-size="12" text-anchor="end">2d ago</text>
  </g>
'''

# Tech Stack Popularity (Bottom Left)
svg += create_panel(50, 460, 320, 300, "#334155")
def tech_box(x, y, w, h, name, color, icon):
    return f'''
    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="rgba(0,0,0,0.3)" stroke="{color}" stroke-width="1.5"/>
    <text x="{x+w/2}" y="{y+h/2-5}" fill="{color}" font-size="20" text-anchor="middle" font-family="sans-serif">{icon}</text>
    <text x="{x+w/2}" y="{y+h-10}" fill="rgba(255,255,255,0.8)" font-size="11" text-anchor="middle">{name}</text>
    '''

svg += f'''
  <g transform="translate(50, 460)">
    <text x="20" y="30" fill="white" font-size="16" font-weight="bold">Tech Stack Expertise (Top)</text>
    {tech_box(20, 50, 80, 80, "Azure", "#0078d4", "☁")}
    {tech_box(110, 50, 80, 80, "Terraform", "#8661c5", "⬢")}
    {tech_box(200, 50, 100, 80, "Kubernetes", "#326ce5", "⎈")}
    
    {tech_box(20, 140, 120, 80, "Docker", "#00b7c3", "⬡")}
    {tech_box(150, 140, 70, 80, "CI/CD", "#008272", "⟲")}
    {tech_box(230, 140, 70, 40, "Bash", "#ffffff", "🐚")}
    {tech_box(230, 190, 70, 30, "PS", "#5391fe", "❯_")}
    
    <text x="20" y="255" fill="rgba(255,255,255,0.6)" font-size="12">Primary focus: Azure Cloud & DevOps. Extensive</text>
    <text x="20" y="275" fill="rgba(255,255,255,0.6)" font-size="12">IaC, Security, and Container proficiency.</text>
  </g>
'''

# Infrastructure Distribution (Pie Chart) (Bottom Middle)
svg += create_panel(390, 460, 270, 300, "#334155")
# Simple SVG pie chart approximation
svg += '''
  <g transform="translate(390, 460)">
    <text x="20" y="30" fill="white" font-size="16" font-weight="bold">Infrastructure Targets</text>
    
    <!-- Pie Chart -->
    <g transform="translate(135, 140)">
      <circle r="70" fill="transparent" stroke="#0078d4" stroke-width="40" stroke-dasharray="220 220" /> <!-- AKS 50% -->
      <circle r="70" fill="transparent" stroke="#8661c5" stroke-width="40" stroke-dasharray="110 330" stroke-dashoffset="-220" /> <!-- VNet/NSG 25% -->
      <circle r="70" fill="transparent" stroke="#00b294" stroke-width="40" stroke-dasharray="66 374" stroke-dashoffset="-330" /> <!-- Key Vault 15% -->
      <circle r="70" fill="transparent" stroke="#ff8c00" stroke-width="40" stroke-dasharray="44 396" stroke-dashoffset="-396" /> <!-- App Gateway 10% -->
      
      <circle r="50" fill="#1e293b"/>
      <text x="0" y="5" fill="white" font-size="14" font-weight="bold" text-anchor="middle">Azure</text>
    </g>
    
    <!-- Labels -->
    <text x="60" y="110" fill="#0078d4" font-size="12" font-weight="bold">50% AKS</text>
    <text x="220" y="110" fill="#8661c5" font-size="12" font-weight="bold">25% VNet</text>
    <text x="60" y="200" fill="#00b294" font-size="12" font-weight="bold">15% Security</text>
    <text x="220" y="200" fill="#ff8c00" font-size="12" font-weight="bold">10% Traffic</text>
    
    <text x="20" y="255" fill="rgba(255,255,255,0.6)" font-size="12">Azure environment targets for</text>
    <text x="20" y="275" fill="rgba(255,255,255,0.6)" font-size="12">deployment and security tasks.</text>
  </g>
'''

# Project Velocity (Bar/Line Chart) (Bottom Right)
svg += create_panel(680, 460, 390, 300, "#334155")
svg += '''
  <g transform="translate(680, 460)">
    <text x="20" y="30" fill="white" font-size="16" font-weight="bold">Deployment Velocity</text>
    <rect x="260" y="15" width="110" height="24" rx="12" fill="rgba(255,255,255,0.1)"/>
    <text x="315" y="31" fill="rgba(255,255,255,0.7)" font-size="11" text-anchor="middle">Weekly Commits</text>
    
    <!-- Grid lines -->
    <line x1="40" y1="70" x2="350" y2="70" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>
    <text x="30" y="74" fill="rgba(255,255,255,0.4)" font-size="10" text-anchor="end">40</text>
    
    <line x1="40" y1="110" x2="350" y2="110" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>
    <text x="30" y="114" fill="rgba(255,255,255,0.4)" font-size="10" text-anchor="end">30</text>
    
    <line x1="40" y1="150" x2="350" y2="150" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>
    <text x="30" y="154" fill="rgba(255,255,255,0.4)" font-size="10" text-anchor="end">20</text>
    
    <line x1="40" y1="190" x2="350" y2="190" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>
    <text x="30" y="194" fill="rgba(255,255,255,0.4)" font-size="10" text-anchor="end">10</text>
    
    <line x1="40" y1="230" x2="350" y2="230" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>
    <text x="30" y="234" fill="rgba(255,255,255,0.4)" font-size="10" text-anchor="end">0</text>
    
    <!-- Bars -->
    <rect x="50" y="180" width="20" height="50" fill="url(#glass-gradient)" stroke="#8661c5" stroke-width="1"/>
    <rect x="90" y="160" width="20" height="70" fill="url(#glass-gradient)" stroke="#8661c5" stroke-width="1"/>
    <rect x="130" y="130" width="20" height="100" fill="url(#glass-gradient)" stroke="#8661c5" stroke-width="1"/>
    <rect x="170" y="140" width="20" height="90" fill="url(#glass-gradient)" stroke="#8661c5" stroke-width="1"/>
    <rect x="210" y="100" width="20" height="130" fill="url(#glass-gradient)" stroke="#8661c5" stroke-width="1"/>
    <rect x="250" y="180" width="20" height="50" fill="url(#glass-gradient)" stroke="#8661c5" stroke-width="1"/>
    <rect x="290" y="90" width="20" height="140" fill="url(#glass-gradient)" stroke="#8661c5" stroke-width="1"/>
    <rect x="330" y="150" width="20" height="80" fill="url(#glass-gradient)" stroke="#8661c5" stroke-width="1"/>
    
    <!-- Line Graph (Velocity Trend) -->
    <polyline points="60,200 100,140 140,110 180,150 220,70 260,190 300,80 340,160" fill="none" stroke="#00b7c3" stroke-width="3" filter="url(#glow-cyan)"/>
    
    <text x="20" y="270" fill="rgba(255,255,255,0.6)" font-size="12">Active development focus on Cloud Infrastructure,</text>
    <text x="20" y="285" fill="rgba(255,255,255,0.6)" font-size="12">DevOps pipelines, and Security validation.</text>
    
    <!-- "Export" Popover (Decorative) -->
    <g transform="translate(240, 160)">
      <rect x="0" y="0" width="130" height="90" rx="8" fill="rgba(15,23,42,0.9)" stroke="#00b7c3" stroke-width="1" filter="url(#glow-cyan)"/>
      <text x="10" y="20" fill="white" font-size="12" font-weight="bold">Export &amp; Share</text>
      <line x1="0" y1="30" x2="130" y2="30" stroke="rgba(255,255,255,0.1)"/>
      
      <text x="10" y="50" fill="rgba(255,255,255,0.8)" font-size="12">CSV</text>
      <text x="110" y="50" fill="rgba(255,255,255,0.5)" font-size="12">⤓</text>
      
      <text x="10" y="75" fill="rgba(255,255,255,0.8)" font-size="12">Project Report</text>
      <text x="110" y="75" fill="rgba(255,255,255,0.5)" font-size="12">⤤</text>
    </g>
  </g>
'''

svg += '</svg>'

with open(out_file, "w", encoding="utf-8") as f:
    f.write(svg)

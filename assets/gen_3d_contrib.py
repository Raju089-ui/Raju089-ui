import random

out_file = r"d:\github3d\assets\3d-contrib.svg"

colors = {
    0: {"top": "#eaf3fe", "left": "#d8e7fc", "right": "#c6daf8"},
    1: {"top": "#99c9f5", "left": "#7ab4ea", "right": "#5a9fdc"},
    2: {"top": "#4eb0f0", "left": "#2d98de", "right": "#1882c5"},
    3: {"top": "#0078d4", "left": "#006cbd", "right": "#005a9e"},
    4: {"top": "#005a9e", "left": "#004882", "right": "#003867"},
}

grid_cols = 16
grid_rows = 7

tile_w = 16
tile_h = 8
z_scale = 8

svg_width = 800
svg_height = 240
offset_x = svg_width / 2
offset_y = 60

svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}">
  <defs>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#0a3d6e" flood-opacity="0.15"/>
    </filter>
  </defs>
  <rect width="100%" height="100%" rx="16" fill="#f5f9ff"/>
  <text x="400" y="30" text-anchor="middle" font-family="Segoe UI, sans-serif" font-size="12" font-weight="700" fill="#1a3a5c" letter-spacing="4" opacity="0.6">GITHUB CONTRIBUTION ACTIVITY</text>
  <g transform="translate({offset_x}, {offset_y})">
'''

blocks = []
for c in range(grid_cols):
    for r in range(grid_rows):
        val = random.choices([0, 1, 2, 3, 4], weights=[0.5, 0.2, 0.15, 0.1, 0.05])[0]
        if (c+r)%5 == 0: val = min(4, val+1)
        if c > 8 and r > 3: val = random.choices([2,3,4], weights=[0.3, 0.5, 0.2])[0]
        if c == 13: val = 0
        blocks.append((c, r, val))

blocks.sort(key=lambda b: b[0] + b[1])

for b in blocks:
    c, r, val = b
    x = (c - r) * tile_w
    y = (c + r) * tile_h
    
    z = val * z_scale
    if val == 0: z = 2
        
    c_top = colors[val]["top"]
    c_left = colors[val]["left"]
    c_right = colors[val]["right"]
    
    p_top = f"{x},{y-z} {x+tile_w},{y+tile_h-z} {x},{y+tile_h*2-z} {x-tile_w},{y+tile_h-z}"
    p_left = f"{x-tile_w},{y+tile_h-z} {x},{y+tile_h*2-z} {x},{y+tile_h*2} {x-tile_w},{y+tile_h}"
    p_right = f"{x},{y+tile_h*2-z} {x+tile_w},{y+tile_h-z} {x+tile_w},{y+tile_h} {x},{y+tile_h*2}"
    
    filter_attr = ' filter="url(#shadow)"' if z > 4 else ''
    
    svg_content += f'    <g{filter_attr}>\n'
    if z > 0:
        svg_content += f'      <polygon points="{p_left}" fill="{c_left}"/>\n'
        svg_content += f'      <polygon points="{p_right}" fill="{c_right}"/>\n'
    svg_content += f'      <polygon points="{p_top}" fill="{c_top}"/>\n'
    svg_content += f'    </g>\n'

svg_content += '''  </g>
</svg>'''

with open(out_file, "w") as f:
    f.write(svg_content)

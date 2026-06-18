from PIL import Image, ImageDraw, ImageFont
import math

# Create a larger image for the flow diagram
width = 1600
height = 2000
image = Image.new('RGB', (width, height), color='white')
draw = ImageDraw.Draw(image)

# Colors
TITLE_COLOR = (0, 51, 102)
START_COLOR = (76, 175, 80)  # Green
PROCESS_COLOR = (68, 114, 196)  # Blue
DECISION_COLOR = (255, 193, 7)  # Yellow
DATABASE_COLOR = (244, 67, 54)  # Red
END_COLOR = (76, 175, 80)  # Green
ARROW_COLOR = (64, 64, 64)  # Dark gray

# Fonts
try:
    title_font = ImageFont.truetype("arial.ttf", 20)
    section_font = ImageFont.truetype("arial.ttf", 16)
    text_font = ImageFont.truetype("arial.ttf", 12)
    small_font = ImageFont.truetype("arial.ttf", 10)
except:
    title_font = ImageFont.load_default()
    section_font = ImageFont.load_default()
    text_font = ImageFont.load_default()
    small_font = ImageFont.load_default()

def draw_box(x, y, width, height, text, color, text_color=(255, 255, 255)):
    """Draw a rounded rectangle box"""
    draw.rectangle([x, y, x + width, y + height], fill=color, outline=ARROW_COLOR, width=2)
    # Draw text
    bbox = draw.textbbox((0, 0), text, font=text_font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = x + (width - text_width) // 2
    text_y = y + (height - text_height) // 2
    draw.text((text_x, text_y), text, fill=text_color, font=text_font)

def draw_diamond(x, y, size, text, color):
    """Draw a diamond shape for decisions"""
    points = [
        (x + size, y),  # Top
        (x + size * 2, y + size),  # Right
        (x + size, y + size * 2),  # Bottom
        (x, y + size)  # Left
    ]
    draw.polygon(points, fill=color, outline=ARROW_COLOR)
    bbox = draw.textbbox((0, 0), text, font=small_font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = x + size - text_width // 2
    text_y = y + size - text_height // 2
    draw.text((text_x, text_y), text, fill=(0, 0, 0), font=small_font)

def draw_arrow(x1, y1, x2, y2, label=""):
    """Draw an arrow between points"""
    draw.line([(x1, y1), (x2, y2)], fill=ARROW_COLOR, width=2)
    # Draw arrowhead
    angle = math.atan2(y2 - y1, x2 - x1)
    arrow_size = 10
    arrow_x1 = x2 - arrow_size * math.cos(angle - math.pi/6)
    arrow_y1 = y2 - arrow_size * math.sin(angle - math.pi/6)
    arrow_x2 = x2 - arrow_size * math.cos(angle + math.pi/6)
    arrow_y2 = y2 - arrow_size * math.sin(angle + math.pi/6)
    draw.polygon([(x2, y2), (arrow_x1, arrow_y1), (arrow_x2, arrow_y2)], fill=ARROW_COLOR)
    
    # Draw label if provided
    if label:
        label_x = (x1 + x2) // 2 + 10
        label_y = (y1 + y2) // 2 - 10
        draw.text((label_x, label_y), label, fill=ARROW_COLOR, font=small_font)

def draw_database(x, y, width, height, text):
    """Draw a database cylinder"""
    # Draw top rectangle
    draw.rectangle([x, y, x + width, y + height//3], fill=DATABASE_COLOR, outline=ARROW_COLOR, width=2)
    # Draw bottom rectangle
    draw.rectangle([x, y + height*2//3, x + width, y + height], fill=DATABASE_COLOR, outline=ARROW_COLOR, width=2)
    # Draw middle lines
    draw.rectangle([x, y + height//3, x + width, y + height*2//3], fill=DATABASE_COLOR, outline=ARROW_COLOR, width=2)
    
    # Draw text
    text_y = y + height // 2 - 10
    bbox = draw.textbbox((0, 0), text, font=text_font)
    text_width = bbox[2] - bbox[0]
    text_x = x + (width - text_width) // 2
    draw.text((text_x, text_y), text, fill=(255, 255, 255), font=text_font)

# Title
y_pos = 30
draw.text((350, y_pos), 'TaskBoard Lite - Application Flow Diagram', fill=TITLE_COLOR, font=title_font)
y_pos += 60

# ===== MAIN FLOW =====
draw.text((50, y_pos), 'MAIN APPLICATION FLOW', fill=TITLE_COLOR, font=section_font)
y_pos += 40

# Start
draw_box(600, y_pos, 200, 50, 'User Visits App', START_COLOR)
draw_arrow(700, y_pos + 50, 700, y_pos + 80)
y_pos += 90

# Check Authentication
draw_diamond(580, y_pos, 60, 'Logged In?', DECISION_COLOR)
draw_arrow(580, y_pos + 60, 400, y_pos + 120)
draw_arrow(700, y_pos + 120, 900, y_pos + 120)
draw.text((500, y_pos + 75), 'No', fill=ARROW_COLOR, font=small_font)
draw.text((780, y_pos + 75), 'Yes', fill=ARROW_COLOR, font=small_font)
y_pos += 130

# Left branch - Login/Register
draw_box(250, y_pos, 200, 50, 'Login/Register Page', PROCESS_COLOR, (255, 255, 255))
draw_box(700, y_pos, 200, 50, 'Dashboard', PROCESS_COLOR, (255, 255, 255))
y_pos += 70

# Login flow
draw_arrow(350, y_pos - 20, 350, y_pos + 10)
draw_box(250, y_pos, 200, 50, 'Enter Credentials', PROCESS_COLOR)
draw_arrow(350, y_pos + 50, 350, y_pos + 80)
draw.text((350, y_pos + 85), 'API: POST /auth/login', fill=ARROW_COLOR, font=small_font)
draw.text((350, y_pos + 105), 'or /auth/register', fill=ARROW_COLOR, font=small_font)
y_pos += 140

# Database check
draw_database(250, y_pos, 200, 80, 'Database')
draw_arrow(350, y_pos - 20, 350, y_pos)
draw_arrow(350, y_pos + 80, 350, y_pos + 110)
y_pos += 150

# JWT Token
draw_box(250, y_pos, 200, 50, 'Generate JWT Token', PROCESS_COLOR)
draw_arrow(350, y_pos + 50, 350, y_pos + 80)
y_pos += 90

# Right branch - Dashboard features
draw_arrow(800, y_pos - 250, 800, y_pos - 100)
draw_box(700, y_pos - 100, 200, 50, 'Boards List', PROCESS_COLOR)
draw_arrow(800, y_pos - 50, 800, y_pos + 10)
y_pos += 30

draw.text((50, y_pos), 'BOARD OPERATIONS', fill=TITLE_COLOR, font=section_font)
y_pos += 40

# Board options
draw_box(600, y_pos, 150, 45, 'View Board', PROCESS_COLOR)
draw_box(800, y_pos, 150, 45, 'Create Board', PROCESS_COLOR)
y_pos += 60

draw_arrow(675, y_pos - 15, 675, y_pos + 10)
draw_arrow(875, y_pos - 15, 875, y_pos + 10)

draw_box(600, y_pos, 150, 45, 'Board View', PROCESS_COLOR)
draw_box(800, y_pos, 150, 45, 'Board Form', PROCESS_COLOR)
y_pos += 60

draw_arrow(675, y_pos - 15, 675, y_pos + 10)
draw_arrow(875, y_pos - 15, 875, y_pos + 10)

draw.text((50, y_pos), 'TASK OPERATIONS', fill=TITLE_COLOR, font=section_font)
y_pos += 40

draw_box(500, y_pos, 140, 45, 'View Tasks', PROCESS_COLOR)
draw_box(680, y_pos, 140, 45, 'Add Task', PROCESS_COLOR)
draw_box(860, y_pos, 140, 45, 'Edit Task', PROCESS_COLOR)
y_pos += 60

draw_arrow(570, y_pos - 15, 570, y_pos + 10)
draw_arrow(750, y_pos - 15, 750, y_pos + 10)
draw_arrow(930, y_pos - 15, 930, y_pos + 10)

draw_box(500, y_pos, 140, 45, 'Task List', PROCESS_COLOR)
draw_box(680, y_pos, 140, 45, 'New Task Form', PROCESS_COLOR)
draw_box(860, y_pos, 140, 45, 'Edit Form', PROCESS_COLOR)
y_pos += 60

draw_arrow(570, y_pos - 15, 570, y_pos + 10)
draw_arrow(750, y_pos - 15, 750, y_pos + 10)
draw_arrow(930, y_pos - 15, 930, y_pos + 10)

draw.text((50, y_pos), 'DRAG & DROP INTERACTION', fill=TITLE_COLOR, font=section_font)
y_pos += 40

draw_box(550, y_pos, 200, 50, 'Drag Task Between Columns', PROCESS_COLOR)
draw_arrow(650, y_pos + 50, 650, y_pos + 80)
y_pos += 90

draw_box(550, y_pos, 200, 50, 'Update Task Status', PROCESS_COLOR)
draw.text((550, y_pos + 65), 'API: PUT /tasks/{task_id}', fill=ARROW_COLOR, font=small_font)
draw_arrow(650, y_pos + 50, 650, y_pos + 80)
y_pos += 110

draw_database(550, y_pos, 200, 80, 'Update Database')
draw_arrow(650, y_pos + 80, 650, y_pos + 110)
y_pos += 140

draw_box(550, y_pos, 200, 50, 'Refresh Task Display', PROCESS_COLOR)
draw_arrow(650, y_pos + 50, 650, y_pos + 80)
y_pos += 90

draw_box(550, y_pos, 200, 50, 'End', END_COLOR)

# ===== API LAYER (Right side) =====
api_x = 1150
draw.text((api_x, 90), 'API LAYER', fill=TITLE_COLOR, font=section_font)

api_endpoints = [
    'POST /auth/register',
    'POST /auth/login',
    'GET /auth/me',
    'GET /boards',
    'POST /boards',
    'GET /boards/{id}',
    'PUT /boards/{id}',
    'DELETE /boards/{id}',
    'GET /boards/{id}/tasks',
    'POST /boards/{id}/tasks',
    'GET /tasks/{id}',
    'PUT /tasks/{id}',
    'DELETE /tasks/{id}'
]

api_y = 140
for i, endpoint in enumerate(api_endpoints):
    color = (68, 114, 196) if i < 3 else (144, 202, 249) if i < 8 else (173, 216, 230)
    draw.rectangle([api_x, api_y + i*35, api_x + 280, api_y + i*35 + 30], 
                   fill=color, outline=ARROW_COLOR, width=1)
    draw.text((api_x + 10, api_y + i*35 + 5), endpoint, fill=(255, 255, 255), font=small_font)

# ===== DATABASE SCHEMA (Bottom right) =====
db_x = 1150
db_y = 1050

draw.text((db_x, db_y), 'DATABASE SCHEMA', fill=TITLE_COLOR, font=section_font)
db_y += 50

schemas = [
    ('Users', ['id', 'email', 'username', 'password_hash', 'created_at']),
    ('Boards', ['id', 'user_id (FK)', 'title', 'description', 'created_at']),
    ('Tasks', ['id', 'board_id (FK)', 'title', 'status', 'position', 'created_at'])
]

for title_sch, fields in schemas:
    draw.rectangle([db_x, db_y, db_x + 250, db_y + 30], 
                   fill=DATABASE_COLOR, outline=ARROW_COLOR, width=2)
    draw.text((db_x + 10, db_y + 5), title_sch, fill=(255, 255, 255), font=text_font)
    db_y += 35
    
    for field in fields:
        draw.rectangle([db_x, db_y, db_x + 250, db_y + 25], 
                       fill=(245, 245, 245), outline=(200, 200, 200), width=1)
        draw.text((db_x + 10, db_y + 3), field, fill=(0, 0, 0), font=small_font)
        db_y += 25
    
    db_y += 15

# Legend
legend_y = 1600
draw.text((50, legend_y), 'LEGEND:', fill=TITLE_COLOR, font=section_font)

legend_items = [
    (50, legend_y + 40, START_COLOR, 'Start/End'),
    (250, legend_y + 40, PROCESS_COLOR, 'Process/Operation'),
    (500, legend_y + 40, DECISION_COLOR, 'Decision'),
    (750, legend_y + 40, DATABASE_COLOR, 'Database'),
]

for x, y, color, label in legend_items:
    draw.rectangle([x, y, x + 30, y + 30], fill=color, outline=ARROW_COLOR, width=1)
    draw.text((x + 40, y + 5), label, fill=(0, 0, 0), font=text_font)

# Notes
notes_y = 1700
draw.text((50, notes_y), 'KEY FLOWS:', fill=TITLE_COLOR, font=section_font)

notes = [
    '1. Authentication: User registers/logs in → JWT token generated → Access dashboard',
    '2. Board Management: Create/view/edit boards → Stored in database with user_id',
    '3. Task Management: Create/view/edit tasks → Displayed in Kanban columns',
    '4. Drag & Drop: Move task between columns → API updates status → Database persists change'
]

for i, note in enumerate(notes):
    draw.text((50, notes_y + 35 + i*30), note, fill=(0, 0, 0), font=text_font)

# Save image
output_path = 'TaskBoard_Lite_Flow_Diagram.png'
image.save(output_path)
print(f'✓ Flow diagram created: {output_path}')

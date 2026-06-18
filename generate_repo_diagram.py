from PIL import Image, ImageDraw, ImageFont
import textwrap

# Create a new image with white background
width = 1200
height = 1600
image = Image.new('RGB', (width, height), color='white')
draw = ImageDraw.Draw(image)

# Try to use a monospace font, fallback to default
try:
    title_font = ImageFont.truetype("arial.ttf", 24)
    heading_font = ImageFont.truetype("arial.ttf", 16)
    text_font = ImageFont.truetype("consolas.ttf", 12)
except:
    title_font = ImageFont.load_default()
    heading_font = ImageFont.load_default()
    text_font = ImageFont.load_default()

# Colors
TITLE_COLOR = (0, 51, 102)
HEADING_COLOR = (68, 114, 196)
FOLDER_COLOR = (255, 140, 0)
FILE_COLOR = (64, 64, 64)
BACKEND_COLOR = (100, 149, 237)
FRONTEND_COLOR = (144, 238, 144)

# Title
y_pos = 30
draw.text((30, y_pos), "TaskBoard Lite - Repository Structure", fill=TITLE_COLOR, font=title_font)
y_pos += 50

# Draw the tree structure
def draw_line(text, indent=0, color=FILE_COLOR, is_folder=False):
    global y_pos
    prefix = "  " * indent
    if is_folder:
        prefix += "📁 "
    else:
        prefix += "  "
    draw.text((30 + indent * 20, y_pos), prefix + text, fill=color, font=text_font)
    y_pos += 25
    return y_pos

# Root
draw_line("taskboard-lite/", 0, FOLDER_COLOR, True)

# Backend
draw_line("backend/", 1, BACKEND_COLOR, True)
draw_line("main.py", 2, FILE_COLOR)
draw_line("database.py", 2, FILE_COLOR)
draw_line("models.py", 2, FILE_COLOR)
draw_line("schemas.py", 2, FILE_COLOR)
draw_line("auth.py", 2, FILE_COLOR)
draw_line("cache.py", 2, FILE_COLOR)
draw_line("conftest.py", 2, FILE_COLOR)
draw_line("requirements.txt", 2, FILE_COLOR)
draw_line("README.md", 2, FILE_COLOR)
draw_line("taskboard.db", 2, FILE_COLOR)
draw_line("routers/", 2, BACKEND_COLOR, True)
draw_line("auth.py", 3, FILE_COLOR)
draw_line("boards.py", 3, FILE_COLOR)
draw_line("tasks.py", 3, FILE_COLOR)
draw_line("stats.py", 3, FILE_COLOR)
draw_line("__init__.py", 3, FILE_COLOR)

y_pos += 10

# Frontend
draw_line("frontend/", 1, FRONTEND_COLOR, True)
draw_line("index.html", 2, FILE_COLOR)
draw_line("boards.html", 2, FILE_COLOR)
draw_line("board.html", 2, FILE_COLOR)
draw_line("stats.html", 2, FILE_COLOR)
draw_line("css/", 2, FRONTEND_COLOR, True)
draw_line("style.css", 3, FILE_COLOR)
draw_line("js/", 2, FRONTEND_COLOR, True)
draw_line("api.js", 3, FILE_COLOR)

y_pos += 10

# Documentation & Config
draw_line("generate_business_spec.py", 1, FILE_COLOR)
draw_line("TaskBoard_Lite_Business_Specification.docx", 1, FILE_COLOR)
draw_line(".git/", 1, FOLDER_COLOR, True)

# Add legend
y_pos += 30
draw.text((30, y_pos), "Legend:", fill=HEADING_COLOR, font=heading_font)
y_pos += 35

draw.text((30, y_pos), "Backend Components:", fill=BACKEND_COLOR, font=heading_font)
y_pos += 25
draw.text((50, y_pos), "• main.py - FastAPI application entry point", fill=FILE_COLOR, font=text_font)
y_pos += 22
draw.text((50, y_pos), "• database.py - SQLAlchemy database configuration", fill=FILE_COLOR, font=text_font)
y_pos += 22
draw.text((50, y_pos), "• models.py - SQLAlchemy ORM models (User, Board, Task)", fill=FILE_COLOR, font=text_font)
y_pos += 22
draw.text((50, y_pos), "• schemas.py - Pydantic request/response schemas", fill=FILE_COLOR, font=text_font)
y_pos += 22
draw.text((50, y_pos), "• routers/ - API route handlers (auth, boards, tasks, stats)", fill=FILE_COLOR, font=text_font)

y_pos += 35
draw.text((30, y_pos), "Frontend Components:", fill=FRONTEND_COLOR, font=heading_font)
y_pos += 25
draw.text((50, y_pos), "• *.html - HTML pages (index, boards, board, stats)", fill=FILE_COLOR, font=text_font)
y_pos += 22
draw.text((50, y_pos), "• css/ - Stylesheets (style.css)", fill=FILE_COLOR, font=text_font)
y_pos += 22
draw.text((50, y_pos), "• js/ - JavaScript files (api.js for API communication)", fill=FILE_COLOR, font=text_font)

# Save image
output_path = 'TaskBoard_Lite_Repository_Structure.png'
image.save(output_path)
print(f'✓ Repository structure diagram created: {output_path}')

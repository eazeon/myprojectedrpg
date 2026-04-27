import tkinter as tk

# ═════════════════════════════════════════════════════════════════════════════
# COLOR PALETTES
# ═════════════════════════════════════════════════════════════════════════════

# Main background colors
COLOR_BACKGROUND_DARK = "#0a0a0a"
COLOR_BACKGROUND_DARKER = "#181a20"
COLOR_BACKGROUND_VERY_DARK = "#0d0d0d"

# Header and title colors
COLOR_HEADER_BG = "#1a0f2e"
COLOR_HEADER_ACCENT = "#ffd700"

# Stats bar colors
COLOR_STATS_BG = "#1a1a1a"
COLOR_STATS_BORDER = "#1a1a1a"

# Light background colors for windows
COLOR_LIGHT_BG = "#fff9ec"
COLOR_LIGHT_BG_BLUE = "#eef7ff"
COLOR_LIGHT_BG_SOFT = "#fffaf0"
COLOR_LIGHT_BG_CREAM = "#f9f5ec"
COLOR_LIGHT_BG_LIGHT = "#f1f1f1"

# Text colors
COLOR_TEXT_GOLD = "#ffed4e"
COLOR_TEXT_BRIGHT = "#eeeeee"
COLOR_TEXT_MUTED = "#cccccc"
COLOR_TEXT_DARK_GRAY = "#a0a0a0"
COLOR_TEXT_GREEN = "#00ff99"
COLOR_TEXT_RED = "#ff5555"
COLOR_TEXT_BLUE_BRIGHT = "#44ccff"
COLOR_TEXT_YELLOW = "#ffaa00"

# Combat window colors
COLOR_COMBAT_BG = "#23272e"
COLOR_COMBAT_STATUS_BG = "#181a20"
COLOR_COMBAT_GREEN = "#00ff99"
COLOR_COMBAT_RED = "#ff5555"
COLOR_COMBAT_GRAY = "#cccccc"

# Border and frame colors
COLOR_BORDER_GOLD = "#8b6f47"
COLOR_BORDER_DARK = "#660000"
COLOR_BORDER_BLUE = "#0066cc"
COLOR_BORDER_GRAY = "#444444"

# Merchant colors
COLOR_MERCHANT_BG = "#8b5a00"

# Player section colors
COLOR_PLAYER_SECTION_BG = "#0a1a2a"
COLOR_PLAYER_ACCENT = "#4da6ff"

# Combat/Adventure colors
COLOR_COMBAT_SECTION_BG = "#2a0a0a"
COLOR_COMBAT_ACCENT = "#ff6b6b"

# Options section colors
COLOR_OPTIONS_SECTION_BG = "#1a1a2a"
COLOR_OPTIONS_ACCENT = "#888888"

# Magic colors
COLOR_MAGIC_ACCENT = "#663399"

# Button colors map
BUTTON_COLORS = {
    "merchant": "#8b5a00",
    "player": "#004a8f",
    "combat": "#8b0000",
    "magic": "#663399",
    "neutral": "#444444",
    "danger": "#b32222"
}

# ═════════════════════════════════════════════════════════════════════════════
# FONT DEFINITIONS
# ═════════════════════════════════════════════════════════════════════════════

# Title fonts
FONT_TITLE_MAIN = ("Courier", 36, "bold")
FONT_TITLE_LARGE = ("Courier", 12, "bold")
FONT_DECORATIVE_SMALL = ("Courier", 9)
FONT_VERSION = ("Courier", 10, "italic")

# Window fonts
FONT_WINDOW_TITLE = ("Verdana", 14, "bold")
FONT_WINDOW_HEADER = ("Verdana", 12, "bold")
FONT_WINDOW_BODY = ("Verdana", 12)
FONT_WINDOW_SMALL = ("Verdana", 11)
FONT_WINDOW_TINY = ("Verdana", 10)
FONT_WINDOW_ITALIC = ("Verdana", 10, "italic")

# Label fonts
FONT_LABEL_BOLD = ("Verdana", 11, "bold")
FONT_LABEL_NORMAL = ("Verdana", 11)
FONT_LABEL_SMALL = ("Verdana", 10)

# Button fonts
FONT_BUTTON_BOLD = ("Courier", 9, "bold")
FONT_BUTTON_LARGE = ("Verdana", 16, "bold")
FONT_BUTTON_NORMAL = ("Verdana", 13, "bold")
FONT_BUTTON_SMALL = ("Verdana", 9)

# Combat fonts
FONT_COMBAT_TITLE = ("Verdana", 16, "bold")
FONT_COMBAT_NORMAL = ("Verdana", 12)
FONT_COMBAT_SMALL = ("Verdana", 11)
FONT_COMBAT_TINY = ("Verdana", 10)
FONT_COMBAT_CODE = ("Consolas", 11)

# Floating text font
FONT_FLOATING = ("Verdana", 14, "bold")

# ═════════════════════════════════════════════════════════════════════════════
# WINDOW SIZES
# ═════════════════════════════════════════════════════════════════════════════

# Main window
WINDOW_WIDTH_MAIN = 1200
WINDOW_HEIGHT_MAIN = 900

# Popup windows
WINDOW_WIDTH_INVENTORY = 900
WINDOW_HEIGHT_INVENTORY = 800

WINDOW_WIDTH_SKILLS = 1000
WINDOW_HEIGHT_SKILLS = 700

WINDOW_WIDTH_MAP = 900
WINDOW_HEIGHT_MAP = 700

WINDOW_WIDTH_QUESTS = 800
WINDOW_HEIGHT_QUESTS = 600

WINDOW_WIDTH_QUEST_DIALOGUE = 600
WINDOW_HEIGHT_QUEST_DIALOGUE = 400

WINDOW_WIDTH_QUEST_RESULT = 600
WINDOW_HEIGHT_QUEST_RESULT = 450

WINDOW_WIDTH_COMBAT = 1100
WINDOW_HEIGHT_COMBAT = 700

WINDOW_WIDTH_UPGRADE = 420
WINDOW_HEIGHT_UPGRADE = 500

WINDOW_WIDTH_SHOP = 600
WINDOW_HEIGHT_SHOP = 500

# ═════════════════════════════════════════════════════════════════════════════
# HEADER DIMENSIONS
# ═════════════════════════════════════════════════════════════════════════════

HEADER_HEIGHT = 140
STATS_BAR_HEIGHT = 60
FOOTER_HEIGHT = 40
BORDER_HEIGHT = 3

# ═════════════════════════════════════════════════════════════════════════════
# PADDING AND SPACING
# ═════════════════════════════════════════════════════════════════════════════

PADDING_NORMAL = 10
PADDING_SMALL = 5
PADDING_LARGE = 20

PADY_NORMAL = 10
PADY_SMALL = 5
PADY_LARGE = 20

# ═════════════════════════════════════════════════════════════════════════════
# DECORATIVE CHARACTERS AND SYMBOLS
# ═════════════════════════════════════════════════════════════════════════════

DECORATIVE_HORIZONTAL = "═══════════════════════════════════"
DECORATIVE_HORIZONTAL_SMALL = "━━━━━━━━━━━━━━━━━━━━━━━━"
DECORATIVE_SWORD = "⚔️"
DECORATIVE_DIVIDER = "│"

# ═════════════════════════════════════════════════════════════════════════════
# STYLING FUNCTIONS
# ═════════════════════════════════════════════════════════════════════════════


def styled_frame(parent, title, bg_color, border_color, accent_color="#ffd700"):
    """
    Create a stylized frame with border and decorative elements.
    
    Args:
        parent: Parent tkinter widget
        title: Title text for the frame
        bg_color: Background color of the frame
        border_color: Border/outer frame color
        accent_color: Color for decorative elements (default: gold)
    
    Returns:
        The inner frame ready for adding widgets
    """
    # Outer frame for border effect
    outer = tk.Frame(parent, bg=border_color, relief=tk.RAISED, bd=3)
    outer.pack(side=tk.LEFT, padx=8, pady=8, fill=tk.BOTH, expand=True)
    
    # Inner frame with actual content
    inner = tk.Frame(outer, bg=bg_color, padx=12, pady=12)
    inner.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
    
    # Top decorative line
    top_line = tk.Label(inner, text=DECORATIVE_HORIZONTAL_SMALL, 
                       font=FONT_DECORATIVE_SMALL, fg=accent_color, bg=bg_color)
    top_line.pack(pady=(0, 8))
    
    # Title with fancy styling
    title_label = tk.Label(inner, text=title, font=FONT_TITLE_LARGE, 
                          fg=accent_color, bg=bg_color)
    title_label.pack(pady=(0, 10))
    
    # Bottom decorative line
    bottom_line = tk.Label(inner, text=DECORATIVE_HORIZONTAL_SMALL, 
                          font=FONT_DECORATIVE_SMALL, fg=accent_color, bg=bg_color)
    bottom_line.pack(pady=(0, 12))
    
    return inner


def create_button(parent, text, command, color="neutral"):
    """
    Create a styled button with consistent appearance.
    
    Args:
        parent: Parent tkinter widget
        text: Button text
        command: Command to execute on click
        color: Button color type (merchant, player, combat, magic, neutral, danger)
    
    Returns:
        The created button widget
    """
    btn = tk.Button(parent, 
                   text=text, 
                   font=FONT_BUTTON_BOLD,
                   bg=BUTTON_COLORS.get(color, BUTTON_COLORS["neutral"]),
                   fg="#ffffff",
                   activebackground="#ffdd00",
                   activeforeground="#000000",
                   relief=tk.RAISED,
                   bd=2,
                   padx=10,
                   pady=10,
                   highlightthickness=1,
                   highlightbackground="#666666",
                   command=command)
    btn.pack(pady=7, fill=tk.X, expand=False)
    
    # Add hover effects
    def on_enter(event):
        btn.config(bd=3, relief=tk.SUNKEN)
    
    def on_leave(event):
        btn.config(bd=2, relief=tk.RAISED)
    
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    
    return btn


def create_progress_bar(parent, label_text, color, max_value=100, width=200, height=20):
    """
    Create a progress bar with label.
    
    Args:
        parent: Parent tkinter widget
        label_text: Label for the bar
        color: Color of the progress bar
        max_value: Maximum value for the bar
        width: Width of the bar canvas
        height: Height of the bar canvas
    
    Returns:
        Tuple of (canvas, bar_rectangle, value_label, bar_width)
    """
    container = tk.Frame(parent, bg="#23272e")
    container.pack(pady=5)
    
    label = tk.Label(container, text=label_text, font=FONT_WINDOW_SMALL, 
                     fg=color, bg="#23272e")
    label.pack(side=tk.LEFT, padx=5)
    
    bar_width = max(200, int(max_value * 1.5))
    canvas = tk.Canvas(container, width=bar_width, height=height, 
                       bg="#181a20", highlightthickness=0)
    canvas.pack(side=tk.LEFT)
    
    bar = canvas.create_rectangle(0, 0, bar_width, height, fill=color)
    
    value_label = tk.Label(container, text=f"{max_value}/{max_value}", 
                          font=FONT_WINDOW_SMALL, fg="#cccccc", bg="#23272e")
    value_label.pack(side=tk.LEFT, padx=5)
    
    return canvas, bar, value_label, bar_width

from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        # Header: Project Name on top right
        self.set_font('Arial', 'I', 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, 'FDIAS: Real-Time Intrusion Alert System', 0, 0, 'R')
        self.ln(15)

    def footer(self):
        # Footer: Page Number
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def slide_title(self, title):
        # Standardized Title Format
        self.set_font('Arial', 'B', 22)
        self.set_text_color(0, 51, 102)  # Navy Blue
        self.cell(0, 10, title, 0, 1, 'L')
        self.set_draw_color(0, 204, 102) # Green Accent
        self.set_line_width(1)
        self.line(10, self.get_y(), 287, self.get_y())
        self.ln(10)

    def content_pane_left(self, points):
        # Text on Left
        self.set_y(45)
        self.set_font('Arial', '', 12)
        self.set_text_color(0)
        for point in points:
            self.multi_cell(130, 8, chr(149) + " " + point)
            self.ln(2)

    def content_pane_right(self, points):
        # Text on Right
        self.set_y(45)
        self.set_left_margin(150)
        self.set_font('Arial', '', 12)
        self.set_text_color(0)
        for point in points:
            self.multi_cell(130, 8, chr(149) + " " + point)
            self.ln(2)
        self.set_left_margin(10) # Reset

    def visual_placeholder(self, x, y, w, h, label, description):
        # Draws a placeholder for diagrams
        self.set_fill_color(240, 240, 240)
        self.set_draw_color(100)
        self.set_line_width(0.5)
        self.rect(x, y, w, h, 'DF')
        
        self.set_xy(x, y + (h/2) - 5)
        self.set_font('Arial', 'B', 10)
        self.set_text_color(80, 80, 80)
        self.cell(w, 5, f"[ VISUAL: {label} ]", 0, 1, 'C')
        
        self.set_xy(x, y + (h/2) + 2)
        self.set_font('Arial', 'I', 9)
        self.cell(w, 5, f"({description})", 0, 1, 'C')

# Initialize PDF (Landscape, mm, A4)
pdf = PDF(orientation='L', unit='mm', format='A4')
pdf.set_auto_page_break(auto=True, margin=15)

# --- SLIDE 1: TITLE (Source Page 1) ---
pdf.add_page()
pdf.ln(40)
pdf.set_font('Arial', 'B', 32)
pdf.set_text_color(0, 51, 102)
pdf.cell(0, 15, 'FDIAS', 0, 1, 'C')
pdf.set_font('Arial', 'B', 18)
pdf.cell(0, 15, 'Real-Time Face Detection Intrusion Alert System', 0, 1, 'C')
pdf.set_font('Arial', '', 14)
pdf.cell(0, 10, 'Using Hybrid AI Models (YOLOv8 + DeepFace)', 0, 1, 'C')
pdf.ln(20)
pdf.set_font('Arial', 'I', 11)
pdf.set_text_color(100)
pdf.cell(0, 10, 'Presented by: [Your Name] | Dept. of Computer Science & Engineering', 0, 1, 'C')
pdf.cell(0, 10, 'November 2025', 0, 1, 'C')

# --- SLIDE 2: MOTIVATION (Source Page 2) ---
pdf.add_page()
pdf.slide_title("Introduction & Motivation")
points = [
    "Need for physical safeguarding in an era where security is paramount.",
    "Traditional surveillance has limitations in real-time monitoring.",
    "Growing concern over unauthorized access in restricted areas.",
    "Challenge: Delay in threat identification leads to breaches.",
    "Solution: FDIAS uses a hybrid AI approach for instant detection."
]
pdf.content_pane_left(points)
pdf.visual_placeholder(150, 50, 130, 100, "Security Context", "Img: Security Camera / Restricted Area Sign")

# --- SLIDE 3: OBJECTIVES (Source Page 3) ---
pdf.add_page()
pdf.slide_title("Core Objectives & Key Features")
points = [
    "Real-time Face Detection: High-speed detection using YOLOv8.",
    "Hybrid AI Processing: Lightweight detection + Heavy recognition (Facenet512).",
    "Detect Unauthorized Access: Immediate identification of unknowns.",
    "Instant Alerts: Dispatch notifications via Telegram API.",
    "Multi-Process Architecture: Non-blocking design for smooth video."
]
pdf.content_pane_right(points)
pdf.visual_placeholder(10, 50, 130, 100, "Features Diagram", "Icon Grid: Speed, AI Brain, Telegram, Shield")

# --- SLIDE 4: TECH STACK (Source Page 5) ---
pdf.add_page()
pdf.slide_title("Core Technology Stack")
points = [
    "OpenCV: The system's 'eyes'. Captures video via cv2.VideoCapture(0).",
    "YOLOv8: High-speed detection (yolov8n-face.onnx). purely for finding faces.",
    "DeepFace: Handles recognition using Facenet512 embeddings.",
    "pyTelegramBotAPI: Connects to Telegram Bot to send alerts/images.",
    "Python: The backbone language integrating all libraries."
]
pdf.content_pane_left(points)
pdf.visual_placeholder(150, 50, 130, 100, "Tech Stack Logos", "Logos: OpenCV, YOLO, DeepFace, Python")

# --- SLIDE 5: TWO-STAGE PIPELINE (Source Page 6) ---
pdf.add_page()
pdf.slide_title("Hybrid AI: Two-Stage Processing")
points = [
    "Stage 1: Detection (YOLOv8)",
    "   - Rapid processing with minimal latency.",
    "   - Outputs bounding box coordinates.",
    "   - Purely for detection, not identification.",
    "Stage 2: Recognition (Facenet512)",
    "   - Converts face to 512-d vector embedding.",
    "   - Compares using Euclidean L2 distance.",
    "   - Ensures high frame rate while performing detailed recognition."
]
pdf.content_pane_right(points)
pdf.visual_placeholder(10, 50, 130, 100, "Processing Pipeline", "Flow: Video -> YOLO Box -> Cropped Face -> Vector")

# --- SLIDE 6: ARCHITECTURE (Source Page 7) ---
pdf.add_page()
pdf.slide_title("Multi-Process Architecture")
points = [
    "Main Process (camera.py):",
    "   - Lightweight video capture.",
    "   - Runs fast YOLOv8 model.",
    "   - Keeps video stream flowing smoothly.",
    "Subprocess (monitor.py):",
    "   - Handles computationally intensive DeepFace tasks.",
    "   - Compares embeddings against database.",
    "   - Prevents video lag/freezing."
]
pdf.content_pane_left(points)
pdf.visual_placeholder(150, 50, 130, 100, "Architecture Diagram", "Two blocks (Camera/Monitor) connected by queue")

# --- SLIDE 7: WORKFLOW (Source Page 8) ---
pdf.add_page()
pdf.slide_title("Implementation Workflow")
points = [
    "1. Video Capture: Webcam feed accessed.",
    "2. Face Detection: YOLOv8 finds face coordinates.",
    "3. Image Cropping: Facial region extracted.",
    "4. Subprocess Init: Sent to monitor.py.",
    "5. Recognition: Converted to 512-d embedding.",
    "6. Database Comparison: Checked against authorized users.",
    "7. Intrusion Alert: Flagged if distance > threshold.",
    "8. Dispatch: Telegram sends Image + ID + Time."
]
pdf.content_pane_right(points)
pdf.visual_placeholder(10, 50, 130, 100, "Workflow Step-by-Step", "Circular or Linear Flowchart 1 through 8")

# --- SLIDE 8: ALERT SYSTEM (Source Page 9) ---
pdf.add_page()
pdf.slide_title("Alert System & Database")
points = [
    "Telegram Integration:",
    "   - Sends immediate notification to Administrator.",
    "   - Payload: Timestamp, Tracking ID, Captured Image.",
    "Database Management:",
    "   - 'Faces' directory stores authorized personnel.",
    "   - Pre-computed embeddings for faster comparison.",
    "Logic: Unknown faces trigger the bot immediately."
]
pdf.content_pane_left(points)
pdf.visual_placeholder(150, 50, 130, 100, "Mobile Alert Mockup", "Screenshot of Telegram Chat with Alert")

# --- SLIDE 9: CONCLUSION (Source Page 10) ---
pdf.add_page()
pdf.slide_title("Conclusion & Future Scope")
points = [
    "Conclusion:",
    "   - Successful integration of Hybrid AI (Speed + Accuracy).",
    "   - Cost-effective, efficient security solution.",
    "Future Enhancements:",
    "   - Multi-camera support for broader coverage.",
    "   - Cloud integration for centralized databases.",
    "   - Optimization for low-light environments.",
    "   - Edge deployment (Raspberry Pi/Jetson Nano)."
]
pdf.content_pane_right(points)
pdf.visual_placeholder(10, 50, 130, 100, "Growth & Future", "Icons: Cloud, Multiple Cameras, Edge Chip")

# Output
pdf.output('FDIAS_Project_Presentation.pdf')
print("PDF Generated: FDIAS_Project_Presentation.pdf")

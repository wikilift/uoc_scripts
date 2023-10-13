from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Assembly Program Execution Output", 0, 1, "C")

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")
    def chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, 0, 1)
        self.ln(5)
    
    def chapter_body_dict(self, body:dict):
        self.set_font("Arial", "", 12)
        for line,v in body.items():
            self.cell(0, 10, f"{line}:{str(hex(v)).upper().zfill(8)}", ln=True)
        self.ln(5)


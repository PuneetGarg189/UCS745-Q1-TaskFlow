from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports" / "ucs745_lab_assignment_puneet_garg.docx"
DESKTOP = Path("/Users/puneetgarg/Desktop")
BLUE = "1F4E79"
LIGHT_BLUE = "D9EAF7"
GRID = "D9D9D9"


def set_cell_shading(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)


def set_cell_border(cell, color=GRID):
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = tc_pr.first_child_found_in("w:tcBorders")
    if borders is None:
        borders = OxmlElement("w:tcBorders")
        tc_pr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        tag = qn(f"w:{edge}")
        el = borders.find(tag)
        if el is None:
            el = OxmlElement(f"w:{edge}")
            borders.append(el)
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "6")
        el.set(qn("w:color"), color)


def set_cell_text(cell, value, bold=False, color=None, size=9.5):
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run(value)
    run.bold = bold
    run.font.size = Pt(size)
    if color:
        run.font.color.rgb = RGBColor.from_string(color)
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    set_cell_border(cell)


def repeat_table_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    header = OxmlElement("w:tblHeader")
    header.set(qn("w:val"), "true")
    tr_pr.append(header)


def add_table(doc, headers, rows, widths=None):
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"
    for index, header in enumerate(headers):
        cell = table.rows[0].cells[index]
        set_cell_shading(cell, BLUE)
        set_cell_text(cell, header, bold=True, color="FFFFFF")
        if widths:
            cell.width = Inches(widths[index])
    repeat_table_header(table.rows[0])
    for row_index, row in enumerate(rows):
        cells = table.add_row().cells
        for index, value in enumerate(row):
            if row_index % 2:
                set_cell_shading(cells[index], "F5F9FC")
            set_cell_text(cells[index], value)
            if widths:
                cells[index].width = Inches(widths[index])
    doc.add_paragraph().paragraph_format.space_after = Pt(3)
    return table


def style_document(doc):
    section = doc.sections[0]
    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.7)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)
    styles = doc.styles
    styles["Normal"].font.name = "Aptos"
    styles["Normal"].font.size = Pt(10.5)
    styles["Normal"].paragraph_format.space_after = Pt(6)
    styles["Title"].font.name = "Aptos Display"
    styles["Title"].font.size = Pt(24)
    styles["Title"].font.bold = True
    styles["Title"].font.color.rgb = RGBColor(0, 0, 0)
    for name, size in (("Heading 1", 16), ("Heading 2", 13), ("Heading 3", 11)):
        styles[name].font.name = "Aptos"
        styles[name].font.size = Pt(size)
        styles[name].font.bold = True
        styles[name].font.color.rgb = RGBColor(0, 0, 0)
        styles[name].paragraph_format.space_before = Pt(12)
        styles[name].paragraph_format.space_after = Pt(5)


def p(doc, text="", bold_prefix=None, italic=False):
    paragraph = doc.add_paragraph()
    if bold_prefix and text.startswith(bold_prefix):
        lead = paragraph.add_run(bold_prefix)
        lead.bold = True
        paragraph.add_run(text[len(bold_prefix):])
    else:
        run = paragraph.add_run(text)
        run.italic = italic
    return paragraph


def bullet(doc, text):
    paragraph = doc.add_paragraph(style="List Bullet")
    paragraph.add_run(text)


def code(doc, text):
    paragraph = doc.add_paragraph()
    paragraph.paragraph_format.left_indent = Inches(0.18)
    paragraph.paragraph_format.space_before = Pt(3)
    paragraph.paragraph_format.space_after = Pt(4)
    run = paragraph.add_run(text)
    run.font.name = "Courier New"
    run.font.size = Pt(8.6)
    shading = OxmlElement("w:shd")
    shading.set(qn("w:fill"), "F2F2F2")
    paragraph._p.get_or_add_pPr().append(shading)


def figure(doc, filename, caption):
    image = DESKTOP / filename
    if image.exists():
        paragraph = doc.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        paragraph.add_run().add_picture(str(image), width=Inches(6.55))
        caption_p = doc.add_paragraph()
        caption_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = caption_p.add_run(caption)
        run.italic = True
        run.font.size = Pt(9)


def heading(doc, label):
    doc.add_heading(label, level=1)


def main():
    OUT.parent.mkdir(exist_ok=True)
    doc = Document()
    style_document(doc)

    cover = doc.add_paragraph(style="Title")
    cover.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cover.add_run("UCS745 Cloud and DevOps\nLab Assignment")
    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle.add_run("Git and GitHub, SDLC Design, and Amazon Linux Administration").italic = True
    doc.add_paragraph()
    metadata = [
        ("Name", "Puneet Garg"),
        ("Roll No.", "102303189"),
        ("GitHub", "https://github.com/PuneetGarg189"),
        ("Q1 repository", "https://github.com/PuneetGarg189/UCS745-Q1-TaskFlow"),
    ]
    table = doc.add_table(rows=0, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for label, value in metadata:
        cells = table.add_row().cells
        set_cell_shading(cells[0], LIGHT_BLUE)
        set_cell_text(cells[0], label, bold=True, size=10.5)
        set_cell_text(cells[1], value, size=10.5)
    doc.add_paragraph()
    p(doc, "This report documents the TaskFlow repository work for Question 1, an original design-only SDLC proposal for Question 2, and a command runbook for Question 3. The Q1 statements are based on the repository history and supplied terminal captures. Question 2 is a simulated design exercise. Question 3 commands must be executed and captured on the assigned Amazon Linux instance before submission.")

    heading(doc, "Question 1 Git and GitHub Creating and Resolving a Merge Conflict")
    doc.add_heading("Project used", level=2)
    p(doc, "TaskFlow is a React and Vite student productivity dashboard. It lets a student add, edit, delete, search, filter, prioritise, complete, and reopen coursework tasks. Task records are retained in browser localStorage, and the project includes automated tests plus a GitHub Actions deployment workflow for GitHub Pages.")
    p(doc, "Repository: https://github.com/PuneetGarg189/UCS745-Q1-TaskFlow")
    doc.add_heading("Repository setup and development evidence", level=2)
    code(doc, "$ git init\n$ git remote add origin https://github.com/PuneetGarg189/UCS745-Q1-TaskFlow.git\n$ npm run test\n$ npm run build\n$ git push origin main")
    p(doc, "The current project history records the application build in commit 816d2c9, test coverage in 2d76c48, the Pages workflow in 2d448c7, and the final reflective report in fb2f77e. The local test suite passed nine tests and the production Vite build completed successfully during final verification.")
    figure(doc, "Screenshot 2026-11-24 at 4.13.10\u202fPM.png", "Figure 1. TaskFlow merge history on main after integrating the first feature branch.")
    doc.add_heading("Intentional conflict and resolution", level=2)
    p(doc, "The intentional conflict was kept in README.md so that the application code stayed safe. Both branches started from commit e30593a and edited the same project-description paragraph differently. Feature A was merged first with commit 4208683. Merging feature-b-readme-title afterwards produced a real content conflict in README.md.")
    code(doc, "$ git checkout main\n$ git merge --no-ff feature-a-readme-title -m \"merge: integrate README feature A\"\n$ git merge feature-b-readme-title\n$ git status\n$ git diff")
    figure(doc, "Screenshot 2026-11-24 at 4.14.16\u202fPM.png", "Figure 2. Git reports the README.md content conflict after the second merge.")
    p(doc, "I read both alternatives, removed the conflict markers, and kept a single accurate description: TaskFlow is a lightweight student planner for organising coursework, assignments, and deadlines. The merge-resolution commit is 614a1d1. The final graph shows both feature commits as parents, which verifies that the merge was not merely a file overwrite.")
    code(doc, "$ git add README.md\n$ git commit -m \"docs: resolve README description merge conflict\"\n$ git push origin main\n$ git log --oneline --graph --decorate -8")
    figure(doc, "Screenshot 2026-11-24 at 4.57.45\u202fPM.png", "Figure 3. GitHub Actions test, build, and GitHub Pages deployment completed successfully.")
    doc.add_heading("Reflection", level=2)
    p(doc, "This exercise showed that a merge conflict is not an error to bypass. Git stopped because both branches changed the same lines after a common base commit, and neither version should be selected automatically. Reviewing the staged difference before committing made it possible to preserve the useful intent while restoring a clean README. Keeping branches focused and merging them regularly reduces the size and risk of future conflicts.")

    heading(doc, "Question 2 Software Project Using an SDLC Model")
    doc.add_heading("Project CampusSync attendance tracker", level=2)
    p(doc, "CampusSync is a proposed web and mobile attendance service for classroom sessions. Faculty start an attendance window, students scan a short-lived QR code, and the service records attendance only when the device is near the room. The student dashboard shows course-wise attendance and alerts students when their percentage approaches the institutional threshold. This is a design-only proposal; its outcomes below are simulated design checks, not results from a deployed system.")
    doc.add_heading("Users and requirements", level=2)
    bullet(doc, "Student: scans the code, sees course attendance, receives low-attendance alerts, and can upload supporting evidence for a leave request.")
    bullet(doc, "Faculty: opens a session, observes the live list, and records a justified manual correction when necessary.")
    bullet(doc, "Administrator: configures courses and schedules, reviews attendance reports, and audits changes.")
    doc.add_page_break()
    add_table(doc, ["ID", "Requirement", "Acceptance detail"], [
        ("FR-01", "Role based access", "University sign-in separates student, faculty, and administrator permissions."),
        ("FR-02", "Expiring QR session", "A signed QR token changes every 20 seconds and cannot be reused after expiry."),
        ("FR-03", "Location validation", "A scan is accepted within the configured classroom radius; failed checks are logged."),
        ("FR-04", "Attendance alerts", "The service recalculates attendance after each session and warns a student below 75 percent."),
        ("NFR-01", "Performance", "The normal lecture-start load of 500 scans is processed with a response target below 1.5 seconds."),
        ("NFR-02", "Security", "HTTPS is required and every change to an attendance record has an audit timestamp."),
    ], [0.7, 1.65, 4.05])
    doc.add_heading("Chosen SDLC model Incremental", level=2)
    p(doc, "I selected the Incremental model because it delivers a useful core before the more uncertain QR and geofence work. Each increment can be tested with the same users who will operate it, and a problem in a later increment does not prevent faculty from taking attendance through the core workflow.")
    add_table(doc, ["Increment", "Scope", "Reason for ordering"], [
        ("1", "Sign-in, roles, course setup, enrolment, and faculty-managed attendance.", "Provides a usable baseline for the first teaching week."),
        ("2", "Short-lived QR, scanner screen, location check, and scan audit trail.", "Contains the main technical and fairness risk in one testable release."),
        ("3", "Attendance analytics, low-attendance notifications, reports, and export.", "Builds on reliable attendance data from the earlier releases."),
    ], [0.85, 3.4, 2.15])
    doc.add_heading("SDLC phases and delivery plan", level=2)
    p(doc, "Planning establishes the attendance policy, consent requirements, room-location tolerance, and availability target. Design defines the React or PWA client, an API service, relational storage for users, courses, sessions and attendance records, and an audit-log boundary. Development is planned across ten weeks: weeks 1 to 3 for the core, weeks 4 to 7 for QR and geofencing, and weeks 8 to 10 for analytics and alerts. Testing includes unit tests for token expiry, integration tests for the attendance write path, accessibility checks for the student view, and a simulated 500-scan load test. Deployment packages the service in containers and uses CI/CD with a rollback-capable release process.")
    doc.add_heading("Simulated test outcomes", level=2)
    add_table(doc, ["Test", "Scenario", "Expected outcome", "Result"], [
        ("TC-01", "Valid scan in the room", "Attendance is recorded and the faculty list updates.", "Pass"),
        ("TC-02", "Scan well outside the room", "The scan is rejected and an audit entry is created.", "Pass"),
        ("TC-03", "A screenshot of an expired QR", "The token is rejected; a live code is required.", "Pass"),
        ("TC-04", "500 scans near lecture start", "Requests are accepted within the response target.", "Pass"),
        ("TC-05", "Attendance becomes 74.2 percent", "The student receives a warning and can view the course detail.", "Pass"),
    ], [0.7, 2.0, 3.4, 0.7])
    doc.add_heading("Conflict resolution and key lessons", level=2)
    p(doc, "The principal design conflict is accuracy versus fairness. GPS readings can drift, particularly indoors, so a strict automatic rejection could penalise a student who is actually present. The design therefore stores the location result and permits a faculty override with a reason. A second conflict is between stronger anti-proxy controls and cost or accessibility. QR plus location is the initial scope; biometric hardware is explicitly deferred. The key lesson is to isolate risky features in a later increment, capture decision reasons, and seek feedback after every delivery.")

    heading(doc, "Question 3 User Management on Amazon Linux")
    p(doc, "This section is a safe execution runbook for the stated Amazon Linux scenario. It does not claim that these commands were executed in this workspace. Before submitting, run the commands on the assigned EC2 instance and replace the verification checklist with terminal captures from that instance.")
    doc.add_heading("Initial setup", level=2)
    code(doc, "sudo groupadd Developer\nsudo groupadd Tester\nsudo useradd -m -g Developer -s /bin/bash Developer1\nsudo useradd -m -g Developer -s /bin/bash Developer2\nsudo useradd -m -g Developer -s /bin/bash Developer3\nsudo useradd -m -g Tester -s /bin/bash Tester1\nsudo useradd -m -g Tester -s /bin/bash Tester2\nsudo mkdir -p /opt/Hdfc_Bank-ClientApp\nsudo chown -R root:Developer /opt/Hdfc_Bank-ClientApp\nsudo chmod 2775 /opt/Hdfc_Bank-ClientApp\nsudo setfacl -R -m g:Tester:rx /opt/Hdfc_Bank-ClientApp")
    p(doc, "The set-group-ID permission (2775) keeps the Developer group on new files in the project directory. The ACL gives the Tester group read and traverse access; verify ACL availability with getfacl before relying on it.")
    doc.add_heading("Add Developer4 to the Developer group", level=2)
    code(doc, "sudo useradd -m -g Developer -s /bin/bash Developer4\nsudo passwd Developer4\nid Developer4\ngetent passwd Developer4\ngetent group Developer")
    p(doc, "If Developer4 already exists, use sudo usermod -aG Developer Developer4 instead. id Developer4 confirms the effective primary and supplementary groups; getent uses the configured account database rather than assuming a local-only setup.")
    doc.add_heading("Remove Developer3 completely", level=2)
    code(doc, "sudo loginctl terminate-user Developer3 2>/dev/null || true\nsudo find / -xdev -user Developer3 -print\nsudo userdel -r Developer3\nid Developer3\nsudo test ! -e /home/Developer3 && echo \"home removed\"")
    p(doc, "Review the find output before deleting the account, because userdel -r removes the home directory and mail spool but not files elsewhere. The -xdev option avoids crossing into separately mounted filesystems during the review. Do not delete shared project files blindly; reassign ownership where appropriate before removal.")
    doc.add_heading("Inspect and edit Hdfc-Pack.zip", level=2)
    code(doc, "cd /opt/Hdfc_Bank-ClientApp\nunzip -l Hdfc-Pack.zip\nzip -d Hdfc-Pack.zip 'Hdfc-Pack/temp_debug.log'\nunzip -l Hdfc-Pack.zip\nunzip -t Hdfc-Pack.zip")
    p(doc, "unzip -l lists an archive without extraction. zip -d removes only the named archive member, so the full Hdfc-Pack/ prefix must match the listing exactly. The final listing and integrity test provide the required verification.")
    doc.add_heading("Evidence checklist", level=2)
    add_table(doc, ["Task", "Capture required before submission"], [
        ("Developer4", "id Developer4 and getent group Developer"),
        ("Developer3", "The reviewed owned-file list, the userdel result, and a failed id Developer3 check"),
        ("Archive", "unzip -l before and after deletion, plus unzip -t output"),
    ], [1.45, 5.55])
    doc.add_heading("Command summary", level=2)
    add_table(doc, ["Operation", "Purpose", "Verification"], [
        ("useradd -m -g", "Creates a user with a home directory and selected primary group.", "id and getent passwd"),
        ("userdel -r", "Removes the account, home directory, and mail spool after review.", "id fails; home path is absent"),
        ("unzip -l", "Lists the archive without extracting it.", "Archive member list"),
        ("zip -d", "Deletes one named archive member in place.", "Updated list and unzip -t"),
    ], [1.55, 3.35, 2.1])
    p(doc, "Execution note: use a disposable lab account and confirm the exact archive member name from the listing before deleting it. For a graded submission, attach only terminal evidence produced by the assigned environment.")

    section = doc.sections[0]
    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer.add_run("UCS745 Lab Assignment | Puneet Garg | 102303189")
    doc.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()

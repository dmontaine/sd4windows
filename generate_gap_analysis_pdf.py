#!/usr/bin/env python
"""Generate the SD Core Documentation Change Proposals PDF."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white, grey
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, KeepTogether
)
from reportlab.pdfgen import canvas
import os

OUTPUT_PATH = os.path.join(os.path.expanduser("~"), "Documents", "10centDocChangeProposals.pdf")

# --- Styles ---
styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Title'],
    fontSize=22,
    spaceAfter=6,
    textColor=HexColor('#1a1a2e'),
)

subtitle_style = ParagraphStyle(
    'DocSubtitle',
    parent=styles['Normal'],
    fontSize=11,
    spaceAfter=20,
    textColor=HexColor('#555555'),
    alignment=TA_CENTER,
    fontName='Helvetica-Oblique',
)

h1_style = ParagraphStyle(
    'H1',
    parent=styles['Heading1'],
    fontSize=15,
    spaceBefore=18,
    spaceAfter=8,
    textColor=HexColor('#16213e'),
    borderWidth=0,
    borderPadding=0,
)

h2_style = ParagraphStyle(
    'H2',
    parent=styles['Heading2'],
    fontSize=12,
    spaceBefore=12,
    spaceAfter=6,
    textColor=HexColor('#0f3460'),
)

body_style = ParagraphStyle(
    'Body',
    parent=styles['Normal'],
    fontSize=10,
    leading=14,
    spaceAfter=6,
    alignment=TA_LEFT,
)

bullet_style = ParagraphStyle(
    'Bullet',
    parent=body_style,
    leftIndent=18,
    bulletIndent=6,
    spaceAfter=3,
)

note_style = ParagraphStyle(
    'Note',
    parent=body_style,
    fontSize=9.5,
    textColor=HexColor('#444444'),
    leftIndent=12,
    rightIndent=12,
    spaceBefore=4,
    spaceAfter=8,
    fontName='Helvetica-Oblique',
)

recommendation_style = ParagraphStyle(
    'Recommendation',
    parent=body_style,
    fontSize=10,
    leftIndent=18,
    rightIndent=12,
    spaceBefore=4,
    spaceAfter=8,
    textColor=HexColor('#1a1a2e'),
    backColor=HexColor('#f0f0f8'),
    borderColor=HexColor('#9999bb'),
    borderWidth=0.5,
    borderPadding=8,
)


# --- Page numbering ---
def add_page_number(canvas_obj, doc):
    canvas_obj.saveState()
    canvas_obj.setFont('Helvetica', 8)
    canvas_obj.setFillColor(grey)
    page_num = canvas_obj.getPageNumber()
    canvas_obj.drawRightString(
        letter[0] - 0.75 * inch,
        0.5 * inch,
        f"Page {page_num}"
    )
    canvas_obj.drawString(
        0.75 * inch,
        0.5 * inch,
        "SD Core for Windows - Documentation Change Proposals"
    )
    canvas_obj.restoreState()


# --- Build content ---
def build_story():
    story = []

    # Title page
    story.append(Spacer(1, 2 * inch))
    story.append(Paragraph("SD Core for Windows 1.0-0", title_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Documentation Change Proposals", title_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "A gap analysis comparing upstream OpenQM and SD documentation "
        "against the current SD Core for Windows documentation set, "
        "with recommendations for new and expanded documents.",
        subtitle_style
    ))
    story.append(Spacer(1, 0.5 * inch))

    # Info table
    info_data = [
        ["Date", "August 2026"],
        ["Document Set", "01-34, 94-95 (36 documents)"],
        ["Proposed New Docs", "12"],
        ["Proposed Expansions", "5"],
        ["Platform", "Windows only"],
    ]
    info_table = Table(info_data, colWidths=[2 * inch, 3 * inch])
    info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, -1), HexColor('#0f3460')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('LINEBELOW', (0, 0), (-1, -2), 0.25, HexColor('#cccccc')),
    ]))
    story.append(info_table)
    story.append(PageBreak())

    # Overview
    story.append(Paragraph("Overview", h1_style))
    story.append(Paragraph(
        "This report compares the upstream OpenQM 2.6.6 documentation "
        "(PDF reference, tutorial, conversion manual, and index), the SD "
        "Linux Help documents (ODT source and SD Manual), and the SD API "
        "Headers against the current SD Core for Windows documentation "
        "set (01-34, 94-95). The goal is to identify what the SD Core "
        "docs do not cover and to recommend how those gaps should be "
        "filled. Features confirmed as shipped in SD Core for Windows "
        "are included. Features that have been removed from the Windows "
        "port are excluded.",
        body_style
    ))

    # Features excluded
    story.append(Paragraph("Features Excluded from This Analysis", h1_style))
    story.append(Paragraph(
        "The following upstream features were investigated in the source "
        "tree and confirmed as not shipping in SD Core for Windows. They "
        "are excluded from all proposals.",
        body_style
    ))

    excluded_data = [
        ["Feature", "Status", "Evidence"],
        ["QMNet / remote files", "Removed",
         "netfiles.c deleted; server;file VOC handling removed; "
         "NETFILES config parameter parsed but inert"],
        ["Embedded Python", "Removed",
         "sdext_py.c, op_sdpyobj.c deleted; OP_SDPYOBJ opcode retired "
         "to op_illegal; Makefile drops PY_HDRS and PY_LDFLAGS"],
        ["sdlnxd daemon", "Linux-only",
         "The monitoring daemon has no Windows equivalent"],
        ["ENCRYPT.FIELD verb", "Removed",
         "VOC entry pointed at $CRYPTO which never existed in the GPL release"],
    ]
    excluded_table = Table(excluded_data, colWidths=[1.5 * inch, 1 * inch, 3.5 * inch])
    excluded_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 8.5),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#16213e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f5f5fa')]),
        ('GRID', (0, 0), (-1, -1), 0.25, HexColor('#999999')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(excluded_table)
    story.append(Spacer(1, 12))

    # Current coverage
    story.append(Paragraph("What the SD Core Docs Currently Cover", h1_style))
    story.append(Paragraph(
        "The current set is 34 documents plus two syntax references:",
        body_style
    ))

    coverage_data = [
        ["Range", "Category", "Coverage"],
        ["01-18", "SDBasic",
         "Program structure, control flow, math, strings, dynamic arrays, "
         "data conversion, file handling, select lists, indexes, sequential "
         "files, CSV, terminal I/O, printing, locks/transactions, sockets, "
         "system/environment, debugging, modern program structure"],
        ["19-31", "TCL",
         "Command processor, files/records, query processor, select lists, "
         "indexes, programs/catalogue, ED, EDIT, MICRO, printing/spooling, "
         "terminal/session, processes/phantoms, locks"],
        ["32", "VOC", "Structure and usage"],
        ["33-34", "Dictionaries", "Record structure, conversions and formatting"],
        ["94-95", "Syntax", "BASIC syntax, TCL syntax"],
    ]
    coverage_table = Table(coverage_data, colWidths=[0.7 * inch, 1.2 * inch, 4.1 * inch])
    coverage_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 8.5),
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#16213e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f5f5fa')]),
        ('GRID', (0, 0), (-1, -1), 0.25, HexColor('#999999')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(coverage_table)
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "This is strong coverage of the programming language and the TCL "
        "command layer. The gaps are below.",
        body_style
    ))

    # Gap 1
    story.append(Paragraph("Gap 1: No Getting Started / Introduction", h1_style))
    story.append(Paragraph(
        "<b>What is missing.</b> The upstream docs have a tutorial that "
        "introduces the multivalue concept, explains what SD is, walks "
        "through first steps (creating a file, entering data, listing it), "
        "and gives an overview of the system architecture. Our docs jump "
        "straight into SDBasic program structure with no orientation.",
        body_style
    ))
    story.append(Paragraph(
        "<b>What upstream covers that we don't:</b>",
        body_style
    ))
    for item in [
        "What is a multivalue database? (the order-processing example, the history from Dick Pick through to SD)",
        "What SD is - a fork of ScarletDME/OpenQM, GPL v3, community-supported",
        "The four components: command processor, query processor, SDBasic, SDClient API",
        "First steps: logging in, creating a file, entering a record, listing it, editing a program",
        "Document conventions (bold = literal, italics = variable, etc.)",
    ]:
        story.append(Paragraph(f"&bull; {item}", bullet_style))

    story.append(Paragraph(
        "<b>Recommendation.</b> One new document:",
        body_style
    ))
    story.append(Paragraph(
        "<b>00-sd-introduction.md</b> - <i>SD Core - Introduction and Getting Started</i><br/><br/>"
        "Covers: what a multivalue database is, what SD is and its lineage, "
        "the four components, logging in for the first time, creating a "
        "file, adding a record, listing it, writing and cataloguing a "
        "one-line program, document conventions. Numbered 00 so it sits "
        "before the BASIC sequence.",
        recommendation_style
    ))

    # Gap 2
    story.append(Paragraph("Gap 2: No System Administration Documentation", h1_style))
    story.append(Paragraph(
        "<b>What is missing.</b> The upstream docs have an entire system "
        "administration section covering configuration, accounts, users, "
        "security, process management, and file system monitoring. Our docs "
        "have nothing on administration - no CONFIG, no CREATE.ACCOUNT, "
        "no CREATE.USER, no LISTU, no PSTAT, no LIST.FILES, no "
        "ANALYSE.FILE, no FSTAT, no LIST.LOCKS.",
        body_style
    ))
    story.append(Paragraph("<b>What upstream covers that we don't:</b>", body_style))
    for item in [
        "Configuration parameters (CONFIG command, the configuration file, ~30 parameters: CMDSTACK, DEADLOCK, ERRLOG, FSYNC, GRPSIZE, MAXIDLEN, MUSTLOCK, NUMFILES, NUMLOCKS, OBJECTS, OBJMEM, PDUMP, PRECISION, PTYPES, etc.)",
        "Account management (CREATE.ACCOUNT, DELETE.ACCOUNT, the QMSYS account, how accounts map to directories)",
        "User management (CREATE.USER, DELETE.USER, LIST.USERS, ADMIN.USER, passwords)",
        "Security (SECURITY command, privileged vs. non-privileged users)",
        "Process management (LISTU, PSTAT, LOGOUT)",
        "File system monitoring (LIST.FILES, LIST.LOCKS, LIST.READU, UNLOCK, FSTAT, ANALYSE.FILE)",
    ]:
        story.append(Paragraph(f"&bull; {item}", bullet_style))
    story.append(Paragraph(
        "<b>Note.</b> The NETFILES and FILERULE configuration parameters "
        "are inert in the Windows port (QMNet was removed) and should "
        "be listed but marked as non-functional.",
        note_style
    ))
    story.append(Paragraph("<b>Recommendation.</b> Two new documents:", body_style))
    story.append(Paragraph(
        "<b>35-sd-admin-configuration.md</b> - <i>SD Administration - Configuration</i><br/><br/>"
        "Covers: the CONFIG command, the configuration file, every "
        "configuration parameter that is active in the Windows port "
        "(grouped: system limits, file system, locking, printing, "
        "diagnostics), global vs. private parameters, licence management "
        "(UPDATE.LICENCE). Parameters that are inert due to removed "
        "features (NETFILES, FILERULE) are listed but marked as "
        "non-functional.",
        recommendation_style
    ))
    story.append(Paragraph(
        "<b>36-sd-admin-accounts-and-security.md</b> - <i>SD Administration - Accounts, Users and Security</i><br/><br/>"
        "Covers: accounts and how they map to directories, "
        "CREATE.ACCOUNT, DELETE.ACCOUNT, the QMSYS account, user "
        "management (CREATE.USER, DELETE.USER, LIST.USERS, ADMIN.USER), "
        "passwords, the SECURITY command, privileged users, process "
        "management (LISTU, PSTAT, LOGOUT), file system monitoring "
        "(LIST.FILES, LIST.LOCKS, LIST.READU, UNLOCK, FSTAT, "
        "ANALYSE.FILE).",
        recommendation_style
    ))

    # Gap 3
    story.append(Paragraph("Gap 3: No Installation, Startup, or Shutdown Documentation", h1_style))
    story.append(Paragraph(
        "<b>What is missing.</b> The upstream docs cover installation, "
        "startup and shutdown of the server, and deinstallation. Our docs "
        "don't cover installation or the service lifecycle.",
        body_style
    ))
    story.append(Paragraph("<b>What upstream covers that we don't:</b>", body_style))
    for item in [
        "Installation (directory structure, licence entry, initial setup)",
        "Startup and shutdown of the SD server",
        "Deinstallation",
    ]:
        story.append(Paragraph(f"&bull; {item}", bullet_style))
    story.append(Paragraph(
        "<b>Note.</b> The upstream docs reference the sdlnxd background "
        "daemon. The daemon is Linux-only and does not ship on Windows. "
        "Startup and shutdown on Windows uses the service or the sd "
        "command with start/stop flags.",
        note_style
    ))
    story.append(Paragraph("<b>Recommendation.</b> One new document:", body_style))
    story.append(Paragraph(
        "<b>37-sd-installation.md</b> - <i>SD Core for Windows - Installation and Setup</i><br/><br/>"
        "Covers: system requirements, installation procedure, directory "
        "structure, starting and stopping the server, licence entry, "
        "initial account creation, verifying the installation.",
        recommendation_style
    ))

    # Gap 4
    story.append(Paragraph("Gap 4: No SDClient API Documentation", h1_style))
    story.append(Paragraph(
        "<b>What is missing.</b> The upstream docs have a QMClient API "
        "section covering the C client library, and the SD API Headers "
        "file documents ~45 functions across four language bindings "
        "(Gambas3, PureBasic, Free Pascal, Python ctypes). The sdclilib "
        "shared library ships in the Windows port. Our docs have nothing "
        "on the client API.",
        body_style
    ))
    story.append(Paragraph("<b>What upstream covers that we don't:</b>", body_style))
    for item in [
        "The SDClient API concept (external applications connecting to SD)",
        "Connection management (SDConnect, SDConnectLocal, SDDisconnect, SDDisconnectAll, SDConnected)",
        "File operations (SDOpen, SDRead, SDReadu, SDWrite, SDWriteu, SDDelete, SDDeleteu, SDClose, SDMarkMapping)",
        "Record manipulation (SDExtract, SDIns, SDDel, SDLocate)",
        "String functions (SDField, SDDcount, SDChange, SDMatch, SDSubstr)",
        "Command execution (SDExecute, SDEndCommand, SDCall/SDCallx with 0-20 argument variants)",
        "Select lists (SDSelect, SDSelectv, SDClearSelect, SDReadNext, SDRelease)",
        "Session management (SDGetSession, SDLogto, SDGetArg, SDEnterPackage, SDExitPackage)",
        "Error handling (SDError, SDDebug)",
        "Server status codes (SV_OK, SV_ON_ERROR, SV_ELSE, SV_ERROR, SV_LOCKED, SV_PROMPT)",
    ]:
        story.append(Paragraph(f"&bull; {item}", bullet_style))
    story.append(Paragraph(
        "<b>Note.</b> SDConnectUDS (Unix Domain Socket) is in the header "
        "but is not applicable on Windows. The Windows port supports "
        "local and TCP connections only. Language bindings should reference "
        "the shared library as sdclilib (the Windows build produces a .dll).",
        note_style
    ))
    story.append(Paragraph("<b>Recommendation.</b> One new document:", body_style))
    story.append(Paragraph(
        "<b>38-sd-client-api.md</b> - <i>SD Client API</i><br/><br/>"
        "Covers: the sdclilib shared library, connection management "
        "(local and TCP only; no UDS), file operations, record "
        "manipulation, string functions, command execution and subroutine "
        "calls, select lists, session management, error handling, the "
        "six server status codes, language bindings (Python ctypes, Free "
        "Pascal, Gambas, PureBasic).",
        recommendation_style
    ))

    # Gap 5
    story.append(Paragraph("Gap 5: No Encryption Documentation", h1_style))
    story.append(Paragraph(
        "<b>What is missing.</b> SD Core for Windows ships with "
        "libsodium-based encryption (sd_encrypt_sodium.c compiles and "
        "links). The upstream SD docs have an encryption document. Our "
        "docs don't cover it.",
        body_style
    ))
    story.append(Paragraph("<b>What upstream covers that we don't:</b>", body_style))
    for item in [
        "The SDENCRYPT and SDDECRYPT SDBasic functions",
        "The encryption library (libsodium)",
        "Key management (SD_SALT, SD_KEYFROMPW keys)",
        "Field-level encryption from SDBasic",
        "SCRAM-SHA-256 authentication primitives (SHA-256, HMAC-SHA256, PBKDF2, random bytes, XOR, constant-time compare)",
    ]:
        story.append(Paragraph(f"&bull; {item}", bullet_style))
    story.append(Paragraph(
        "<b>Note.</b> The ENCRYPT.FIELD VOC verb is removed and should "
        "not be documented. The underlying SDENCRYPT/SDDECRYPT BASIC "
        "functions and the C-level sd_encrypt()/sd_decrypt() functions "
        "are present.",
        note_style
    ))
    story.append(Paragraph("<b>Recommendation.</b> One new document:", body_style))
    story.append(Paragraph(
        "<b>39-sd-encryption.md</b> - <i>SD Encryption</i><br/><br/>"
        "Covers: the SDENCRYPT and SDDECRYPT SDBasic functions, the "
        "libsodium crypto library, key management (SD_SALT, "
        "SD_KEYFROMPW), field-level encryption from SDBasic, the "
        "SCRAM-SHA-256 authentication primitives.",
        recommendation_style
    ))

    # Gap 6
    story.append(Paragraph("Gap 6: No SDEXT Extension Documentation", h1_style))
    story.append(Paragraph(
        "<b>What is missing.</b> The upstream SD docs have an SDEXT "
        "extension document. The op_sdext.c source file ships in the "
        "Windows port and handles encryption keys. Our docs don't cover "
        "the SDEXT extension.",
        body_style
    ))
    story.append(Paragraph("<b>What upstream covers that we don't:</b>", body_style))
    for item in [
        "The SDEXT extension and what it provides",
        "How to enable and use SDEXT",
        "Which keys and functions are available through SDEXT",
    ]:
        story.append(Paragraph(f"&bull; {item}", bullet_style))
    story.append(Paragraph(
        "<b>Note.</b> The Python portion of SDEXT has been removed. The "
        "remaining SDEXT functionality (encryption keys, hex/base64 "
        "encoding) is present. The proposal should cover only what ships.",
        note_style
    ))
    story.append(Paragraph("<b>Recommendation.</b> One new document:", body_style))
    story.append(Paragraph(
        "<b>40-sd-sdext.md</b> - <i>SD SDEXT Extension</i><br/><br/>"
        "Covers: what SDEXT is, the keys and functions it provides "
        "(encryption, hex encoding, base64 encoding), how to enable it. "
        "Does not cover removed Python SDEXT functionality.",
        recommendation_style
    ))

    # Gap 7
    story.append(Paragraph("Gap 7: No Terminal Information (Terminfo) Documentation", h1_style))
    story.append(Paragraph(
        "<b>What is missing.</b> The upstream docs cover the terminfo "
        "database and the terminfo compiler. The sdterminfo.c source file "
        "ships in the Windows port. Our docs mention terminal handling "
        "in 29-sd-tcl-the-terminal-and-the-session.md but don't cover "
        "terminfo.",
        body_style
    ))
    story.append(Paragraph("<b>What upstream covers that we don't:</b>", body_style))
    for item in [
        "The terminfo database",
        "The terminfo compiler utility",
        "Terminal capability definitions",
        "How SD uses terminfo for screen control",
    ]:
        story.append(Paragraph(f"&bull; {item}", bullet_style))
    story.append(Paragraph(
        "<b>Recommendation.</b> Expand the existing terminal document or "
        "create a new one: Expand 29-sd-tcl-the-terminal-and-the-session.md "
        "to cover terminfo, or create <b>41-sd-terminfo.md</b> - <i>SD "
        "Terminal Information (Terminfo)</i>. Covers: the terminfo "
        "database, the terminfo compiler, terminal capability definitions, "
        "how SD uses terminfo for screen control, customising terminal "
        "definitions.",
        recommendation_style
    ))

    # Gap 8
    story.append(Paragraph("Gap 8: No System Limits Reference", h1_style))
    story.append(Paragraph(
        "<b>What is missing.</b> The upstream docs have a system limits "
        "page documenting maximum record sizes, maximum field numbers, "
        "maximum open files, maximum select list items, etc. Our docs "
        "don't have a consolidated limits reference.",
        body_style
    ))
    story.append(Paragraph("<b>Recommendation.</b> One new document:", body_style))
    story.append(Paragraph(
        "<b>42-sd-system-limits.md</b> - <i>SD System Limits</i><br/><br/>"
        "Covers: maximum record size, maximum field count, maximum field "
        "length, maximum open files, maximum locks, maximum select list "
        "size, maximum program size, maximum subroutine call depth, "
        "maximum matrix dimensions, etc.",
        recommendation_style
    ))

    # Gap 9
    story.append(Paragraph("Gap 9: No Glossary", h1_style))
    story.append(Paragraph(
        "<b>What is missing.</b> The upstream docs have a glossary of "
        "terms. Our docs explain terms inline but have no consolidated "
        "glossary.",
        body_style
    ))
    story.append(Paragraph("<b>Recommendation.</b> One new document:", body_style))
    story.append(Paragraph(
        "<b>43-sd-glossary.md</b> - <i>SD Glossary</i><br/><br/>"
        "Covers: account, association, attribute, background, break key, "
        "catalogue, command stack, common block, conversion code, "
        "correlative, dictionary, dynamic array, dynamic file, field, "
        "file, group, index, I-type, mark character, matrix, multivalue, "
        "overflow, paragraph, phantom, p-code, QMSYS, record, select "
        "list, subvalue, terminfo, transaction, VOC, etc.",
        recommendation_style
    ))

    # Gap 10
    story.append(Paragraph("Gap 10: No Format Specification Reference for Dictionaries", h1_style))
    story.append(Paragraph(
        "<b>What is missing.</b> The 34-sd-dicts-conversions.md document "
        "covers format specifications, but the upstream docs have a "
        "dedicated format specification page with more detail than our "
        "doc provides - particularly the full mask syntax, date format "
        "strings, and the interaction between format and conversion.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Recommendation.</b> Expand the existing document rather than "
        "create a new one: Expand 34-sd-dicts-conversions.md to cover the "
        "full format specification syntax in more detail, including the "
        "mask syntax, date format string elements (D, DD, M, MM, MA, ML, "
        "Y, YY, J, Q, W, WL, N), and the interaction between field 3 "
        "(conversion) and field 5 (format).",
        recommendation_style
    ))

    # Gap 11
    story.append(Paragraph("Gap 11: No Standard Subroutines Reference", h1_style))
    story.append(Paragraph(
        "<b>What is missing.</b> The upstream docs have a \"Standard "
        "Subroutines\" page documenting the catalogued subroutines that "
        "ship with the system - things like !PARSER, !FTYPE, !PCL, "
        "!SCREEN, etc. Our docs mention some of these in passing but "
        "don't have a consolidated reference.",
        body_style
    ))
    story.append(Paragraph("<b>Recommendation.</b> One new document:", body_style))
    story.append(Paragraph(
        "<b>44-sd-standard-subroutines.md</b> - <i>SD Standard Subroutines</i><br/><br/>"
        "Covers: the !-prefixed internal subroutines (!PARSER, !FTYPE, "
        "!PCL, !SCREEN, !OCONV, !ICONV, !SORT, !USERNAME, !ERRTEXT, "
        "etc.), what each does, and how to call them from SDBasic.",
        recommendation_style
    ))

    # Gap 12
    story.append(Paragraph("Gap 12: No MV File Concepts Document", h1_style))
    story.append(Paragraph(
        "<b>What is missing.</b> The upstream SD docs have an \"MV File "
        "Concepts\" document that explains the multivalue file model in "
        "detail - the difference between directory files and dynamic "
        "files, how groups work, how overflow works, how the file system "
        "is organised on disk. Our docs cover file handling (07) and "
        "alternate key indexes (09) but don't explain the underlying file "
        "system structure.",
        body_style
    ))
    story.append(Paragraph("<b>What upstream covers that we don't:</b>", body_style))
    for item in [
        "Directory files vs. dynamic files",
        "Group structure and overflow",
        "File system organisation on disk (the sub-file structure)",
        "The dynamic file resize mechanism",
        "How the hash algorithm works",
    ]:
        story.append(Paragraph(f"&bull; {item}", bullet_style))
    story.append(Paragraph("<b>Recommendation.</b> One new document:", body_style))
    story.append(Paragraph(
        "<b>45-sd-file-system.md</b> - <i>SD File System Concepts</i><br/><br/>"
        "Covers: the two file types (directory and dynamic), group "
        "structure, overflow, on-disk layout, file resize, the hash "
        "algorithm, file analysis (ANALYSE.FILE), file statistics (FSTAT).",
        recommendation_style
    ))

    # Gap 13
    story.append(Paragraph("Gap 13: Incomplete TCL Command Coverage", h1_style))
    story.append(Paragraph(
        "<b>What is missing.</b> The upstream docs cover many TCL commands "
        "our docs don't. Some are administrative (covered in Gap 2 above), "
        "but some are general-purpose:",
        body_style
    ))

    tcl_data = [
        ["Command", "What it does", "Where it should go"],
        ["COMPILE", "compile a program", "expand 24"],
        ["BASIC", "compile BASIC", "expand 24"],
        ["COPY", "copy records", "new or expand 20"],
        ["DELETE", "delete records", "new or expand 20"],
        ["COUNT", "count records", "expand 21"],
        ["SEARCH", "search records", "new"],
        ["LIST.ITEM", "list raw records", "expand 21"],
        ["SORT.ITEM", "sort raw records", "expand 21"],
        ["SUM", "sum a field", "expand 21"],
        ["STATS", "statistics", "new"],
        ["REFORMAT", "reformat records", "new"],
        ["SREFORMAT", "sorted reformat", "new"],
        ["LIST.LABEL", "label printing", "expand 28"],
        ["SORT.LABEL", "sorted labels", "expand 28"],
        ["SHOW", "show a file", "new"],
        ["WHERE", "where is a program", "new"],
        ["VERIFY", "verify a file", "new"],
    ]
    tcl_table = Table(tcl_data, colWidths=[1.3 * inch, 2 * inch, 1.7 * inch])
    tcl_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 8.5),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#16213e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f5f5fa')]),
        ('GRID', (0, 0), (-1, -1), 0.25, HexColor('#999999')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(tcl_table)
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "<b>Recommendation.</b> Rather than create a new document for each, "
        "fold the administrative commands into the documents proposed in "
        "Gap 2, and expand the existing TCL docs to cover the remaining "
        "commands. The query processor doc (21) should mention COUNT, SUM, "
        "LIST.ITEM, SORT.ITEM, REFORMAT, SREFORMAT, SEARCH, SHOW.",
        body_style
    ))

    # Summary tables
    story.append(PageBreak())
    story.append(Paragraph("Summary: Recommended New Documents", h1_style))

    new_docs_data = [
        ["#", "Filename", "Title", "Priority"],
        ["00", "00-sd-introduction.md", "SD Core - Introduction and Getting Started", "High"],
        ["35", "35-sd-admin-configuration.md", "SD Administration - Configuration", "High"],
        ["36", "36-sd-admin-accounts-and-security.md", "SD Administration - Accounts, Users and Security", "High"],
        ["37", "37-sd-installation.md", "SD Core for Windows - Installation and Setup", "Medium"],
        ["38", "38-sd-client-api.md", "SD Client API", "Medium"],
        ["39", "39-sd-encryption.md", "SD Encryption", "Low"],
        ["40", "40-sd-sdext.md", "SD SDEXT Extension", "Low"],
        ["41", "41-sd-terminfo.md", "SD Terminal Information (Terminfo)", "Low"],
        ["42", "42-sd-system-limits.md", "SD System Limits", "Low"],
        ["43", "43-sd-glossary.md", "SD Glossary", "Low"],
        ["44", "44-sd-standard-subroutines.md", "SD Standard Subroutines", "Low"],
        ["45", "45-sd-file-system.md", "SD File System Concepts", "Medium"],
    ]
    new_docs_table = Table(new_docs_data, colWidths=[0.4 * inch, 2.2 * inch, 2.6 * inch, 0.8 * inch])
    new_docs_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#16213e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f5f5fa')]),
        ('GRID', (0, 0), (-1, -1), 0.25, HexColor('#999999')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(new_docs_table)
    story.append(Spacer(1, 16))

    story.append(Paragraph("Documents to Expand Rather Than Create New", h2_style))
    expand_data = [
        ["Existing doc", "What to add"],
        ["21-sd-tcl-query-processor.md", "COUNT, SUM, LIST.ITEM, SORT.ITEM, REFORMAT, SREFORMAT, SEARCH, SHOW"],
        ["24-sd-tcl-programs-and-the-catalogue.md", "COMPILE, BASIC verbs"],
        ["28-sd-tcl-printing-and-spooling.md", "LIST.LABEL, SORT.LABEL"],
        ["29-sd-tcl-the-terminal-and-the-session.md", "Terminfo overview"],
        ["34-sd-dicts-conversions.md", "Full format specification syntax"],
    ]
    expand_table = Table(expand_data, colWidths=[2.5 * inch, 3.5 * inch])
    expand_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 8.5),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#0f3460')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f5f5fa')]),
        ('GRID', (0, 0), (-1, -1), 0.25, HexColor('#999999')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(expand_table)
    story.append(Spacer(1, 16))

    # Excluded proposals
    story.append(Paragraph("Features Excluded from All Proposals", h1_style))
    story.append(Paragraph(
        "The following were in the original analysis but have been removed "
        "because SD Core for Windows does not ship them:",
        body_style
    ))

    removed_data = [
        ["Removed proposal", "Reason"],
        ["39-sd-networking.md (QMNet)",
         "QMNet removed: netfiles.c deleted, server;file handling removed, NETFILES parameter inert"],
        ["41-sd-python.md (Python integration)",
         "Embedded Python removed: sdext_py.c deleted, OP_SDPYOBJ retired, Makefile drops Python headers and linker flags"],
        ["48-sd-connections.md (connection types incl. UDS)",
         "UDS is Unix-only; connection types folded into the Client API doc (local and TCP only)"],
        ["sdlnxd daemon references",
         "Linux-only background daemon, no Windows equivalent"],
        ["ENCRYPT.FIELD verb",
         "VOC entry removed, pointed at non-existent $CRYPTO"],
        ["/etc/sd.conf path references",
         "Linux path; Windows uses a different configuration file location"],
        ["sd -start / sd -stop / sd -restart with sudo",
         "Linux invocation; Windows uses the service or command without sudo"],
        ["chmod, chown, kill -9, /etc/group, /home/sd/ paths",
         "Linux-specific commands and paths"],
    ]
    removed_table = Table(removed_data, colWidths=[2.2 * inch, 3.8 * inch])
    removed_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#8B0000')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#fff5f5')]),
        ('GRID', (0, 0), (-1, -1), 0.25, HexColor('#999999')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(removed_table)

    # What is already well covered
    story.append(Spacer(1, 16))
    story.append(Paragraph("What Is Already Well Covered", h1_style))
    story.append(Paragraph(
        "The current SD Core docs are strong on:",
        body_style
    ))
    for item in [
        "<b>SDBasic language</b> (01-18): comprehensive coverage of statements, functions, and concepts",
        "<b>TCL commands</b> (19-31): good coverage of the core command set, editor, and session management",
        "<b>VOC</b> (32): thorough structure and usage guide",
        "<b>Dictionaries</b> (33-34): record types, fields, conversions, and formatting",
        "<b>Syntax references</b> (94-95): BASIC and TCL syntax",
    ]:
        story.append(Paragraph(f"&bull; {item}", bullet_style))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "The main gaps are in <b>system administration</b>, "
        "<b>installation</b>, and <b>SD-specific features</b> "
        "(Client API, encryption, SDEXT, terminfo) - the things that go "
        "beyond the programming language and command layer.",
        body_style
    ))

    return story


def main():
    # Ensure output directory exists
    out_dir = os.path.dirname(OUTPUT_PATH)
    os.makedirs(out_dir, exist_ok=True)

    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=letter,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
        title="SD Core for Windows - Documentation Change Proposals",
        author="SD Core Documentation Team",
        subject="Gap analysis and proposals for new and expanded documentation",
    )

    story = build_story()
    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"PDF created: {OUTPUT_PATH}")


if __name__ == '__main__':
    main()

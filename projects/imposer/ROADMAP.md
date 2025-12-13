# Imposer Roadmap & Feature Ideas

## Version History

### v0.3.0-beta (December 2, 2025)
**N-up Enhancements & Print Functionality**
- [x] **Manual grid tile count fix** - Now correctly fills entire grid (cols × rows) instead of limiting to n
- [x] **N-up fit mode option** - Choose between "Constrain proportions" (maintain aspect ratio) or "Stretch to fit" (fill entire cell)
- [x] **N-up orientation control** - Portrait/Landscape selector swaps sheet dimensions for any selected size
- [x] **Booklet mode** - Automatic page reordering for booklet printing with padding to multiples of 4
- [x] **Print functionality** - Direct print button opens system print dialog for imposed PDFs

### v0.2.0-beta (Prior Release)
**Phase 1 Features Complete**
- [x] Add US size presets (Half Letter, 12×18, 13×19, 17×22, 19×25, 20×26)
- [x] Update N-up dropdown/mapping for new sizes
- [x] Update Multi-up dropdown/mapping for new sizes
- [x] Center Multi-up tiles within margins
- [x] Fix N-up variable (`n: nup`) and preview rendering
- [x] Add layout rows×cols indicator to Multi-up
- [x] **Drag-drop batch file merge** - Added drag-and-drop zone accepting PDF, Word, JPG, PNG files with merge functionality
- [x] **Page range resize** - Added mode selector for single page, page range, or all pages resize
- [x] **Direct Cols×Rows N-up input** (Phase 1) - Manual grid mode with cols/rows inputs to override auto grid calculation
- [x] **Profiles & presets manager** (Phase 1) - Save/load imposition settings to JSON files with full state preservation
- [x] **Slug area with job metadata** (Phase 1) - Optional slug zone showing job name, timestamp, and sheet number
- [x] **Advanced registration marks** (Phase 1) - Enhanced marks with corner+center cross style and configurable diameter
- [x] **Waste % calculation display** (Phase 1) - Calculate and show unused sheet area percentage after imposing
- [x] **Side-by-side preview toggle** (Phase 1) - Split preview layout to show original and imposed side-by-side
- [x] **Word document support** - Accept and convert .docx and .doc files to PDF (basic text extraction)
- [x] **Author information** - Added business details to About dialog

### v0.4.1-beta (Current Release)
**Multi-up Pipeline & Print Fix**
- [x] **Multi-up staging pipeline integration** - Fixed race condition in operation queue, proper preview rendering
- [x] **Zero margin/gap handling** - Explicit numeric checks to preserve user-set zero values
- [x] **Render task cancellation** - Stable PDF.js preview updates during window resize
- [ ] **Print functionality restoration** - Fix print button (stopped working in previous versions)

## Current Status

**Latest Version:** 0.4.1-beta  
**Focus:** Stability fixes and print workflow restoration  
**Next Priority:** Print feature fix, Phase 2 features (see below)

### In Progress / Planned
- [ ] **Print feature fix** - Restore print dialog functionality (stopped working in v0.3.5 - v0.4.0)
  - Investigation needed: Electron API changes, BrowserWindow.webContents.print status
  - Priority: High (user workflow critical)
- [ ] **Phase 2 features** - See Phase 2 section below for next priorities
- [ ] **Marketing Assets** - Screenshots, logo, demo videos for public repository and promotion

---

## Feature Ideas from Print Industry Research

### Core Imposition Enhancements
- **Work-and-Turn / Tumble / Sheetwise Modes**: Presets for common commercial press imposition styles
  - Value: Speeds setup for standard print workflows
  - Complexity: Medium (page position mirroring)

- **Booklet Signatures + Creep/Shingling**: Automatically adjust inner pages outward to compensate spine thickness
  - Value: Professional finishing quality
  - Complexity: Medium (needs thickness model)

- **Step-and-Repeat (Labels/Packaging)**: Uniform grid + optional bleed/dieline overlay
  - Value: Label and packaging jobs
  - Complexity: Low–Medium

- **Ganging Multiple PDFs**: Combine different page sizes on one sheet to minimize waste
  - Value: Material savings
  - Complexity: High (bin packing algorithm)

- **Mixed Orientation Auto-Optimization**: Rotate pages to maximize fit within sheet constraints
  - Value: Improved sheet usage
  - Complexity: Medium

### Print Marks & Standards
- **Advanced Registration Marks Set**: Corner marks + center cross + custom diameter
  - Value: Alignment accuracy
  - Complexity: Low

- **Color Bars / Control Strips (FOGRA / ISO 12647)**: Optional density/control patches added to slug zone
  - Value: Press calibration and QC
  - Complexity: Medium (static assets)

- **Crop / Fold / Perforation / Die Marks**: Layered mark types for finishing
  - Value: Downstream clarity
  - Complexity: Low

- **Slug Area with Job Metadata**: Job name, timestamp, version, sheet #
  - Value: Traceability
  - Complexity: Low

- **Page Numbering (Header/Footer)**: Optional page numbers on imposed output with position (corners/center), font, size, opacity
  - Value: Easier navigation and proof review
  - Complexity: Low

- **Barcode / QR (Job Ticket)**: Encode job ID / MIS reference
  - Value: Tracking and automation
  - Complexity: Low (library: `jsbarcode` or `qrcode`)

- **Ink Coverage Estimation (Rough)**: Simple heuristic scanning rasterized page to report CMYK %
  - Value: Estimating ink usage
  - Complexity: High (color conversion)

### Workflow & Automation
- **Batch / CLI Mode**: JSON config → imposed PDF output
  - Value: Integration in pipelines
  - Complexity: Medium

- **Hot Folder Watcher**: Drop PDFs into watched folder → auto impose by profile
  - Value: Automation
  - Complexity: Medium (fs watching)

- **Profiles & Presets Manager**: Save/load imposition settings (JSON)
  - Value: Repeatability
  - Complexity: Low

- **Template-Based Layout Export**: Export layout geometry as JSON for MIS/JDF
  - Value: Interoperability
  - Complexity: Medium

- **Versioned Configs**: Track changes across saved profiles
  - Value: Audit trail
  - Complexity: Low

### Marketing & Visual Assets
- **Application Screenshots**: Capture key features for marketing materials
  - Main interface with loaded PDF
  - N-up layout configuration
  - Booklet mode demonstration
  - Registration marks output
  - Profile manager
  - Value: Marketing and user onboarding
  - Complexity: Low (just needs time)

- **Logo & Branding**: Professional logo and icon for application
  - Application icon (.ico for Windows)
  - GitHub repository icon
  - Marketing materials logo
  - Value: Brand recognition
  - Complexity: Low (design work)

- **Demo Videos**: Screen recordings showing key workflows
  - Basic N-up imposition workflow
  - Booklet creation from start to finish
  - Advanced features (marks, profiles, etc.)
  - Value: Marketing and tutorials
  - Complexity: Low (screen recording + editing)

- **Feature Comparison Chart**: Visual comparison with competitors
  - Highlight unique features
  - Pricing comparison (when available)
  - Value: Sales/marketing
  - Complexity: Low (design work)

### Preflight & Quality
- **PDF/X Compliance Check (Basic)**: Validate color spaces, embedded fonts, transparency warnings
  - Value: Professional output
  - Complexity: Medium

- **Bleed Detection & Warning**: Flag pages lacking requested bleed margin
  - Value: Print readiness
  - Complexity: Low

- **Image Resolution Audit**: List images below threshold (e.g. < 150 DPI)
  - Value: Quality assurance
  - Complexity: Medium

- **Font Embedding Check**: Warn on missing embedded fonts
  - Value: Output reliability
  - Complexity: Medium

- **Trim Safety Overlay**: Semi-transparent margin overlay in preview
  - Value: Visual validation
  - Complexity: Low

### Advanced Optimization
- **Auto Sheet Size Suggestion**: Given page dims + target n-up, propose minimal standard sheet meeting constraints
  - Value: Efficiency
  - Complexity: Medium

- **Waste % Calculation**: Report unused sheet area
  - Value: Cost optimization
  - Complexity: Low

- **Packing Solver (Heuristic)**: For mixed sizes, run simple simulated annealing / greedy
  - Value: Material savings
  - Complexity: High

- **Rotation/Flip Combinator**: Test rotations per page to reduce waste
  - Value: Optimization
  - Complexity: Medium–High

- **Cost Estimator (Configurable)**: Quick sheet cost, ink coverage factor, finishing surcharge
  - Value: Quoting
  - Complexity: Medium

### UI / UX Enhancements
- **Side-by-Side Original vs Imposed Preview**: Toggle split view
  - Value: Clarity
  - Complexity: Low

- **Live Layout Grid Overlay**: Show cell lines before generation
  - Value: Instant feedback
  - Complexity: Low

- **Direct Cols×Rows Input for N‑up**: Override auto grid
  - Value: Control
  - Complexity: Low

- **Inline Errors Panel (Preflight)**: Consolidated warnings
  - Value: Usability
  - Complexity: Low

- **Dark Mode & Scaling**: Better readability
  - Value: Accessibility
  - Complexity: Low

- **Page Resize Presets (US Print Sizes)**: Quick-select dropdown for common US sizes with/without bleed (Letter, Half-Letter, Tabloid, etc.)
  - Value: Accelerates setup; reduces manual entry
  - Complexity: Low

### Packaging / Specialty
- **Dieline Import (SVG/PDF)**: Overlay cut lines in step-and-repeat
  - Value: Packaging workflows
  - Complexity: Medium

- **Variable Data Merge**: CSV to numbered tickets/imposed sheets
  - Value: Numbering & mailing
  - Complexity: High

- **Serial / Lot Number Stamp**: Auto increment marks
  - Value: Product tracking
  - Complexity: Medium

- **Spot Color / Pantone Flagging**: List spot inks present
  - Value: Press setup
  - Complexity: Medium

### Integration / Standards
- **JDF Export (Lite)**: Provide imposition specs (sheet size, page map)
  - Value: MIS integration
  - Complexity: High (subset)

- **CIP3 PPF Stub**: Output basic ink zone file placeholder
  - Value: Future press optimization
  - Complexity: High

- **REST API Mode**: Electron backend served via local API for network clients
  - Value: Remote automation
  - Complexity: Medium

---

## Prioritized Starter Roadmap

### Phase 1 (Low Complexity - Quick Wins) ✅ COMPLETED
- [x] Direct Cols×Rows N-up input
- [x] Profiles & presets manager (save/load settings)
- [x] Slug area with job metadata
- [x] Advanced registration marks
- [x] Waste % calculation display
- [x] Side-by-side preview toggle

### Phase 2 (Medium Complexity) - NEXT PRIORITY
- Color bars and control strips
- Bleed & resolution preflight checks
- Batch CLI mode
- Hot folder watcher
- Auto sheet size suggestion
- Step-and-repeat for labels
- **Custom Watermark for Customer Proofs**: Add configurable watermark (text/image) overlay on proof outputs
  - Value: Prevents unauthorized use of proof PDFs
  - Complexity: Medium (overlay positioning, opacity, rotation)
- **Page Numbering Overlay**: Optional page numbers (footer/header) with position and style
  - Value: Improves navigation and proof review clarity
  - Complexity: Low (text overlay per page)
- **Page Resize Presets**: Pre-built US print size options (with/without bleed) for quick selection
  - Value: Faster setup; eliminates manual dimension lookup
  - Complexity: Low### Phase 3 (Higher Complexity)
- Creep/Shingling for booklets
- Basic ganging solver
- Variable data merge (numbering)
- Work-and-Turn / Tumble modes
- Dieline import for packaging

### Phase 4 (Advanced Features)
- JDF export
- Packing optimization heuristics
- Ink coverage estimation
- PDF/X compliance suite
- REST API mode

---

## Potential Dependencies
- **Barcode/QR**: `jsbarcode` or `qrcode`
- **PDF/X / Preflight**: Custom checks using `pdf-lib` (full compliance is larger scope)
- **Variable Data**: `papaparse` for CSV parsing
- **Color Bars / Marks**: Static SVG assets integrated into draw routines
- **Optimization Solver**: Custom heuristic module (greedy + optional metaheuristics)
- **Hot Folder**: `chokidar` for file system watching

---

## Notes
- Current version: 0.2.0-beta
- Repository: https://github.com/artichoku/imposer
- Author: Leondas Paul, III (Galilee Gallery / One Stop Vape and Print Shop, LLC)
- Tagged: v0.2.0-beta
- Last updated: December 2, 2025

## Recent Development Summary (Dec 2025)
### Session Accomplishments:
1. **Phase 1 Features (Complete)**: All 6 quick-win features implemented and tested
2. **Batch File Merge**: Drag-drop zone with support for PDF, Word, images
3. **Page Range Operations**: Single page, range, or all pages resize capability
4. **Word Document Support**: Basic .docx/.doc conversion using mammoth library
5. **Profile Management**: Save/load complete imposition settings to JSON
6. **Enhanced Marks**: Advanced registration marks with corner+cross+diameter options
7. **Optimization Metrics**: Real-time waste percentage calculation display
8. **UI Improvements**: Split preview toggle, manual grid input, slug metadata

### Technical Implementation:
- **Backend (main.js)**: Added manualGrid support, advanced mark rendering, slug metadata, Word conversion handlers
- **Frontend (src/renderer.js)**: Added 11 new state variables, profile save/load functions, waste calculation, split preview layout
- **Preload (preload.js)**: Exposed file dialog APIs for profile management
- **Dependencies**: Added mammoth for Word document processing

### Known Limitations:
- Word document conversion is basic text extraction (no complex formatting, images, or tables)
- PDF.js worker warnings are non-critical and handled with fallbacks
- Advanced marks only show when crop marks are enabled

### Next Steps (Phase 2):
Focus on medium-complexity features: color bars, preflight checks, CLI mode, hot folder automation

## Release Checklist (for future releases)
See inline documentation for full preflight, build, and release validation steps.

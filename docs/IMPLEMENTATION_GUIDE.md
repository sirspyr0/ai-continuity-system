# AI Continuity System - Implementation Guide

## Quick Start (5 Minutes)

### For an Existing Project

1. **Create `PROJECT_CONTEXT.md` in project root:**

```markdown
# PROJECT_CONTEXT: [Your Project Name]

## Overview

[1-2 sentence description of what this project does]

## Current Status

- **Version:** X.Y.Z
- **Release Status:** [Alpha/Beta/Stable]
- **Last Updated:** YYYY-MM-DD

## Quick Overview for New Instances

[What should a fresh AI instance know immediately? 2-3 bullet points]

## Architecture

### Tech Stack
- [Framework 1]
- [Framework 2]
- [Database]

### Key Architecture Decisions

**Decision 1:** [What] Because [why]
**Decision 2:** [What] Because [why]

### Project Structure

```
src/
├── index.js       // Entry point
├── core/          // Core logic
└── ui/            // User interface
```

## Current Blockers

- [ ] [Blocker 1] - Blocked by external: X
- [ ] [Blocker 2] - Blocked by internal: Y

## Key Files (By Importance)

1. `src/core/main.js` - Core logic, most important
2. `src/ui/render.js` - UI rendering
3. `config.json` - Configuration

## Development Workflow

### Running Locally
```bash
npm install
npm start
```

### Running Tests
```bash
npm test
```

### Deploying
[Steps for deployment]

## Decision History

### Why React Instead of Vue?
[Context and reasoning that explains this choice]

### Why PostgreSQL Instead of MongoDB?
[Context and reasoning that explains this choice]

## Links to Related Projects

- [Related Project A](../other-project/PROJECT_CONTEXT.md)
- [Related Project B](../other-project-b/PROJECT_CONTEXT.md)
```

2. **Create `SESSION_BRIEFING.md` in project root:**

```markdown
# Session Briefing: [Project Name]

## What You're Walking Into

You're continuing work on [short description]. The current status is:

**Last completed:** [What instance N-1 just finished]
**Current blocker:** [What's preventing progress]
**Next goal:** [What should be done next]

## Immediate Action Items

1. [Task 1 - most important]
2. [Task 2]
3. [Task 3]

## How to Get Productive in 15 Minutes

1. Read this briefing (5 min)
2. Read SESSION_LOG.md recent entries (10 min)
3. You're ready to code

## Key Files Changed Recently

- `src/component/X.js` - Modified for feature Y
- `tests/Z.test.js` - Updated with new test cases

## Current Test Status

```
$ npm test

Tests: 47 passed, 2 failed
Coverage: 82%

Failing tests:
- [test name] - Blocker description
- [test name] - Blocker description
```

## For More Context

Read `SESSION_LOG.md` for detailed work history from previous instances.
Read `PROJECT_CONTEXT.md` for architecture and decision history.
```

3. **Create `SESSION_LOG.md` in project root:**

```markdown
# Session Log: [Project Name]

## Active Sessions

### Current Session (Instance #1 - 2025-12-07)

**Starting Context:**
[What did you find when you opened this session?]

**Work Accomplished:**

- [Accomplishment 1 with details]
- [Accomplishment 2]
- [Accomplishment 3]

**Code Changes:**
- `src/file.js`: [What changed and why]
- `tests/file.test.js`: [What changed]

**Blockers Encountered:**
- [Blocker 1]: Description of issue and attempted solutions
- [Blocker 2]: Description of issue

**Decisions Made:**
- [Decision 1]: Chose X over Y because Z
- [Decision 2]: Chose approach A because B

**For Next Instance:**

- **Immediate next step:** [Specific task to continue with]
- **Quick context:** [1-2 sentences about current state]
- **Updated briefing in:** SESSION_BRIEFING.md
- **Test status:** [Pass rate and critical failures]
```

4. **In your `package.json`, ensure you have a git hook or reminder:**

```json
{
  "scripts": {
    "session-start": "echo 'SESSION_LOG.md and SESSION_BRIEFING.md are your handoff files'",
    "session-end": "echo 'Before committing: update SESSION_LOG.md and SESSION_BRIEFING.md'"
  }
}
```

5. **Git workflow:**

```bash
# Make your changes
git add .

# Update SESSION_LOG.md to document what you did
# Update SESSION_BRIEFING.md to show new status

# Commit with a message that references SESSION_LOG.md
git commit -m "Implement feature X

- Added component Y
- Fixed bug Z

See SESSION_LOG.md for detailed context of this work."

# Push to remote
git push
```

## Full Implementation (30 Minutes)

### Step 1: Project Context (10 minutes)

Create a comprehensive `PROJECT_CONTEXT.md`:

**Include:**
- [ ] Project overview (what does it do?)
- [ ] Current version
- [ ] Tech stack with rationale
- [ ] Architecture explanation
- [ ] File structure with purpose of main files
- [ ] Known limitations
- [ ] How to run locally
- [ ] How to run tests
- [ ] Decision history (important "why" questions)

**Avoid:**
- Don't include step-by-step tutorials (that's PROJECT_CONTEXT.md's job)
- Don't include current work status (that's SESSION_BRIEFING.md's job)

### Step 2: Initial Session Briefing (5 minutes)

Create `SESSION_BRIEFING.md`:

**Include:**
- [ ] What's currently being worked on
- [ ] What was just completed
- [ ] Immediate next steps (top 3)
- [ ] Current blockers
- [ ] Test status

**Make it scannable:**
- Use bullet points
- Lead with the most important info
- Keep to 1-2 pages max

### Step 3: Initialize Session Log (5 minutes)

Create `SESSION_LOG.md` with starter template:

```markdown
# Session Log: [Project Name]

## Active Sessions

### Setup Session (Instance #0 - [date])

**Starting Context:**
Initializing continuity system for this project.

**Work Accomplished:**
- Created PROJECT_CONTEXT.md with full architecture documentation
- Created SESSION_BRIEFING.md with current status
- Initialized SESSION_LOG.md

**For Next Instance:**
- All setup complete
- Ready to begin feature work
- See SESSION_BRIEFING.md for immediate tasks
```

### Step 4: First Commit

```bash
git add PROJECT_CONTEXT.md SESSION_BRIEFING.md SESSION_LOG.md
git commit -m "Initialize AI continuity system

- Created PROJECT_CONTEXT.md with architecture
- Created SESSION_BRIEFING.md with current status
- Created SESSION_LOG.md for work tracking

This enables seamless handoff between AI instances."

git push
```

## Maintenance Guide

### After Every Session

**Must Do:**
1. Update SESSION_LOG.md with work accomplished
2. Update SESSION_BRIEFING.md with new status
3. Commit both files

**Good To Do:**
1. Check if PROJECT_CONTEXT.md needs updates (architecture changes)
2. Review SESSION_LOG.md entry for clarity
3. Make sure next steps are clear in SESSION_BRIEFING.md

### Weekly Review

1. Read through SESSION_LOG.md entries from the week
2. Update PROJECT_CONTEXT.md with any architecture decisions made
3. Check if blockers in SESSION_LOG.md are still accurate
4. Make sure SESSION_BRIEFING.md reflects current priorities

### Monthly Review

1. Review all SESSION_LOG.md entries for the month
2. Update PROJECT_CONTEXT.md decision history
3. Check if tech stack rationale is still accurate
4. Consider archiving old SESSION_LOG.md entries if file gets too long

## Examples

### Example SESSION_LOG.md Entry

```markdown
### Current Session (Instance #5 - 2025-12-10)

**Starting Context:**
Found incomplete API tests. Test suite had 3 failing tests from previous instance.
Previous instance documented that pagination endpoint was incomplete.

**Work Accomplished:**

- Fixed pagination endpoint in `src/api/routes.js`
  - Issue: Offset/limit parameters weren't validated
  - Solution: Added input validation before database query
  - Why: Invalid parameters were causing database errors

- Completed API tests in `tests/api.test.js`
  - Added 5 new test cases for pagination
  - All tests now passing (47 passed, 0 failed)
  - Coverage improved from 78% to 82%

- Fixed bug in response formatting
  - Issue: Pagination metadata wasn't included in response
  - Solution: Added `metadata` field to API response
  - Tested with curl to verify structure

**Code Changes Summary:**

```diff
// src/api/routes.js
- app.get('/api/items', (req, res) => {
+ app.get('/api/items', validatePagination, (req, res) => {
  const { offset, limit } = req.query;
  // ...
+ res.json({ data: items, metadata: { offset, limit, total } });
```

**Blockers Encountered:**

- Expected blocker: Documentation on pagination format was unclear
  - Solved by: Reading previous instance's notes in SESSION_LOG.md
  - Resolution: Now documented in API schema

**Decisions Made:**

- **Chose pagination validation middleware** over inline validation
  - Reason: More reusable, consistent with existing patterns
  - Reference: See PROJECT_CONTEXT.md for architecture decision on middleware pattern

**For Next Instance:**

- **Immediate next steps:**
  1. Write client library wrapper for pagination endpoint
  2. Add rate limiting middleware
  3. Document API response structure

- **Quick status:** All core API endpoints now implemented and tested. No failing tests. Ready for client integration.
- **Updated briefing at:** SESSION_BRIEFING.md
- **Test status:** 47 passing, 0 failing, 82% coverage
```

### Example SESSION_BRIEFING.md

```markdown
# Session Briefing: User API Service

## What You're Walking Into

You're implementing the user API service for our platform. Previous instances have completed:
- Core API endpoints (GET, POST, PUT, DELETE)
- Pagination with proper validation
- Test suite with 82% coverage
- All 47 tests passing

**Current blocker:** Client library needs to be written
**Next goal:** Implement client-side wrapper with error handling

## Immediate Action Items

1. **Write client library** (`src/client/api.js`)
   - Wrapper around fetch API
   - Handles pagination
   - Proper error handling
   - Takes 1-2 hours

2. **Test client library** against running API
   - Spin up local API: `npm start`
   - Run client tests: `npm test:client`
   - Should take 30 minutes

3. **Document client usage** in README.md
   - Code examples
   - Common patterns
   - Error handling patterns
   - Takes 20 minutes

## How to Get Productive in 15 Minutes

1. **Read this briefing (2 min)** - You're reading it now
2. **Skim SESSION_LOG.md recent entry (5 min)** - Understand what was just done
3. **Review src/client/api.js stub (3 min)** - See what needs to be implemented
4. **Run API locally (5 min)** - Verify it's working
5. **You're ready to code!**

## Quick Reference

**To run locally:**
```bash
npm install  # If first time
npm start    # Start API server on localhost:3000
```

**To run tests:**
```bash
npm test     # Run all tests
npm test:watch  # Run in watch mode
```

**API endpoints (already implemented):**
- GET /api/items?offset=0&limit=10 - List items with pagination
- POST /api/items - Create new item
- GET /api/items/:id - Get specific item
- PUT /api/items/:id - Update item
- DELETE /api/items/:id - Delete item

## Current Test Status

```
API tests: 47 passed, 0 failed
Coverage: 82%
Client tests: Waiting for implementation
```

## Key Files

1. **src/api/routes.js** - API implementation (complete)
2. **src/client/api.js** - Client wrapper (stub, needs implementation)
3. **tests/api.test.js** - API tests (complete, all passing)
4. **tests/client.test.js** - Client tests (written, waiting for client impl)

## For More Context

Read `SESSION_LOG.md` for detailed history of what was done.
Read `PROJECT_CONTEXT.md` for architecture decisions and rationale.
```

## Troubleshooting

### Problem: SESSION_LOG.md Gets Too Long

**Solution:** Archive old sessions

```markdown
# Session Log: [Project Name]

## Active Sessions

[Current session...]

## Previous Sessions

For complete history, see [ARCHIVE.md](./docs/ARCHIVE.md)

### Recent (Last 5 Sessions)

[Last 5 session summaries...]
```

### Problem: Fresh Instance Doesn't Understand Context

**Fix:**
1. SESSION_BRIEFING.md too vague → Be more specific
2. SESSION_LOG.md too detailed → Summarize key points
3. PROJECT_CONTEXT.md not updated → Update architecture section

### Problem: SESSION_BRIEFING.md Gets Out of Date

**Prevention:**
- Always update SESSION_BRIEFING.md after work
- Add to your checklist: "Is SESSION_BRIEFING.md accurate?"
- In code review: "Does SESSION_BRIEFING.md match the code status?"

## Best Practices

1. **Keep SESSION_BRIEFING.md to 1-2 pages**
   - Next instance should understand in 15 minutes
   - If it's longer, move details to PROJECT_CONTEXT.md

2. **Make SESSION_LOG.md entries scannable**
   - Use bullet points
   - Lead with summaries
   - Save detailed explanations for code comments

3. **Update both files in the same commit**
   - `git commit -m "Work description
     - Change 1
     - Change 2
     Updated SESSION_LOG.md and SESSION_BRIEFING.md"`

4. **Reference your files in the README**
   ```markdown
   ## For AI Continuity

   - **SESSION_BRIEFING.md** - Quick orientation for fresh instances
   - **SESSION_LOG.md** - Detailed work history
   - **PROJECT_CONTEXT.md** - Architecture and decisions
   ```

5. **Add session reminder to your scripts**
   ```json
   {
     "scripts": {
       "poststart": "echo '📝 Remember to update SESSION_LOG.md and SESSION_BRIEFING.md before committing'"
     }
   }
   ```

## Checking Your Work

Before each commit, run this checklist:

- [ ] Code changes are meaningful and tested
- [ ] SESSION_LOG.md is updated with what I did
- [ ] SESSION_BRIEFING.md reflects new status
- [ ] Both files are committed with the code changes
- [ ] Commit message references SESSION_LOG.md
- [ ] Next steps are clear in SESSION_BRIEFING.md

## Next Steps

1. Copy the templates from this guide into your project
2. Customize them for your specific project
3. Make your first commit with all three files
4. Start documenting your work in SESSION_LOG.md
5. After each session, update SESSION_BRIEFING.md

You're now set up for multi-instance continuity!

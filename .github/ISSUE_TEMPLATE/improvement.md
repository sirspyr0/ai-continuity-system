name: Improvement Suggestion
about: Suggest improvements to the AI Continuity System
title: "Improvement: [Your Suggestion]"
labels: ["enhancement"]

body:
  - type: markdown
    attributes:
      value: "## Your Suggestion"
  - type: textarea
    id: problem
    attributes:
      label: "What problem does this solve?"
      placeholder: "Describe the current limitation or issue"
    validations:
      required: true
  - type: textarea
    id: solution
    attributes:
      label: "Your proposed solution"
      placeholder: "How would you improve the system?"
    validations:
      required: true
  - type: textarea
    id: benefits
    attributes:
      label: "What are the benefits?"
      placeholder: "How would this improve the system?"
    validations:
      required: true
  - type: textarea
    id: tradeoffs
    attributes:
      label: "What are the trade-offs?"
      placeholder: "What would be the downsides or costs?"
    validations:
      required: false

name: Implementation Question
about: Ask how to implement this system in your project
title: "How to implement AI Continuity System for [PROJECT_NAME]"
labels: ["question", "implementation"]

body:
  - type: markdown
    attributes:
      value: "## Your Question"
  - type: textarea
    id: question
    attributes:
      label: "What are you trying to implement?"
      placeholder: "Describe the specific aspect of the continuity system you want help with"
    validations:
      required: true
  - type: textarea
    id: project_context
    attributes:
      label: "Tell us about your project"
      placeholder: "Project type, tech stack, current state"
    validations:
      required: false
  - type: markdown
    attributes:
      value: "## What have you tried?"
  - type: textarea
    id: attempted
    attributes:
      label: "What have you already attempted?"
      placeholder: "Describe any attempts you've made"
    validations:
      required: false

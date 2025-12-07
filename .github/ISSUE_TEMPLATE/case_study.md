name: Case Study
about: Share how you implemented the AI Continuity System
title: "Case Study: [Your Implementation]"
labels: ["case-study", "success"]

body:
  - type: markdown
    attributes:
      value: "## Your Implementation Story"
  - type: textarea
    id: overview
    attributes:
      label: "Project Overview"
      placeholder: "What is your project and what tech stack does it use?"
    validations:
      required: true
  - type: textarea
    id: implementation
    attributes:
      label: "How did you implement the system?"
      placeholder: "What files did you create? How did you integrate it?"
    validations:
      required: true
  - type: textarea
    id: results
    attributes:
      label: "What were the results?"
      placeholder: "Productivity gains, lessons learned, metrics"
    validations:
      required: true
  - type: textarea
    id: challenges
    attributes:
      label: "Challenges and How You Solved Them"
      placeholder: "What was difficult? How did you overcome it?"
    validations:
      required: false
  - type: textarea
    id: recommendations
    attributes:
      label: "Recommendations for Others"
      placeholder: "What would you tell others trying to implement this?"
    validations:
      required: false

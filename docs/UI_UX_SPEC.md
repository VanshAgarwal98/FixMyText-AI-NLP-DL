# UI/UX Specification — FixMyText AI

## Brand palette (from supplied reference)
- Primary / deep teal: `#2b6777`
- Secondary / pale blue: `#c8d8e4`
- Canvas / white: `#ffffff`
- Soft background: `#f2f2f2`
- Accent / mint green: `#52ab98`

## Color usage
- Primary actions, sidebar, headings: deep teal.
- Secondary panels and quiet emphasis: pale blue.
- Cards and form surfaces: white.
- Main page canvas: light gray.
- Positive actions, selected states, chart accents: mint green.
- Maintain readable contrast; never use pale blue for small white text.

## Layout
- Persistent sidebar navigation.
- Wide content canvas with clear page title and subtitle.
- Hero panel with a teal-to-mint gradient.
- Four metric cards across the dashboard on wide screens.
- Two-column charts when space allows.
- Single-column forms and tables on narrow displays.

## Components
- Hero banner: title, short explanatory text.
- Metric card: label and large value.
- Form fields with descriptive labels and example placeholders.
- Primary button: teal background, white text.
- Status chips: use text labels as well as color.
- Empty states: explain what is missing and provide a next action.
- Error states: say what went wrong and how to recover.
- Low-confidence state: clearly recommend manual review.

## Accessibility
- Do not rely on color alone to convey status.
- Keep labels visible.
- Use meaningful button text.
- Maintain keyboard navigation through Streamlit controls.
- Keep body copy readable and avoid tiny text.
- Charts should have clear titles and axis labels.

## UX principles
- Fast submission with minimal required fields.
- Show the prediction only after model inference.
- Explain that model output is a suggestion.
- Keep potential similarity separate from confirmed duplication.
- Admin changes should visibly persist and be auditable.

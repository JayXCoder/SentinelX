# SentinelX — task.md for Geng Xin

## Owner

**Geng Xin**

## Assigned Scope

Geng Xin is responsible for the UI/UX system and frontend experience together with Raymond.

Geng Xin focuses mainly on:

- UI/UX systems
- reusable frontend components
- design systems
- responsive layouts
- real-time interaction design
- dashboard visual consistency
- frontend user experience

Geng Xin owns the visual and interaction layer of SentinelX.

---

# 1. Main Objective

Build the design system and frontend interaction experience for SentinelX.

The goal is to make SentinelX feel like a professional enterprise-grade intelligence platform.

The UI must:

- look modern
- feel responsive
- support large amounts of intelligence data
- support real-time updates
- remain readable and structured
- provide clear intelligence visualization
- support executive-level usage

Geng Xin’s work should ensure:

- consistent design language
- reusable components
- scalable UI architecture
- responsive behavior
- accessible interaction design

---

# 2. Technology Stack

Geng Xin’s assigned frontend stack:

- Next.js
- TypeScript
- Tailwind CSS v4
- React
- Docker

Optional libraries:

- Recharts
- Framer Motion
- TanStack Table
- React Icons
- Lucide React
- clsx
- tailwind-merge

---

# 3. Frontend Responsibilities

Geng Xin needs to build these frontend areas:

## 3.1 Design System

Responsible for:

- color palette
- typography system
- spacing system
- visual hierarchy
- theme consistency
- UI standards

## 3.2 Reusable Components

Responsible for:

- cards
- buttons
- tables
- charts
- alerts
- modals
- badges
- navigation components
- notification components
- loading components

## 3.3 Real-Time UI Interactions

Responsible for:

- live notifications
- toast systems
- animated updates
- streaming UI behavior
- dashboard responsiveness

## 3.4 Dashboard UX

Responsible for:

- usability
- layout clarity
- responsive design
- accessibility
- dashboard readability
- interaction consistency

---

# 4. Suggested Folder Structure

```text
sentinelx-frontend/
├── components/
│   ├── ui/
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── input.tsx
│   │   ├── textarea.tsx
│   │   ├── modal.tsx
│   │   ├── badge.tsx
│   │   ├── tabs.tsx
│   │   ├── dropdown.tsx
│   │   ├── tooltip.tsx
│   │   ├── toast.tsx
│   │   ├── loading.tsx
│   │   └── skeleton.tsx
│   ├── dashboard/
│   │   ├── metric-card.tsx
│   │   ├── score-card.tsx
│   │   ├── event-feed.tsx
│   │   ├── vendor-card.tsx
│   │   ├── signal-card.tsx
│   │   ├── intelligence-summary.tsx
│   │   ├── realtime-alert.tsx
│   │   └── timeline-view.tsx
│   ├── charts/
│   │   ├── line-chart.tsx
│   │   ├── bar-chart.tsx
│   │   ├── pie-chart.tsx
│   │   ├── risk-chart.tsx
│   │   └── timeline-chart.tsx
│   ├── tables/
│   │   ├── threat-table.tsx
│   │   ├── vendor-table.tsx
│   │   ├── signal-table.tsx
│   │   └── event-table.tsx
│   ├── navigation/
│   │   ├── sidebar.tsx
│   │   ├── topbar.tsx
│   │   ├── mobile-nav.tsx
│   │   └── breadcrumb.tsx
│   └── notifications/
│       ├── alert-toast.tsx
│       ├── notification-center.tsx
│       └── live-feed.tsx
├── styles/
│   ├── globals.css
│   ├── theme.css
│   └── animations.css
├── lib/
│   ├── design-system.ts
│   ├── theme.ts
│   └── animations.ts
└── README.md
```

---

# 5. Design System Requirements

## Purpose

Create a consistent enterprise-grade visual language.

The dashboard should feel:

- modern
- clean
- technical
- intelligence-focused
- executive-friendly
- professional

---

## Color Palette

Suggested categories:

### Neutral Colors

Used for:

- background
- cards
- panels
- containers
- borders

### Intelligence Colors

Suggested mapping:

```text
blue    = information
red     = critical threat
orange  = warning
green   = opportunity
purple  = executive insight
cyan    = realtime event
```

---

## Typography System

Must define:

- page titles
- section titles
- card titles
- metric values
- paragraph text
- small metadata text

Typography should prioritize:

- readability
- information density
- hierarchy clarity

---

## Spacing System

Must define:

- container spacing
- card padding
- dashboard gaps
- section margins
- responsive spacing

---

# 6. Core UI Components

## 6.1 Metric Card Component

### Purpose

Display dashboard metrics.

### Must Support

- title
- metric value
- trend direction
- percentage change
- optional icon
- optional severity state

### Example Usage

```text
Total Threats
145
+12%
```

---

## 6.2 Risk Score Card

### Purpose

Display risk scores clearly.

### Must Support

- score value
- score type
- risk level
- color-coded severity
- explanation snippet

---

## 6.3 Signal Feed Component

### Purpose

Display intelligence signals.

### Must Support

- signal title
- timestamp
- severity badge
- source label
- signal category
- expandable details

---

## 6.4 Alert Toast Component

### Purpose

Show realtime notifications.

### Must Support

- severity color
- timestamp
- short description
- dismiss button
- smooth animation

---

## 6.5 Intelligence Summary Component

### Purpose

Display executive AI-generated summaries.

### Must Support

- summary text
- confidence score
- related entities
- supporting evidence links
- recommendation section

---

# 7. Chart Requirements

Geng Xin should build reusable chart components.

## Required Charts

### Risk Trend Chart

Displays:

- risk score changes over time

---

### Threat Distribution Chart

Displays:

- threats by category
- threats by severity

---

### Vendor Risk Chart

Displays:

- vendor risk comparison
- vendor trend analysis

---

### Intelligence Timeline Chart

Displays:

- event timelines
- correlated events
- signal frequency

---

### GTM Opportunity Chart

Displays:

- opportunity ranking
- competitor movement
- market activity

---

# 8. Real-Time Interaction Requirements

## Purpose

The UI must feel live and intelligence-driven.

Users should immediately see:

- new alerts
- new risks
- new signals
- score changes
- intelligence updates

---

## Real-Time UI Features

### Live Notification Toasts

Must:

- animate smoothly
- auto-dismiss optionally
- support severity color
- stack properly

---

### Live Dashboard Updates

Must:

- refresh cards automatically
- update tables incrementally
- avoid full page reloads
- animate important changes

---

### Streaming Indicators

Must display:

- connection status
- realtime sync status
- loading indicators
- backend health indicators

---

# 9. Responsive Design Requirements

The dashboard must support:

- desktop
- laptop
- tablet
- mobile

---

## Desktop Priority

SentinelX is primarily an enterprise dashboard.

Desktop experience is highest priority.

Must support:

- wide layouts
- dense information
- multiple panels
- expandable sidebars

---

## Mobile Support

Must still support:

- responsive cards
- collapsible sidebar
- readable tables
- scrollable charts

---

# 10. Accessibility Requirements

The UI should support:

- keyboard navigation
- screen reader compatibility
- visible focus states
- readable contrast ratios
- accessible buttons

---

# 11. Animation Requirements

Animations should be:

- subtle
- smooth
- professional
- lightweight

Avoid:

- excessive motion
- distracting effects
- gaming-style animations

---

## Suggested Animation Usage

### Use animations for:

- notification appearance
- modal transitions
- hover states
- chart updates
- loading transitions
- panel expansion

---

# 12. Integration With Raymond

Geng Xin works closely with Raymond.

Raymond handles:

- frontend logic
- API integration
- page structure
- data rendering

Geng Xin handles:

- UI components
- design system
- visual consistency
- interaction systems
- UX improvements

---

# 13. Integration With Backend Team

Geng Xin should coordinate with Jay and Kai Zhe to understand:

- API response shapes
- real-time event structures
- risk score formats
- intelligence summary formats
- RAG answer formats

---

# 14. Required UI States

Every component should support:

## Loading State

Examples:

- skeleton cards
- spinner
- loading text

---

## Error State

Examples:

- retry button
- error icon
- error description

---

## Empty State

Examples:

- no threats detected
- no signals found
- no alerts available

---

# 15. Notification System

## Notification Types

```text
critical_alert
warning_alert
opportunity_alert
executive_alert
system_alert
```

## Notification Features

Must support:

- severity levels
- unread count
- dismiss actions
- persistent notifications
- notification center

---

# 16. Styling Guidelines

## Dashboard Style

The dashboard should look:

- enterprise-grade
- AI-native
- intelligence-focused
- security-oriented
- minimal but information-rich

---

## Avoid

Do not use:

- childish UI
- excessive gradients
- neon overload
- over-animated interfaces
- cluttered layouts

---

# 17. MVP Completion Checklist

## Design System

- [ ] Color palette completed
- [ ] Typography system completed
- [ ] Spacing system completed
- [ ] Theme consistency completed

## Components

- [ ] Metric cards completed
- [ ] Risk score cards completed
- [ ] Tables completed
- [ ] Charts completed
- [ ] Modals completed
- [ ] Alert toasts completed
- [ ] Loading components completed

## Real-Time UI

- [ ] Notification system completed
- [ ] Live update animations completed
- [ ] Realtime indicators completed

## Responsiveness

- [ ] Desktop layout completed
- [ ] Tablet layout completed
- [ ] Mobile layout completed

## Accessibility

- [ ] Keyboard navigation completed
- [ ] Focus states completed
- [ ] Color contrast verified

## Documentation

- [ ] Component documentation completed
- [ ] Design system documented
- [ ] Reusable component guidelines completed

---

# 18. Suggested Build Order

## Phase 1 — Design Foundation

- define color palette
- define typography system
- define spacing system
- configure Tailwind theme

## Phase 2 — Core Components

- build buttons
- build cards
- build tables
- build badges
- build modal system

## Phase 3 — Dashboard Components

- build metric cards
- build signal feeds
- build charts
- build alert components

## Phase 4 — Realtime Features

- build notification system
- implement toast animations
- build realtime indicators

## Phase 5 — Responsiveness and UX

- optimize layouts
- optimize spacing
- improve accessibility
- improve mobile support

## Phase 6 — Polish

- refine interactions
- improve visual consistency
- fix responsiveness issues
- optimize component performance

---

# 19. Final Deliverable

Geng Xin’s final deliverable is a complete enterprise-grade frontend design and interaction system that:

1. provides a professional intelligence dashboard UI
2. supports real-time intelligence visualization
3. provides reusable frontend components
4. supports responsive enterprise layouts
5. delivers strong UX and accessibility
6. integrates with Raymond’s frontend logic
7. supports live notifications and updates
8. provides visual consistency across SentinelX
9. supports executive-level usability
10. makes SentinelX feel like a production-grade AI intelligence platform

This is the frontend experience and visual intelligence layer of SentinelX.


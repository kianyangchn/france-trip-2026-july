# Design System Document: The Modern Curator (Tactile Scrapbook)

## 1. Overview & Creative North Star: "The Digital Curator"
This design system moves away from the rigid, sterile grids of typical travel apps and embraces the soul of a **Tactile Scrapbook**. The Creative North Star is **The Digital Curator**: an experience that feels like a curated collection of memories-in-the-making. 

Instead of flat, industrial layouts, we utilize **intentional asymmetry, organic layering, and hyper-rounded forms** (`ROUND_FULL`). We break the "template" look by treating the screen as a physical desk where travel plans are laid out like beautiful paper ephemera. The goal is to make the user feel safe, inspired, and organized through a warm, "hand-assembled" editorial aesthetic.

---

## 2. Colors: Warmth & Soul
The palette is a sun-drenched collection of ochres, sages, and creams. It avoids clinical whites and harsh blacks to maintain a family-friendly, approachable atmosphere.

### The "No-Line" Rule
**Explicit Instruction:** Designers are prohibited from using 1px solid borders for sectioning. Boundaries must be defined solely through background color shifts.
*   **Surface-to-Surface Transitions:** Use `surface_container_low` for the main canvas and `surface_container_highest` for interactive elements.
*   **Tonal Transitions:** Define areas by shifting from `surface` to `surface_variant`.

### Surface Hierarchy & Nesting
Treat the UI as physical layers of fine paper. 
*   **Base:** `background` (#faf9f6)
*   **Sections:** `surface_container_low` (#f4f4f0)
*   **Interactive Cards:** `surface_container_lowest` (#ffffff) to create a subtle "lift."

### Signature Textures & Glass
*   **The Glass Rule:** For floating navigation or date headers, use `surface` at 80% opacity with a `backdrop-blur` of 20px. This allows the warm scrapbook colors to bleed through, softening the interface.
*   **Soulful Gradients:** Main CTAs (e.g., "Add New Trip") should use a subtle linear gradient from `primary` (#914d00) to `primary_container` (#ffaf6d) at a 135-degree angle.

---

## 3. Typography: Editorial Clarity (Chinese-First)
The typography scale is designed for high readability in Chinese (SC) while maintaining a sophisticated, editorial "travel magazine" feel.

*   **Display (plusJakartaSans / Noto Sans SC):** Used for date headers and major city names. Large, bold, and expressive.
*   **Headline (plusJakartaSans / Noto Sans SC):** Used for daily itineraries (e.g., "Day 1: Beijing").
*   **Body (beVietnamPro / Noto Sans SC):** Optimized for legibility in travel descriptions and notes.
*   **Labels:** Small, all-caps (for English accents) or high-contrast weight for Chinese, used for categories like "HOTEL" or "PARKING."

**Identity Note:** We pair the geometric structure of the English fonts with the clean lines of Noto Sans SC to create a "Global Traveler" vibe—organized yet soulful.

---

## 4. Elevation & Depth: Tonal Layering
We eschew traditional shadows in favor of **Tonal Layering**. Depth is a result of color proximity, not artificial lighting.

*   **The Layering Principle:** To make a card pop, place a `surface_container_lowest` element onto a `surface_container` background. The slight shift in "brightness" creates a natural, soft lift.
*   **Ambient Shadows:** If a "floating" action button is required, use an extra-diffused shadow: `offset-y: 8px, blur: 24px, color: rgba(145, 77, 0, 0.08)` (a tinted version of the primary color).
*   **The Ghost Border:** If accessibility requires a container edge, use `outline_variant` at **15% opacity**. Never use 100% opaque lines.

---

## 5. Components: The Scrapbook Elements

### Clickable Cards (Itinerary Items)
*   **Style:** No borders. `ROUND_FULL` (or `xl: 3rem`) corners.
*   **Layout:** Asymmetric spacing. The category icon (e.g., Restaurant) should be housed in a `secondary_container` circle.
*   **Interaction:** On tap, the card should scale down slightly (0.98) to mimic the feel of pressing into thick cardstock.

### Date-Focused Header
*   **Style:** Fixed at the top using the **Glassmorphism Rule**. 
*   **Content:** Large `display-sm` date number paired with `label-md` day of the week.
*   **Color:** Use `tertiary_container` (#fdd355) as a highlighter effect behind the active date.

### Category Icons & Chips
*   **Icons:** Use "hand-drawn" style or thick-stroke icons for Hotel, Parking, Attraction, and Restaurant.
*   **Chips:** Use `ROUND_FULL` with `secondary_fixed` (#98fabe) backgrounds for active filters.

### Input Fields
*   **Style:** Forbid the standard "bottom line" or "outlined box." Use a pill-shaped (`ROUND_FULL`) `surface_container_high` background.
*   **Error State:** Use `error_container` for the background fill and `on_error_container` for text.

### Scrapbook "Extras" (Specialty Components)
*   **The Photo Tape:** A component for attaching images to the itinerary that looks like a semi-transparent piece of washi tape (using `primary_fixed` at 30% opacity).
*   **The Daily Progress Path:** Instead of a straight line, use a soft, dotted path using `outline_variant` to connect itinerary items.

---

## 6. Do's and Don'ts

### Do:
*   **Do** use vertical white space (32px+) to separate days instead of divider lines.
*   **Do** lean into the "Warmth" by using `on_surface_variant` (#5d605c) for secondary text rather than pure grey.
*   **Do** use `ROUND_FULL` for all buttons and interactive containers to ensure the "Family-Friendly/Safe" promise.

### Don't:
*   **Don't** use a 1px solid border. Ever.
*   **Don't** use sharp 90-degree corners; it breaks the "Tactile Scrapbook" softness.
*   **Don't** use high-contrast dark shadows. They feel too "tech" and heavy for a family travel app.
*   **Don't** clutter the screen. If it doesn't fit on a "piece of paper," move it to a sub-layer.

---

## 7. Language Support: Chinese (SC)
Ensure all typography maintains a line-height of at least 1.6 for Chinese characters to prevent visual "clumping." Use `title-md` for Chinese sub-headers to ensure the stroke density of the characters remains clear and legible against the warm backgrounds.
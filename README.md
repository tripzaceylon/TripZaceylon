# TripzaCeylon

Front-end for a Sri Lanka travel company. Static HTML — no build step, no dependencies.

**Live site:** https://tripzaceylon.github.io/TripZaceylon/

## Pages

| File | What it is |
|---|---|
| `index.html` | Home page (copy of `tripzaceylon.html`) |
| `tripzaceylon.html` | Same page under its original name |
| `build-your-trip.html` | Route planner — pick pins, get distance, drive time and days |
| `enquire.html` | Enquiry form |

## Running it locally

Open `index.html` in a browser. That's it. For live reload, use the VS Code
**Live Server** extension.

## What's in it

- Interactive Sri Lanka map built from Natural Earth district geometry, with
  place, hotel and adventure pins that zoom on hover
- Drag-to-browse carousels for offers, packages, stories and destinations
- Swipeable card deck for the food section on mobile
- Site search (`/` or `Cmd/Ctrl+K`)
- Route planner with distance and driving-time estimates

## Credits

Photography from [Unsplash](https://unsplash.com). Typefaces from Google Fonts
(Poppins, Fraunces, Caveat, Pacifico, Cormorant Garamond, Jost, Inter).
Map geometry derived from [Natural Earth](https://www.naturalearthdata.com/)
via the Highcharts map collection. Adventure illustrations are original SVG.

## Not real yet

Prices, hotel names, partner counts, reviews and the hotline number are
placeholders. Forms show a confirmation but do not submit anywhere.

---
name: Institutional Terminal
colors:
  surface: '#141218'
  surface-dim: '#141218'
  surface-bright: '#3b383e'
  surface-container-lowest: '#0f0d13'
  surface-container-low: '#1d1b20'
  surface-container: '#211f24'
  surface-container-high: '#2b292f'
  surface-container-highest: '#36343a'
  on-surface: '#e6e0e9'
  on-surface-variant: '#cbc4d2'
  inverse-surface: '#e6e0e9'
  inverse-on-surface: '#322f35'
  outline: '#948e9c'
  outline-variant: '#494551'
  surface-tint: '#cfbcff'
  primary: '#cfbcff'
  on-primary: '#381e72'
  primary-container: '#6750a4'
  on-primary-container: '#e0d2ff'
  inverse-primary: '#6750a4'
  secondary: '#cdc0e9'
  on-secondary: '#342b4b'
  secondary-container: '#4d4465'
  on-secondary-container: '#bfb2da'
  tertiary: '#e7c365'
  on-tertiary: '#3e2e00'
  tertiary-container: '#c9a74d'
  on-tertiary-container: '#503d00'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#e9ddff'
  primary-fixed-dim: '#cfbcff'
  on-primary-fixed: '#22005d'
  on-primary-fixed-variant: '#4f378a'
  secondary-fixed: '#e9ddff'
  secondary-fixed-dim: '#cdc0e9'
  on-secondary-fixed: '#1f1635'
  on-secondary-fixed-variant: '#4b4263'
  tertiary-fixed: '#ffdf93'
  tertiary-fixed-dim: '#e7c365'
  on-tertiary-fixed: '#241a00'
  on-tertiary-fixed-variant: '#594400'
  background: '#141218'
  on-background: '#e6e0e9'
  surface-variant: '#36343a'
typography:
  display:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: -0.01em
  ui-medium:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 16px
  ui-small:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '400'
    lineHeight: 14px
  data-mono:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: -0.02em
  data-mono-sm:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '400'
    lineHeight: 14px
spacing:
  unit: 4px
  container-padding: 12px
  cell-padding-x: 8px
  cell-padding-y: 4px
  gutter: 1px
---

## Brand & Style

This design system is engineered for the high-velocity environment of professional equity research and real-time trading. It prioritizes information density and ocular efficiency over decorative flair. The aesthetic is rooted in **Modern Minimalism with a Technical edge**, evoking the precision of a Bloomberg Terminal or a high-end IDE. 

The goal is to provide a "glass-pane" experience where the interface disappears, leaving only the data. By removing rounded corners and heavy shadows, the system emphasizes a rigid, grid-based architecture that communicates stability, speed, and institutional-grade reliability.

## Colors

The palette is strictly functional, utilizing the Zinc grayscale to establish a hierarchy of depth without the use of shadows. 

- **Primary Background**: Zinc-950 (`#09090b`) serves as the void, providing maximum contrast for data.
- **Surfaces**: Zinc-900 (`#18181b`) is used for panels, table headers, and modal containers.
- **Borders**: Zinc-800 (`#27272a`) defines the structure. All elements are bounded by 1px solid strokes.
- **Semantic Accents**: Emerald-500 and Rose-500 are reserved exclusively for price action and performance indicators. Blue-500 is used sparingly for active states and selection highlights.

## Typography

This system employs a dual-font strategy to separate interface logic from financial data.

- **Inter**: Used for all UI elements, navigation, labels, and instructional text. It provides a neutral, highly legible canvas for the terminal's architecture.
- **JetBrains Mono**: Used for all numerical data, tickers, and price values. The monospaced nature ensures that columns of numbers align perfectly in tables, allowing for rapid vertical scanning of decimals and percentages.

All typography uses a slightly tightened letter-spacing to maintain the high-density requirement.

## Layout & Spacing

The layout follows a **Fixed-Grid Modular approach**. The screen is divided into functional "tiles" or "panes" separated by 1px Zinc-800 borders, mimicking a multi-monitor trading setup within a single window.

- **Density**: The spacing scale is based on a 4px increment. Padding is kept to the absolute minimum necessary for legibility.
- **Grid**: Use a 12-column grid for internal layout within panes, but prioritize a flexible flex-box approach for toolbars to maximize horizontal space.
- **Alignment**: All data cells must be top-aligned. Numerical data should be right-aligned to the decimal point for tabular comparison.

## Elevation & Depth

Elevation in this design system is achieved through **Tonal Layering and Borders** rather than shadows or blurs.

- **Level 0 (Base)**: Zinc-950 background.
- **Level 1 (Panes)**: Zinc-900 surface with a 1px Zinc-800 border.
- **Level 2 (Popovers/Tooltips)**: Zinc-900 surface with a brighter Zinc-700 border to differentiate from the background panels. 
- **Active State**: Active panes or selected rows are indicated by a 1px Blue-500 left-border or a subtle Zinc-800 background shift. Shadows are prohibited to maintain the flat, technical aesthetic.

## Shapes

The design system utilizes **Sharp (0px) geometry** exclusively. 

Every UI element—including buttons, input fields, dropdowns, and containers—must have square corners. This reinforces the "Institutional Terminal" feel, emphasizing the precision of a technical instrument. The absence of radii allows for more efficient use of pixels in high-density data grids.

## Components

- **Data Tables**: The core component. Features a Zinc-900 header with Inter UI-Small (Bold) text. Rows are Zinc-950 with 1px Zinc-800 bottom borders. On hover, rows shift to Zinc-900.
- **Buttons**: Square edges. Primary buttons use a Blue-500 fill with white text. Ghost buttons use a Zinc-800 border and no fill.
- **Inputs**: Flat Zinc-950 background with a 1px Zinc-800 border. Focus state changes the border to Blue-500. No glow or shadow.
- **Status Pills**: Rectangular tags for "Buy/Sell" or "Long/Short". No rounding. Emerald-500/Rose-500 text on a low-opacity background of the same color.
- **Tickers**: Displayed in JetBrains Mono. Price movements are indicated by color-coded text (Emerald-500 for up, Rose-500 for down) and a small geometric triangle icon (pointing up or down).
- **Scrollbars**: Ultra-thin (4px) Zinc-700 bars with no track background to minimize visual noise.
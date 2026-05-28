/** @type {import('tailwindcss').Config} */
import forms from '@tailwindcss/forms'
import containerQueries from '@tailwindcss/container-queries'

export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      "colors": {
        "surface-dim": "#d8dadc",
        "secondary-fixed-dim": "#c8c6c8",
        "on-secondary-fixed-variant": "#474649",
        "error-container": "#ffdad6",
        "on-primary-container": "#fff2f0",
        "on-background": "#191c1e",
        "tertiary": "#57575a",
        "secondary-fixed": "#e4e2e4",
        "on-secondary": "#ffffff",
        "surface-bright": "#f8f9fb",
        "inverse-on-surface": "#eff1f3",
        "on-tertiary-fixed": "#1b1b1e",
        "surface-container": "#eceef0",
        "surface-container-highest": "#e0e3e5",
        "primary-fixed": "#ffdad6",
        "on-surface": "#191c1e",
        "secondary": "#5f5e60",
        "inverse-surface": "#2d3133",
        "outline-variant": "#e4beba",
        "tertiary-fixed-dim": "#c7c6c9",
        "primary": "#af101a",
        "on-secondary-container": "#636264",
        "background": "#f8f9fb",
        "on-tertiary-fixed-variant": "#464649",
        "on-tertiary": "#ffffff",
        "on-error": "#ffffff",
        "error": "#ba1a1a",
        "on-tertiary-container": "#f5f3f7",
        "on-secondary-fixed": "#1b1b1d",
        "inverse-primary": "#ffb3ac",
        "on-surface-variant": "#5b403d",
        "on-error-container": "#93000a",
        "surface-container-low": "#f2f4f6",
        "surface": "#f8f9fb",
        "tertiary-fixed": "#e3e2e5",
        "surface-container-lowest": "#ffffff",
        "on-primary": "#ffffff",
        "on-primary-fixed": "#410003",
        "on-primary-fixed-variant": "#930010",
        "tertiary-container": "#6f6f72",
        "surface-container-high": "#e6e8ea",
        "primary-container": "#d32f2f",
        "primary-fixed-dim": "#ffb3ac",
        "secondary-container": "#e2dfe1",
        "surface-variant": "#e0e3e5",
        "surface-tint": "#ba1a20",
        "outline": "#8f6f6c"
      },
      "borderRadius": {
        "DEFAULT": "0.25rem",
        "lg": "0.5rem",
        "xl": "0.75rem",
        "full": "9999px"
      },
      "spacing": {
        "container-max": "1440px",
        "stack-md": "16px",
        "stack-sm": "8px",
        "stack-lg": "24px",
        "margin-desktop": "32px",
        "margin-tablet": "24px",
        "gutter": "24px",
        "sidebar-width": "260px",
        "margin-mobile": "16px"
      },
      "fontFamily": {
        "body-md": ["Inter"],
        "headline-lg": ["Inter"],
        "body-lg": ["Inter"],
        "label-sm": ["Inter"],
        "headline-sm": ["Inter"],
        "headline-md": ["Inter"],
        "label-md": ["Inter"],
        "display-lg": ["Inter"],
        "headline-lg-mobile": ["Inter"]
      },
      "fontSize": {
        "body-md": ["14px", {"lineHeight": "20px", "fontWeight": "400"}],
        "headline-lg": ["32px", {"lineHeight": "40px", "letterSpacing": "-0.01em", "fontWeight": "600"}],
        "body-lg": ["16px", {"lineHeight": "24px", "fontWeight": "400"}],
        "label-sm": ["12px", {"lineHeight": "16px", "fontWeight": "500"}],
        "headline-sm": ["20px", {"lineHeight": "28px", "fontWeight": "600"}],
        "headline-md": ["24px", {"lineHeight": "32px", "fontWeight": "600"}],
        "label-md": ["14px", {"lineHeight": "18px", "letterSpacing": "0.01em", "fontWeight": "500"}],
        "display-lg": ["48px", {"lineHeight": "56px", "letterSpacing": "-0.02em", "fontWeight": "700"}],
        "headline-lg-mobile": ["24px", {"lineHeight": "32px", "fontWeight": "600"}]
      }
    },
  },
  plugins: [
    forms,
    containerQueries
  ],
}

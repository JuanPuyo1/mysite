/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./core/templates/**/*.html",
    "./static/js/**/*.js",
  ],
  theme: {
    extend: {
      colors: {
        bg: "#f4f6f5",
        ink: "#141816",
        muted: "#5c6660",
        accent: "#1f6f78",
        "accent-soft": "#d7ebec",
        surface: "#ffffff",
        line: "#dce3df",
      },
      fontFamily: {
        display: ["Space Grotesk", "sans-serif"],
        body: ["IBM Plex Sans", "sans-serif"],
      },
      borderRadius: {
        xl: "12px",
      },
    },
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: [
      {
        esteban: {
          primary: "#1f6f78",
          secondary: "#d7ebec",
          accent: "#4fa88a",
          neutral: "#141816",
          "base-100": "#ffffff",
          "base-200": "#f4f6f5",
          "base-300": "#dce3df",
          "base-content": "#141816",
        },
      },
    ],
  },
};

module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/**/*.js"
  ],
  theme: {
    extend: {
      colors: {
        primary: '#8b5cf6',
        secondary: '#10b981',
        accent: '#f59e0b',
      },
      boxShadow: {
        'card-shadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
      }
    },
  },
  plugins: [],
}

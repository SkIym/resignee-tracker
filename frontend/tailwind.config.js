/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      colors: {
        'custom-light-green': '#CFEED8',
        'custom-dark-green': '#1E9F37',
        'custom-light-red': '#FED9DA',
        'custom-dark-red': '#D7313E',
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}
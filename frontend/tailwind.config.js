/** @type {import('tailwindcss').Config} */
export default {
    darkMode: 'class',
    content: ['./src/**/*.{html,svelte,js,ts}'],
    theme: {
      extend: {
        // 필요 시 커스텀 컬러나 폰트 등 추가
      }
    },
    plugins: [
      require('@tailwindcss/typography')
      // 필요 시 다른 Tailwind 플러그인 추가
    ]
  };
  
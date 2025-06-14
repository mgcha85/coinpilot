<script lang="ts">
    const links = [
      { label: 'Privacy Policy', href: '#' },
      { label: 'Terms of Service', href: '#' },
      { label: 'Contact Us', href: '#' }
    ];
  </script>
  <footer class="mt-16 bg-gradient-to-t from-gray-100 dark:from-gray-900 to-transparent text-gray-700 dark:text-gray-300">
    <div class="max-w-7xl mx-auto px-6 py-12 grid grid-cols-1 md:grid-cols-3 gap-6">
      <div>
        <h4 class="text-lg font-semibold mb-4">CoinPilot</h4>
        <p class="text-sm">당신의 크립토 투자 여정을 지원하는 프로페셔널 트레이딩 파트너</p>
      </div>
      <div>
        <h4 class="text-lg font-semibold mb-4">Quick Links</h4>
        <ul class="space-y-2 text-sm">
          {#each links as { label, href }}
            <li><a href={href} class="hover:text-blue-500 transition">{label}</a></li>
          {/each}
        </ul>
      </div>
      <div>
        <h4 class="text-lg font-semibold mb-4">Contact</h4>
        <p class="text-sm">support@coinpilot.example.com</p>
        <p class="text-sm">+82 2-1234-5678</p>
      </div>
    </div>
    <div class="border-t border-gray-300 dark:border-gray-700 mt-6 pt-4 text-center text-sm">
      © 2025 CoinPilot. All rights reserved.
    </div>
  </footer>
  
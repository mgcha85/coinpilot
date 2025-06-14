<script lang="ts">
  import { goto } from '$app/navigation';
  import { BarChart, DollarSign, Database, ClipboardList, Zap, Settings } from 'lucide-svelte';

  const features = [
    { icon: BarChart, title: '실시간 차트 분석', desc: '다중 TF 기반 이평선·볼륨·패턴 분석', link: '/chart' },
    { icon: DollarSign, title: '수익률 추적', desc: '실현/미실현 PNL 통합 조회·시각화', link: '/pnl' },
    { icon: Database, title: '학습 데이터 생성', desc: '클릭 포인트 자동 수집·DB 저장', link: '/dataset' },
    { icon: ClipboardList, title: '전략 체크포인트', desc: '메모·체결 기록·분할 매매 관리', link: '/portfolio' },
    { icon: Zap, title: '상대강도 분석', desc: '코인 간 상대 강도 랭킹 산출', link: '/relative' },
    { icon: Settings, title: '환경설정', desc: 'API 키·관심종목·DB 연결 관리', link: '/settings' }
  ];

  function navTo(path: string) {
    goto(path);
  }
</script>

<main class="bg-gray-50 dark:bg-gray-900 text-gray-800 dark:text-gray-100 py-16 px-6">
  <div class="max-w-5xl mx-auto text-center mb-12">
    <h1 class="text-5xl font-extrabold mb-4">🚀 CoinPilot</h1>
    <p class="text-lg text-gray-600 dark:text-gray-400">
      차트·수익률·전략·상대강도까지<br />
      한 곳에서 스마트하게 매매하세요.
    </p>
  </div>

  <div class="max-w-6xl mx-auto grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
    {#each features as { icon, title, desc, link }}
      <div
        class="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow hover:shadow-xl transform hover:-translate-y-1 transition cursor-pointer"
        on:click={() => navTo(link)}
      >
        <svelte:component this={icon} class="w-10 h-10 text-blue-500 mb-4" />
        <h2 class="text-xl font-semibold mb-2">{title}</h2>
        <p class="text-sm text-gray-500 dark:text-gray-400">{desc}</p>
      </div>
    {/each}
  </div>

  <div class="max-w-5xl mx-auto text-center mt-16">
    <button
      class="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-8 py-3 rounded-full shadow-lg transition hover:-translate-y-1"
      on:click={() => navTo('/portfolio')}
    >
      지금 시작하기 →
    </button>
  </div>
</main>

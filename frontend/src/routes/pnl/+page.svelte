<script lang="ts">
  import { onMount } from 'svelte';
  let mode: 'unrealized' | 'realized' = 'unrealized';
  let loading = true;
  let data = [];

  function fetchPNL() {
    loading = true;
    // TODO: 백엔드 호출
    setTimeout(() => {
      data = [ { date: '2025-06-01', value: 5 }, { date: '2025-06-02', value: -2 } ];
      loading = false;
    }, 800);
  }

  onMount(fetchPNL);
</script>

<div class="max-w-6xl mx-auto p-6">
  <h2 class="text-2xl font-semibold mb-4">수익률 추적</h2>
  <div class="flex space-x-4 mb-6">
    <button
      class="px-4 py-1 rounded focus:outline-none {mode === 'unrealized' ? 'bg-blue-600 text-white' : 'bg-gray-200 dark:bg-gray-700'}"
      on:click={() => { mode = 'unrealized'; fetchPNL(); }}
    >미실현 PNL</button>
    <button
      class="px-4 py-1 rounded focus:outline-none {mode === 'realized' ? 'bg-blue-600 text-white' : 'bg-gray-200 dark:bg-gray-700'}"
      on:click={() => { mode = 'realized'; fetchPNL(); }}
    >실현 PNL</button>
  </div>

  {#if loading}
    <div class="text-center py-10">로딩 중...</div>
  {:else}
    <!-- 차트 / 테이블 표시 -->
    <div class="h-64 bg-gray-100 dark:bg-gray-800 rounded flex items-center justify-center">
      <span class="text-gray-500">{mode} 차트/테이블</span>
    </div>
  {/if}
</div>
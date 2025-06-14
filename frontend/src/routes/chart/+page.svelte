<script lang="ts">
    import { onMount } from 'svelte';
    let loading = true;
    let error = '';
    let symbol = 'BTCUSDT';
    let timeframe = '5m';
    const timeframes = ['5m', '15m', '1h', '4h', '1d'];
  
    function fetchData() {
      loading = true;
      // TODO: 백엔드 API 호출 로직
      setTimeout(() => {
        loading = false;
      }, 1000);
    }
  
    onMount(fetchData);
  </script>
  
  <div class="max-w-6xl mx-auto p-6">
    <h2 class="text-2xl font-semibold mb-4">실시간 차트 분석</h2>
    <div class="flex items-center space-x-4 mb-6">
      <input type="text" bind:value={symbol} placeholder="Symbol" class="border rounded px-3 py-1" />
      <select bind:value={timeframe} class="border rounded px-3 py-1">
        {#each timeframes as tf}
          <option value={tf}>{tf}</option>
        {/each}
      </select>
      <button class="bg-blue-600 text-white px-4 py-1 rounded" on:click={fetchData}>불러오기</button>
    </div>
  
    {#if loading}
      <div class="text-center py-10">로딩 중...</div>
    {:else}
      <!-- 차트 라이브러리 삽입 위치 -->
      <div class="h-96 bg-gray-100 dark:bg-gray-800 flex items-center justify-center rounded">
        <span class="text-gray-500">차트가 여기에 표시됩니다</span>
      </div>
    {/if}
  </div>
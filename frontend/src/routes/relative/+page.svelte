<script lang="ts">
  import { onMount } from 'svelte';
  
  const tickers = ['BTCUSDT', 'ETHUSDT', 'XRPUSDT', 'ADAUSDT'];
  let selectedTickers: string[] = ['BTCUSDT', 'ETHUSDT'];
  const intervals = ['1m', '5m', '15m', '1h', '4h'];
  let selectedInterval = '5m';
  let limit = 400;

  let loading = false;
  let error = '';
  let results: { symbol: string; strength: number }[] = [];

  const BASE_URL = import.meta.env.VITE_BASE_URL || "";

  async function fetchStrength() {
    loading = true;
    error = '';
    results = [];
    try {
      // 백엔드 호출
      const params = new URLSearchParams({
        tickers: selectedTickers.join(','),
        interval: selectedInterval,
        limit: String(limit)
      });
        const res = await fetch(`${BASE_URL}/v1/relative-strength?${params}`);
      if (!res.ok) throw new Error('Server error');
      results = await res.json();
    } catch (e) {
      console.error(e);
      error = '상대강도 조회 중 오류가 발생했습니다.';
    } finally {
      loading = false;
    }
  }

  onMount(fetchStrength);
</script>

<div class="max-w-4xl mx-auto p-6">
  <h2 class="text-2xl font-semibold mb-4">상대강도 분석</h2>

  {#if error}
    <p class="text-red-500 mb-4">{error}</p>
  {/if}

  <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
    <div>
      <label class="block mb-1 font-medium">Tickers</label>
      <select bind:value={selectedTickers} multiple class="border rounded p-2 w-full h-24">
        {#each tickers as t}
          <option value={t}>{t}</option>
        {/each}
      </select>
    </div>
    <div>
      <label class="block mb-1 font-medium">Interval</label>
      <select bind:value={selectedInterval} class="border rounded p-2 w-full">
        {#each intervals as iv}
          <option value={iv}>{iv}</option>
        {/each}
      </select>
    </div>
    <div>
      <label class="block mb-1 font-medium">Limit</label>
      <input
        type="number"
        bind:value={limit}
        min="1"
        class="border rounded p-2 w-full"
      />
    </div>
    <div class="flex items-end">
      <button
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition w-full"
        on:click={fetchStrength}
        disabled={loading || selectedTickers.length === 0}
      >
        {#if loading}로딩 중...{:else}조회{/if}
      </button>
    </div>
  </div>

  <table class="w-full table-auto bg-white dark:bg-gray-800 rounded shadow overflow-hidden">
    <thead class="bg-gray-100 dark:bg-gray-700">
      <tr>
        <th class="px-4 py-2">Symbol</th>
        <th class="px-4 py-2">Strength (%)</th>
      </tr>
    </thead>
    <tbody>
      {#each results as r}
        <tr class="border-t border-gray-200 dark:border-gray-700">
          <td class="px-4 py-2">{r.symbol}</td>
          <td class="px-4 py-2">{r.strength.toFixed(2)}</td>
        </tr>
      {/each}
    </tbody>
  </table>
</div>

<style>
/* 필요 시 스타일 추가 */
</style>

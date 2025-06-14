<script lang="ts">
    type Row = { symbol: string; timeframe: string; timestamp: string };
    let rows: Row[] = [];
    let newSymbol = '';
    let newTf = '5m';
    let loading = false;
  
    function addRow() {
      if (!newSymbol) return;
      rows = [{ symbol: newSymbol, timeframe: newTf, timestamp: new Date().toISOString() }, ...rows];
      newSymbol = '';
    }
  
    async function extract() {
      loading = true;
      // TODO: 각 row에 대해 데이터 추출 백엔드 호출
      await new Promise(r => setTimeout(r, 1000));
      loading = false;
    }
  </script>
  
  <div class="max-w-6xl mx-auto p-6">
    <h2 class="text-2xl font-semibold mb-4">학습 데이터 생성</h2>
    <div class="flex space-x-2 mb-4">
      <input type="text" bind:value={newSymbol} placeholder="Symbol" class="border rounded px-3 py-1 flex-1" />
      <select bind:value={newTf} class="border rounded px-3 py-1">
        <option value="5m">5m</option>
        <option value="15m">15m</option>
        <option value="1h">1h</option>
        <option value="4h">4h</option>
        <option value="1d">1d</option>
      </select>
      <button class="bg-green-600 text-white px-4 py-1 rounded" on:click={addRow}>추가</button>
    </div>
  
    {#if rows.length === 0}
      <p class="text-gray-500">추가된 학습 포인트가 없습니다.</p>
    {:else}
      <table class="w-full table-auto mb-4">
        <thead><tr class="bg-gray-200 dark:bg-gray-700"><th>Symbol</th><th>TF</th><th>Time</th><th></th></tr></thead>
        <tbody>
          {#each rows as row, i}
          <tr>
            <td>{row.symbol}</td><td>{row.timeframe}</td><td>{row.timestamp}</td>
            <td><button class="text-red-500" on:click={() => rows = rows.filter((_, idx) => idx !== i)}>삭제</button></td>
          </tr>
          {/each}
        </tbody>
      </table>
      <button class="bg-blue-600 text-white px-4 py-1 rounded" on:click={extract} disabled={loading}>
        {#if loading}추출 중...{:else}데이터 추출{/if}
      </button>
    {/if}
  </div>
  
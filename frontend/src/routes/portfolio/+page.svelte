<script lang="ts">
    type Trade = { step: number; type: 'swing' | 'scalp'; price: number; size: number };
    let trades: Trade[] = [];
    let step = 1;
    let type: Trade['type'] = 'swing';
    let price = 0;
    let size = 0;
  
    function placeOrder() {
      trades = [...trades, { step, type, price, size }];
      step += 1;
    }
  </script>
  
  <div class="max-w-6xl mx-auto p-6">
    <h2 class="text-2xl font-semibold mb-4">전략 체크포인트</h2>
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
      <input type="number" bind:value={step} class="border rounded px-3 py-1" readonly placeholder="Step" />
      <select bind:value={type} class="border rounded px-3 py-1">
        <option value="swing">Swing</option>
        <option value="scalp">Scalp</option>
      </select>
      <input type="number" bind:value={price} placeholder="Price" class="border rounded px-3 py-1" />
      <input type="number" bind:value={size} placeholder="Size" class="border rounded px-3 py-1" />
    </div>
    <button class="bg-blue-600 text-white px-4 py-1 rounded mb-6" on:click={placeOrder}>주문 실행</button>
  
    {#if trades.length === 0}
      <p class="text-gray-500">실행된 주문이 없습니다.</p>
    {:else}
      <table class="w-full table-auto">
        <thead><tr class="bg-gray-200 dark:bg-gray-700"><th>Step</th><th>Type</th><th>Price</th><th>Size</th></tr></thead>
        <tbody>
          {#each trades as t}
          <tr><td>{t.step}</td><td>{t.type}</td><td>{t.price}</td><td>{t.size}</td></tr>
          {/each}
        </tbody>
      </table>
    {/if}
  </div>
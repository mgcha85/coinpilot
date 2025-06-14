<script lang="ts">
  import { onMount } from 'svelte';
  import { writable, derived } from 'svelte/store';

  // 환경 변수
  const BASE_URL = import.meta.env.VITE_BASE_URL || 'http://localhost:8000';
  const JWT = import.meta.env.VITE_JWT_TOKEN || '';
  
  // 미리 지원할 거래소 리스트 (추후 API로 변경 가능)
  const supportedServices = ['binance', 'okx'];

  // --- Types ---
  type Exchange = {
    id: number;
    service: string;
    api_key: string;
    secret_key: string;
    market_type: 'spot' | 'future' | 'both';
    is_main: boolean;
    created_at: string;
  };

  // --- Stores ---
  const exchanges = writable<Exchange[]>([]);
  const loadingExchanges = writable(false);
  const errorExchanges = writable('');

  const mainExchange = derived(exchanges, $exchanges =>
    $exchanges.find(e => e.is_main)
  );

  const symbols = writable<string[]>([]);
  const loadingSymbols = writable(false);
  const errorSymbols = writable('');

  const selectedSymbols = writable<Set<string>>(new Set());

  // --- Helpers ---
  function createEmptyExchange(): Exchange {
    return {
      id: 0,
      service: supportedServices[0],
      api_key: '',
      secret_key: '',
      market_type: 'spot',
      is_main: false,
      created_at: ''
    };
  }

  async function loadExchanges() {
    loadingExchanges.set(true);
    errorExchanges.set('');
    try {
      const res = await fetch(`${BASE_URL}/v1/settings/exchanges/`, {
        headers: { 
          'Authorization': `Bearer ${JWT}`,
          'Content-Type': 'application/json'
        }
      });
      if (!res.ok) throw new Error();
      exchanges.set(await res.json());
    } catch {
      errorExchanges.set('거래소 설정을 불러오는데 실패했습니다.');
    } finally {
      loadingExchanges.set(false);
    }
  }

  function addExchangeRow() {
    exchanges.update(list => [...list, createEmptyExchange()]);
  }

  async function saveExchange(ex: Exchange) {
    try {
      const res = await fetch(`${BASE_URL}/v1/settings/exchanges/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${JWT}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          service: ex.service,
          api_key: ex.api_key,
          secret_key: ex.secret_key,
          market_type: ex.market_type,
          is_main: ex.is_main
        })
      });
      if (!res.ok) throw new Error();
      await loadExchanges();
    } catch {
      alert('거래소 설정 저장에 실패했습니다.');
    }
  }

  async function loadSymbols() {
    loadingSymbols.set(true);
    errorSymbols.set('');
    symbols.set([]);
    selectedSymbols.set(new Set());
    try {
      const res = await fetch(`${BASE_URL}/v1/settings/exchanges/symbols/`, {
        headers: { 
          'Authorization': `Bearer ${JWT}`,
          'Content-Type': 'application/json'
        }
      });
      if (!res.ok) throw new Error();
      symbols.set(await res.json());
    } catch {
      errorSymbols.set('심볼 목록을 불러오는데 실패했습니다.');
    } finally {
      loadingSymbols.set(false);
    }
  }

  async function saveSelectedSymbols() {
    const syms = Array.from($selectedSymbols);
    for (const sym of syms) {
      await fetch(`${BASE_URL}/v1/settings/exchanges/symbols/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${JWT}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          exchange_id: $mainExchange!.id,
          symbol: sym
        })
      });
    }
    alert('모니터링 심볼이 저장되었습니다.');
  }

  function toggleSymbol(sym: string) {
    const set = new Set($selectedSymbols);
    set.has(sym) ? set.delete(sym) : set.add(sym);
    selectedSymbols.set(set);
  }

  // 초기 로드
  onMount(loadExchanges);

  // 주 거래소 변경 시 심볼 자동 로드
  $: if ($mainExchange) loadSymbols();
</script>

<style>
  .btn {
    @apply bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700;
  }
  .input {
    @apply border rounded px-2 py-1 w-full;
  }
</style>

<div class="p-6 space-y-8">
  <!-- 거래소 설정 -->
  <section>
    <h2 class="text-2xl font-semibold mb-4">거래소 설정</h2>

    <button class="btn mb-4" on:click={addExchangeRow}>
      + 새 거래소 추가
    </button>

    {#if $loadingExchanges}
      <p>로딩 중…</p>
    {:else if $errorExchanges}
      <p class="text-red-500">{$errorExchanges}</p>
    {:else}
      <table class="w-full table-auto border-collapse">
        <thead>
          <tr class="bg-gray-100">
            <th class="p-2">거래소</th>
            <th class="p-2">API Key</th>
            <th class="p-2">Secret Key</th>
            <th class="p-2">Market Type</th>
            <th class="p-2">주거래소</th>
            <th class="p-2">등록/저장</th>
          </tr>
        </thead>
        <tbody>
          {#each $exchanges as ex, idx (ex.id || idx)}
            <tr class="border-t">
              <td class="p-1">
                <select bind:value={ex.service} class="input">
                  {#each supportedServices as svc}
                    <option value={svc}>{svc}</option>
                  {/each}
                </select>
              </td>
              <td class="p-1"><input class="input" type="text" bind:value={ex.api_key} /></td>
              <td class="p-1"><input class="input" type="password" bind:value={ex.secret_key} /></td>
              <td class="p-1">
                <select bind:value={ex.market_type} class="input">
                  <option value="spot">Spot</option>
                  <option value="future">Future</option>
                  <option value="both">Both</option>
                </select>
              </td>
              <td class="p-1 text-center">
                <input type="checkbox" bind:checked={ex.is_main} />
              </td>
              <td class="p-1 text-center">
                <button class="btn" on:click={() => saveExchange(ex)}>
                  {ex.id === 0 ? '등록' : '저장'}
                </button>
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    {/if}
  </section>

  <!-- 심볼 선택 & 저장 -->
  {#if $mainExchange}
    <section>
      <h2 class="text-2xl font-semibold mb-4">
        심볼 선택 (Main: {$mainExchange.service} / {$mainExchange.market_type})
      </h2>

      {#if $loadingSymbols}
        <p>심볼 로딩 중…</p>
      {:else if $errorSymbols}
        <p class="text-red-500">{$errorSymbols}</p>
      {:else}
        <div class="grid grid-cols-3 gap-3 max-h-64 overflow-auto mb-4">
          {#each $symbols as sym}
            <label class="flex items-center space-x-2">
              <input
                type="checkbox"
                checked={$selectedSymbols.has(sym)}
                on:change={() => toggleSymbol(sym)}
              />
              <span>{sym}</span>
            </label>
          {/each}
        </div>
        <button class="btn" on:click={saveSelectedSymbols}>
          모니터링 심볼 저장
        </button>
      {/if}
    </section>
  {/if}
</div>

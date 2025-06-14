<script lang="ts">
    import { onMount } from 'svelte';
    import { writable } from 'svelte/store';
  
    // 상태 저장용 Store
    const formData = writable({
      binanceApiKey: '',
      binanceSecret: '',
      okxApiKey: '',
      okxSecret: '',
      dbUrl: '',
      symbols: '' // 쉼표 구분 입력
    });
  
    let saved = false;
  
    // 저장 버튼 클릭 시
    async function saveSettings() {
      const res = await fetch('/api/settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify($formData)
      });
  
      saved = res.ok;
    }
  
    // 페이지 진입 시 초기 데이터 로드
    onMount(async () => {
      const res = await fetch('/api/settings');
      if (res.ok) {
        const data = await res.json();
        formData.set(data);
      }
    });
  </script>
  
  <main class="p-6 max-w-xl mx-auto">
    <h1 class="text-2xl font-bold mb-4">⚙️ 환경 설정</h1>
  
    <form class="space-y-4" on:submit|preventDefault={saveSettings}>
      <div>
        <label>Binance API Key</label>
        <input type="text" bind:value={$formData.binanceApiKey} class="input" />
      </div>
  
      <div>
        <label>Binance Secret</label>
        <input type="password" bind:value={$formData.binanceSecret} class="input" />
      </div>
  
      <div>
        <label>OKX API Key</label>
        <input type="text" bind:value={$formData.okxApiKey} class="input" />
      </div>
  
      <div>
        <label>OKX Secret</label>
        <input type="password" bind:value={$formData.okxSecret} class="input" />
      </div>
  
      <div>
        <label>DB Endpoint (PostgreSQL)</label>
        <input type="text" bind:value={$formData.dbUrl} class="input" />
      </div>
  
      <div>
        <label>관심 종목 (쉼표로 구분)</label>
        <input type="text" bind:value={$formData.symbols} class="input" />
      </div>
  
      <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded">저장</button>
      {#if saved}<p class="text-green-600">✅ 설정이 저장되었습니다!</p>{/if}
    </form>
  </main>
  
  <style>
    label {
      display: block;
      font-weight: bold;
    }
    .input {
      width: 100%;
      padding: 0.5rem;
      margin-top: 0.25rem;
      border: 1px solid #ccc;
      border-radius: 0.375rem;
    }
  </style>
  
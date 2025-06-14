<script lang="ts">
    import { goto } from '$app/navigation';
    let username = '';
    let email = '';
    let password = '';
    let confirmPassword = '';
    let message = '';
    let errors: string[] = [];
  
    const BASE_URL = import.meta.env.VITE_BASE_URL || "";

    async function register() {
      message = '';
      errors = [];
  
      if (password !== confirmPassword) {
        errors.push('비밀번호와 비밀번호 확인이 일치하지 않습니다.');
        return;
      }
  
      try {
        const res = await fetch(`${BASE_URL}/v1/auth/register`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username, email, password })
        });
        const data = await res.json();
        if (res.ok) {
          message = '회원가입이 완료되었습니다!';
          setTimeout(() => goto('/login'), 1500);
        } else if (data.detail) {
          errors = data.detail.map((d: any) => `${d.loc.join(' > ')}: ${d.msg}`);
        } else {
          errors = ['알 수 없는 오류가 발생했습니다.'];
        }
      } catch (e) {
        console.error(e);
        errors = ['서버와 통신 중 오류가 발생했습니다.'];
      }
    }
  </script>
  
  <div class="max-w-md mx-auto p-6">
    <h2 class="text-2xl font-semibold mb-4">회원가입</h2>
  
    {#if message}
      <p class="mb-4 text-green-600">{message}</p>
    {/if}
    {#if errors.length}
      <ul class="mb-4 text-red-500 list-disc list-inside">
        {#each errors as err}
          <li>{err}</li>
        {/each}
      </ul>
    {/if}
  
    <div class="space-y-4">
      <div>
        <label class="block mb-1">사용자 이름</label>
        <input bind:value={username} type="text" class="w-full border rounded px-3 py-2" />
      </div>
      <div>
        <label class="block mb-1">이메일</label>
        <input bind:value={email} type="email" class="w-full border rounded px-3 py-2" />
      </div>
      <div>
        <label class="block mb-1">비밀번호</label>
        <input bind:value={password} type="password" class="w-full border rounded px-3 py-2" />
      </div>
      <div>
        <label class="block mb-1">비밀번호 확인</label>
        <input bind:value={confirmPassword} type="password" class="w-full border rounded px-3 py-2" />
      </div>
      <button on:click={register} class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition">
        가입하기
      </button>
    </div>
  </div>
  
  <style>
  /* Register page styles */
  </style>
<script lang="ts">
  import { goto } from '$app/navigation';
  let email = '';
  let password = '';
  let message = '';
  let errors: string[] = [];

  const BASE_URL = import.meta.env.VITE_BASE_URL || "";

  async function login() {
    message = '';
    errors = [];
    try {
      const res = await fetch(`${BASE_URL}/v1/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      const data = await res.json();
      if (res.ok) {
        // 토큰 저장
        localStorage.setItem('token', data.access_token);
        message = '로그인 성공!';
        setTimeout(() => goto('/'), 1000);
      } else if (data.detail) {
        // validation errors
        if (Array.isArray(data.detail)) {
          errors = data.detail.map((d: any) => `${d.loc.join(' > ')}: ${d.msg}`);
        } else {
          errors = [data.detail];
        }
      } else {
        errors = ['로그인 중 오류가 발생했습니다.'];
      }
    } catch (e) {
      console.error(e);
      errors = ['서버와 통신 중 오류가 발생했습니다.'];
    }
  }
</script>

<div class="max-w-md mx-auto p-6">
  <h2 class="text-2xl font-semibold mb-4">로그인</h2>

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
      <label class="block mb-1">이메일</label>
      <input bind:value={email} type="email" class="w-full border rounded px-3 py-2" />
    </div>
    <div>
      <label class="block mb-1">비밀번호</label>
      <input bind:value={password} type="password" class="w-full border rounded px-3 py-2" />
    </div>
    <button on:click={login} class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition">
      로그인
    </button>
    <p class="mt-4 text-center text-sm">
      회원이 아니신가요? <a href="/register" class="text-blue-600 hover:underline">회원가입</a>
    </p>
  </div>
</div>

<style>
/* Login page styles */
</style>

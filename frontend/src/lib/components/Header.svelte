<script lang="ts">
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import { Menu, X, Sun, Moon } from 'lucide-svelte';
  
    let menuOpen = false;
    let dark = false;
  
    function navTo(href: string) {
      goto(href);
      menuOpen = false;
    }
  
    onMount(() => {
      dark = document.documentElement.classList.contains('dark');
    });
  
    function toggleDark() {
      dark = !dark;
      document.documentElement.classList.toggle('dark', dark);
    }
  </script>
  
  <nav class="fixed top-0 w-full bg-white/90 dark:bg-gray-900/90 backdrop-blur z-40 shadow">
    <div class="max-w-7xl mx-auto flex items-center justify-between px-6 py-4">
      <h1 class="text-2xl font-bold text-blue-600 cursor-pointer" on:click={() => navTo('/')}>CoinPilot</h1>
      <div class="hidden md:flex items-center space-x-8">
        <a class="text-gray-700 dark:text-gray-200 hover:text-blue-600 transition" on:click={() => navTo('/chart')}>Chart</a>
        <a class="text-gray-700 dark:text-gray-200 hover:text-blue-600 transition" on:click={() => navTo('/pnl')}>PNL</a>
        <a class="text-gray-700 dark:text-gray-200 hover:text-blue-600 transition" on:click={() => navTo('/portfolio')}>Portfolio</a>
        <a class="text-gray-700 dark:text-gray-200 hover:text-blue-600 transition" on:click={() => navTo('/settings')}>Settings</a>
        <button class="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 transition" on:click={toggleDark} aria-label="Toggle theme">
          {#if dark}
            <Sun class="w-5 h-5 text-yellow-400" />
          {:else}
            <Moon class="w-5 h-5 text-gray-800" />
          {/if}
        </button>
      </div>
      <button class="md:hidden p-2 rounded-md hover:bg-gray-200 dark:hover:bg-gray-700 transition" on:click={() => (menuOpen = !menuOpen)} aria-label="Toggle menu">
        {#if menuOpen}
          <X class="w-6 h-6" />
        {:else}
          <Menu class="w-6 h-6" />
        {/if}
      </button>
    </div>
  
    {#if menuOpen}
      <div class="md:hidden bg-white dark:bg-gray-900 shadow-inner">
        <a class="block px-6 py-3 text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800 transition" on:click={() => navTo('/chart')}>Chart</a>
        <a class="block px-6 py-3 text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800 transition" on:click={() => navTo('/pnl')}>PNL</a>
        <a class="block px-6 py-3 text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800 transition" on:click={() => navTo('/portfolio')}>Portfolio</a>
        <a class="block px-6 py-3 text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800 transition" on:click={() => navTo('/settings')}>Settings</a>
        <button class="w-full text-left px-6 py-3 text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800 transition" on:click={toggleDark}>
          {#if dark}Light Mode{:else}Dark Mode{/if}
        </button>
      </div>
    {/if}
  </nav>
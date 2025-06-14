<script>
  import Sidebar from '$lib/Layout/Sidebar.svelte';
  import Topbar from '$lib/Layout/Topbar.svelte';
</script>

<div class="flex h-screen">
  <Sidebar />
  <div class="flex flex-col flex-1">
    <Topbar />
    <main class="p-4 overflow-auto">
      <slot />
    </main>
  </div>
</div>
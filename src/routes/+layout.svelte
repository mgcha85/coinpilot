
<script>
  import Sidebar from '$lib/components/Sidebar.svelte';
</script>

<div class="flex h-screen">
  <Sidebar />
  <div class="flex-1 overflow-auto p-4">
    <slot />
  </div>
</div>

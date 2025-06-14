<script lang="ts">
  import '$lib/app.css';
  import Header from '$lib/components/Header.svelte';
  import Footer from '$lib/components/Footer.svelte';
</script>

<div class="flex flex-col min-h-screen">
	<Header />
	<main class="flex-1 pt-20 mb-16">
		<slot />
	</main>
	<Footer />
</div>

<script>
    let { onsearch } = $props();

    let searchTerm = $state('');
    let searchInput = $state();

    function handleInput() {
        onsearch?.({ searchTerm });
    }

    function clearSearch() {
        searchTerm = '';
        handleInput();
        searchInput?.focus();
    }

    $effect(() => {
        handleInput();
    });
</script>

<div class="relative flex-1 min-w-[200px] max-w-md">
    <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
        <svg class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M21 21l-4.35-4.35M17 10a7 7 0 11-14 0 7 7 0 0114 0z"
            />
        </svg>
    </div>

    <input
        bind:this={searchInput}
        bind:value={searchTerm}
        oninput={handleInput}
        type="text"
        placeholder="Search"
        class="block w-full pl-10 pr-10 py-2.5 border border-gray-300 rounded-3xl"
    />

    {#if searchTerm}
        <div class="absolute inset-y-0 right-0 pr-3 flex items-center">
            <button
                onclick={clearSearch}
                class="text-gray-400 hover:text-gray-600 focus:outline-none transition-colors"
                aria-label="Clear search"
            >
                <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
            </button>
        </div>
    {/if}

</div>

<style>

</style>
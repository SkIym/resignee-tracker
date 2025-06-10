<script>
  import Table from './lib/Table.svelte'
  import { onMount } from 'svelte';

  import SortAndFilterDropdownButton from './lib/SortAndFilterDropdownButton.svelte';

  let employees = [];
  let error = '';

  onMount(async () => {
    try {
      const res = await fetch('http://localhost:8000/ResignedEmployees');
      if (!res.ok) throw new Error(await res.text());
      employees = await res.json();
    } catch (e) {
      error = e.message;
    }
  });
</script>

<main>

  <!-- Search and Controls -->
  <div class="flex flex-wrap gap-3 mb-4">
    <div class="flex-1 min-w-[200px] relative">
      <input 
        type="text" 
        placeholder="Search" 
        class="w-full px-4 py-2 border border-gray-300 rounded-lg pl-10"
      >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400 absolute left-3 top-2.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
      </svg>
    </div>
  </div>

  <SortAndFilterDropdownButton/>

  <!-- Table -->
  <div class="card">
    <Table />
  </div>

  <h1>Resigned Employees</h1>
  {#if error}
    <p style="color: red">{error}</p>
  {:else if employees.length === 0}
    <p>No data found.</p>
  {:else}
    <ul>
      {#each employees as emp}
        <li>{emp.employee_num} ({emp.lastname})</li>
      {/each}
    </ul>
  {/if}
</main>

<style>
  .logo {
    height: 6em;
    padding: 1.5em;
    will-change: filter;
    transition: filter 300ms;
  }
  .logo:hover {
    filter: drop-shadow(0 0 2em #646cffaa);
  }
  .logo.svelte:hover {
    filter: drop-shadow(0 0 2em #ff3e00aa);
  }
  .read-the-docs {
    color: #888;
  }
</style>
<script>
  import Table from './lib/Table.svelte'
  import { onMount } from 'svelte';

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
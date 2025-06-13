<script>
  import { onMount } from 'svelte';

  import EmployeeTable from '../lib/EmployeeTable.svelte';
  import SearchBar from '../lib/SearchBar.svelte'
  import FilterButton from '../lib/FilterButton.svelte';
  import ExportCalendarButton from '../lib/ExportCalendarButton.svelte';

  let employees = [];
  let filteredEmployees = [];
  let error = '';
  let searchTerm = '';
  let statusFilter = 'all';
  let loading = true;

  let message = '';
  let response = '';

  const BASE_URL = 'http://localhost:8000';

  onMount(async () => {
    await loadEmployees();
  });

  async function loadEmployees() {
    try {
      loading = true;
      error = '';
      
      const res = await fetch(`${BASE_URL}/resignees`);
      if (!res.ok) throw new Error(await res.text());
      employees = await res.json();
      
      loading = false;
    } catch (e) {
      error = e.message;
      loading = false;
    }
  }

  // filtering
  $: {
    filteredEmployees = employees.filter(emp => {
      const matchesSearch = searchTerm === '' || 
        emp.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        emp.employee_no.toLowerCase().includes(searchTerm.toLowerCase()) ||
        emp.department.toLowerCase().includes(searchTerm.toLowerCase()) ||
        emp.position_title.toLowerCase().includes(searchTerm.toLowerCase());
      
      // Convert processed_date_time to status for filtering
      const empStatus = emp.processed_date_time ? 'processed' : 'unprocessed';
      const matchesStatus = statusFilter === 'all' || empStatus === statusFilter;
      
      return matchesSearch && matchesStatus;
    });
  }

  function handleSearch(event) {
    searchTerm = event.searchTerm;
  }

  function handleFilter(event) {
    filteredEmployees = event.detail.filtered;
  }

  async function submitMessage() {
    if (!message.trim()) {
      response = 'Please enter resignee details';
      return;
    }

    try {
      response = 'Submitting...';
      
      const res = await fetch(`${BASE_URL}/resignees`, {
        method: 'POST',
        headers: {
          'Content-Type': 'text/plain'
        },
        body: message
      });

      if (!res.ok) {
        const errorText = await res.text();
        throw new Error(`HTTP error! status: ${res.status} - ${errorText}`);
      }

      const data = await res.json();
      
      // Update the employees array with the response data
      employees = data;
      
      response = `Successfully added ${data.length} resignee(s)`;
      message = ''; // Clear the input field
      
    } catch (error) {
      response = `Error: ${error.message}`;
    }
  }

  // Function to handle status toggle from EmployeeTable
  async function handleStatusToggle(event) {
    const { employee } = event.detail;
    
    try {
      const res = await fetch(`${BASE_URL}/resignees/${employee.employee_no}/process`, {
        method: 'PUT'
      });

      if (!res.ok) {
        const errorText = await res.text();
        throw new Error(`Failed to update status: ${res.status} - ${errorText}`);
      }

      // Reload employees to get updated data
      await loadEmployees();
      
    } catch (error) {
      response = `Error updating status: ${error.message}`;
    }
  }
</script>

<svelte:head>
  <title>AUB Resignee Tracker</title>
</svelte:head>

<main class="min-h-screen bg-gray-50 p-6">
  <div class="max-w-7xl mx-auto">
    <!-- Header Controls -->
    <div class="flex flex-wrap items-center justify-between gap-4 mb-6">
      <div class="flex items-center gap-4 flex-1">
        <SearchBar onsearch={handleSearch} />
      </div>
      <div class="flex gap-2">
        <FilterButton on:filter={handleFilter} employees={employees} />
        <ExportCalendarButton data={employees} />
        </div>
    </div>

    <!-- Table Container -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      {#if loading}
        <div class="flex items-center justify-center py-12">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span class="ml-3 text-gray-600">Loading employees...</span>
        </div>
      {:else if error}
        <div class="flex items-center justify-center py-12">
          <div class="text-red-600 bg-red-50 px-4 py-2 rounded-lg">
            Error: {error}
          </div>
        </div>
      {:else}
        <EmployeeTable employees={filteredEmployees} onstatustoggle={handleStatusToggle} />
      {/if}
    </div>

    <!-- Results Info -->
    {#if !loading && !error}
      <div class="mt-4 text-sm text-gray-600">
        Showing {filteredEmployees.length} of {employees.length} employees
      </div>
    {/if}
  </div>

  <!-- Input field -->
<form on:submit|preventDefault={submitMessage}>
  <div class="mt-4 max-w-7xl mx-auto mb-6">
    <textarea
      bind:value={message}
      rows="5"
      class="block w-full p-4 text-gray-900 border border-gray-300 rounded-lg bg-white text-base resize-y"
      placeholder="Paste resignee details here..."
    ></textarea>
    <button
      type="submit"
      class="mt-4 px-4.25 py-1.5 bg-blue-500 text-white rounded-md"
    >
      Submit
    </button>
    {#if response}
      <p class="mt-2 text-sm text-gray-700">{response}</p>
    {/if}
  </div>
</form>


  <h1>Resigned Employees</h1>
  {#if error}
    <p style="color: red">{error}</p>
  {:else if employees.length === 0}
    <p>No data found.</p>
  {:else}
    <ul>
      {#each employees as emp}
        <li>{emp.employee_no} ({emp.last_name})</li>
      {/each}
    </ul>
  {/if}
</main>

<style>
  :global(body) {
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  }
</style>
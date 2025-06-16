<script>
  import { onMount } from 'svelte';

  import EmployeeTable from '$lib/EmployeeTable.svelte';
  import SearchBar from '$lib/SearchBar.svelte';
  import FilterButton from '$lib/FilterButton.svelte';
  import ExportCalendarButton from '$lib/ExportCalendarButton.svelte';
  import LogoutButton from '$lib/LogoutButton.svelte';

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
      
      console.log('Attempting to fetch from:', `${BASE_URL}/resignees`);
      
      // Add timeout
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 second timeout
      
      const res = await fetch(`${BASE_URL}/resignees`, {
        signal: controller.signal,
        credentials: "include"
      });

      
      clearTimeout(timeoutId);
      
      console.log('Response status:', res.status);
      console.log('Response ok:', res.ok);
      
      if (!res.ok) {
        const errorText = await res.text();
        console.log('Error response:', errorText);
        throw new Error(`HTTP ${res.status}: ${errorText}`);
      }
      
      const data = await res.json();
      console.log('Received data:', data);
      console.log('Data length:', data?.length);
      
      employees = data || [];
      
      loading = false;
    } catch (e) {
      console.error('Load employees error:', e);
      if (e.name === 'AbortError') {
        error = 'Request timed out. Please check if the server is running.';
      } else if (e.message.includes('fetch')) {
        error = 'Cannot connect to server. Please check if the server is running on http://localhost:8000';
      } else {
        error = e.message;
      }
      loading = false;
    }
  }

  // filtering
  $: {
    filteredEmployees = employees.filter(emp => {
      const matchesSearch = searchTerm === '' || 
        String(emp.name || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
        String(emp.employee_no || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
        String(emp.department || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
        String(emp.position_title || '').toLowerCase().includes(searchTerm.toLowerCase());
      
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
      return;
    }

    try {    
      const res = await fetch(`${BASE_URL}/resignees`, {
        method: 'POST',
        headers: {
          'Content-Type': 'text/plain'
        },
        body: message,

        credentials: 'include'
      });

      if (!res.ok) {
        const errorText = await res.text();
        throw new Error(`HTTP error! status: ${res.status} - ${errorText}`);
      }

      await loadEmployees();
      
      message = '';
      
    } catch (error) {
      response = `Error: ${error.message}`;
    }
  }

  // Function to handle status toggle from EmployeeTable
  async function handleStatusToggle(event) {
    const { employee, action } = event.detail;
    
    try {
      // Determine the endpoint based on the action
      // If no action is provided (old format), determine based on current status
      let endpoint;
      let actionName;
      
      if (action) {
        // New format with explicit action
        endpoint = action;
        actionName = action;
      } else {
        // Old format - determine action based on current status
        if (employee.processed_date_time) {
          endpoint = 'unprocess';
          actionName = 'unprocess';
        } else {
          endpoint = 'process';
          actionName = 'process';
        }
      }
      
      const res = await fetch(`${BASE_URL}/resignees/${employee.employee_no}/${endpoint}`, {
        method: 'PUT',
        credentials: 'include'
      });

      if (!res.ok) {
        const errorText = await res.text();
        throw new Error(`Failed to ${actionName} employee: ${res.status} - ${errorText}`);
      }

      // Reload employees to get updated data
      await loadEmployees();
      
      // Show success message
      const actionPastTense = actionName === 'process' ? 'processed' : 'unprocessed';
      // response = `Successfully marked ${employee.name} as ${actionPastTense}`;
      
    } catch (error) {
      const actionName = action || (employee.processed_date_time ? 'unprocess' : 'process');
      response = `Error ${actionName}ing employee: ${error.message}`;
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
        <div class="overflow-auto max-h-[500px]">
          <EmployeeTable employees={filteredEmployees} onstatustoggle={handleStatusToggle} />
        </div>
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
		<div class="mt-4 flex justify-between items-center">
    <button
      type="submit"
      class="px-4.25 py-1.5 bg-blue-500 text-white rounded-md"
    >
      Submit
    </button>

    <LogoutButton />
  </div>
		{#if response}
		<p class="mt-2 text-sm text-gray-700">{response}</p>
		{/if}
	</div>
	</form>
</main>

<style>
  :global(body) {
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  }
</style>
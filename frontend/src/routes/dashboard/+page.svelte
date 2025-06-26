<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation'; 
  import { BASE_URL } from '../../constants';
  import toast, { Toaster } from 'svelte-5-french-toast';

  import EmployeeTable from '$lib/EmployeeTable.svelte';
  import SearchBar from '$lib/SearchBar.svelte';
  import FilterButton from '$lib/FilterButton.svelte';
  import ExportCalendarButton from '$lib/ExportCalendarButton.svelte';
  import LogoutButton from '$lib/LogoutButton.svelte';

  import type { Employee } from '../../types';

  let employees: Employee[] = [];
  let filteredEmployees: Employee[] = [];
  let error = '';
  let searchTerm = '';
  let statusFilter = 'all';
  let loading = true;

  let message = '';
  let response = '';


  onMount(async () => {
    try {
      const res = await fetch(`${BASE_URL}/check-auth`, {
        method: 'GET',
        credentials: 'include'
      });

      if (!res.ok) {
        console.log("Unauthorized. Redirecting to login.");
        goto('/');
      } else {
        await loadEmployees();
      }
    } catch (err) {
      console.error("Fetch failed (likely CORS or server down). Redirecting to login.");
      goto('/');
    }
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
      
      if (e instanceof Error) {
        if (e.name === 'AbortError') {
          error = 'Request timed out. Please check if the server is running.';
        } else if (e.message.includes('fetch')) {
          error = 'Cannot connect to server. Please check if the server is running on http://localhost:8000';
        } else {
          error = e.message;
        }
      } else {
        error = 'An unexpected error occurred';
      }
      
      loading = false;
    }
  }

  // filtering
  $: {
    const monthAliases = {
      january: 0, jan: 0,
      february: 1, feb: 1,
      march: 2, mar: 2,
      april: 3, apr: 3,
      may: 4,
      june: 5, jun: 5,
      july: 6, jul: 6,
      august: 7, aug: 7,
      september: 8, sep: 8,
      october: 9, oct: 9,
      november: 10, nov: 10,
      december: 11, dec: 11
    };

    const lowerSearch = searchTerm.toLowerCase().trim();
    const monthMatch = monthAliases[lowerSearch as keyof typeof monthAliases];

    filteredEmployees = employees.filter(emp => {
      const empStatus = emp.processed_date_time ? 'processed' : 'unprocessed';
      const matchesStatus = statusFilter === 'all' || empStatus === statusFilter;

      // Check string-based fields
      const matchesField = (field: unknown) =>
        String(field || '').toLowerCase().includes(lowerSearch);

      // Check month match in date fields
      const empDateHired = new Date(emp.date_hired);
      const empLastDay = new Date(emp.last_day);
      const matchesMonth =
        monthMatch !== undefined &&
        (empDateHired.getMonth() === monthMatch || empLastDay.getMonth() === monthMatch);

      return (
        lowerSearch === '' ||
        matchesField(emp.name) ||
        matchesField(emp.employee_no) ||
        matchesField(emp.department) ||
        matchesField(emp.position_title) ||
        matchesMonth
      ) && matchesStatus;
    });
  }

  function handleSearch(event: { searchTerm: string }) {
    searchTerm = event.searchTerm;
  }

  function handleFilter(event: { detail: { filtered: Employee[] } }) {
    filteredEmployees = event.detail.filtered;
  }

  async function submitMessage() {
    const rawLines = message.split('\n'); // Do NOT trim here

    const LINES_PER_EMPLOYEE = 20;

    // Validation: must be a clean multiple of 20
    if (rawLines.length % LINES_PER_EMPLOYEE !== 0) {
      toast.error(`Invalid input: expected 20 lines per employee (10 fields, each followed by a blank line). Got ${rawLines.length} lines.`);
      return;
    }

    const numEmployees = rawLines.length / LINES_PER_EMPLOYEE;

    for (let emp = 0; emp < numEmployees; emp++) {
      for (let i = 0; i < LINES_PER_EMPLOYEE; i++) {
        const index = emp * LINES_PER_EMPLOYEE + i;
        const line = rawLines[index];

        if (i % 2 === 0) {
          // Expecting data
          if (!line || line.trim() === '') {
            toast.error(`Employee ${emp + 1}, line ${i + 1} is empty. Expected a data field.`);
            return;
          }
        } else {
          // Expecting blank
          if (line.trim() !== '') {
            toast.error(`Employee ${emp + 1}, line ${i + 1} must be blank (used for spacing).`);
            return;
          }
        }
      }
    }

    try {
      const res = await fetch(`${BASE_URL}/resignees`, {
        method: 'POST',
        headers: {
          'Content-Type': 'text/plain'
        },
        body: message.trimEnd(), // keep any final newline that the user intended
        credentials: 'include'
      });

      if (!res.ok) {
        const errorText = await res.text();
        throw new Error(`HTTP error! status: ${res.status} - ${errorText}`);
      }

      await loadEmployees();
      message = '';
      let summaryList: string[] = [];

      for (let emp = 0; emp < numEmployees; emp++) {
        const base = emp * LINES_PER_EMPLOYEE;
        const empNo = rawLines[base].trim();
        const lastName = rawLines[base + 6].trim();
        const firstName = rawLines[base + 8].trim();
        const middleName = rawLines[base + 10].trim();

        summaryList.push(`${empNo} – ${firstName} ${middleName} ${lastName}`);
      }

      toast.success(
        `Successfully added ${numEmployees} employee(s)!\n${summaryList.join('\n')}`
      );

    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      toast.error(`Failed to add employee(s): ${errorMsg}`);
    }
  }


  async function handleStatusToggle(event: { detail: { employee: Employee, action?: string } }) {
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
      const errorMessage = error instanceof Error ? error.message : String(error);
      response = `Error ${actionName}ing employee: ${errorMessage}`;
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
      <img src="/assets/aub-logo-2.png" alt="AUB logo" width="45"/>
      <div class="flex items-center gap-4 flex-1">
        <SearchBar onsearch={handleSearch} />
      </div>
      <div class="flex gap-2">
        <FilterButton on:filter={handleFilter} employees={employees} />
        <ExportCalendarButton />
      </div>
    </div>

    <!-- Table Container -->
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
          <EmployeeTable
            employees={filteredEmployees}
            onstatustoggle={handleStatusToggle}
            onEmployeeUpdate={() => {
                // Refetch your employee data here
                loadEmployees();
            }}
          />
      {/if}

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
      class="px-4.25 py-1.5 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition"
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
<script>
  import EmployeeTable from './lib/EmployeeTable.svelte';
  import { onMount } from 'svelte';

  import EmployeeTable from './lib/EmployeeTable.svelte'
  // import ExportButton from './lib/ExportButton.svelte'
  // import FilterButton from './lib/FilterButton.svelte'
  import SearchBar from './lib/SearchBar.svelte'
  // import SortAndFilterDropdownButton from './lib/SortAndFilterDropdownButton.svelte'
  import SortAndFilterDropdownButton from './lib/SortAndFilterDropdownButton.svelte';
  import ExportButton from './lib/ExportButton.svelte';

  let employees = [];
  let filteredEmployees = [];
  let error = '';
  let searchTerm = '';
  let statusFilter = 'all';
  let loading = true;

  // hardcoded data
  const mockEmployees = [
    {
      employee_no: '00001',
      date_hired: '2025-06-11',
      cost_center: 'CC001',
      name: 'Aneko Delfin',
      position_title: 'IT Risk Management Intern',
      rank: 'NA',
      department: 'Operations & IT',
      last_day: '2025-07-04',
      status: 'processed'
    },
    {
      employee_no: '00002',
      date_hired: '2025-06-11',
      cost_center: 'CC001',
      name: 'Tristan Tan',
      position_title: 'IT Risk Management Intern',
      rank: 'NA',
      department: 'Operations & IT',
      last_day: '2025-07-04',
      status: 'processed'
    },
    {
      employee_no: '00003',
      date_hired: '2025-06-11',
      cost_center: 'CC001',
      name: 'Abram Josh Marcelo',
      position_title: 'IT Risk Management Intern',
      rank: 'NA',
      department: 'Operations & IT',
      last_day: '2025-07-04',
      status: 'processed'
    },
    {
      employee_no: '00004',
      date_hired: '2025-06-11',
      cost_center: 'CC001',
      name: 'Nate Feliciano',
      position_title: 'IT Risk Management Intern',
      rank: 'NA',
      department: 'Operations & IT',
      last_day: '2025-07-04',
      status: 'processed'
    },
  ];

  onMount(async () => {
    try {
      // using hardcoded data muna so commented out

      // const res = await fetch('http://localhost:8000/ResignedEmployees');
      // if (!res.ok) throw new Error(await res.text());
      // employees = await res.json();
      
      // simulating API delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      employees = mockEmployees;
      filteredEmployees = employees;
      loading = false;
    } catch (e) {
      error = e.message;
      loading = false;
    }
  });

  // filtering stuff
  $: {
    filteredEmployees = employees.filter(emp => {
      const matchesSearch = searchTerm === '' || 
        emp.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        emp.employee_no.toLowerCase().includes(searchTerm.toLowerCase()) ||
        emp.department.toLowerCase().includes(searchTerm.toLowerCase()) ||
        emp.position_title.toLowerCase().includes(searchTerm.toLowerCase());
      
      const matchesStatus = statusFilter === 'all' || emp.status === statusFilter;
      
      return matchesSearch && matchesStatus;
    });
  }

  function handleSearch(event) {
    searchTerm = event.searchTerm;
  }

  function handleFilter(event) {
    statusFilter = event.filter;
  }

  function handleExport(event) {
    //
  }

</script>

<main class="min-h-screen bg-gray-50 p-6">
  <div class="max-w-7xl mx-auto">
    <!-- Header Controls -->
    <div class="flex flex-wrap items-center justify-between gap-4 mb-6">
      <div class="flex items-center gap-4 flex-1">
        <SearchBar onsearch={handleSearch} />
        <!-- <FilterButton onfilter={handleFilter} /> -->
      </div>
      <!-- <ExportButton onexport={handleExport} /> -->
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
        <EmployeeTable employees={filteredEmployees} />
      {/if}
    </div>

    <!-- Results Info -->
    {#if !loading && !error}
      <div class="mt-4 text-sm text-gray-600">
        Showing {filteredEmployees.length} of {employees.length} employees
      </div>
    {/if}
  </div>
  <!-- <SortAndFilterDropdownButton/> -->

  <!-- Table -->
  <!-- <div class="card">
    <Table />
  </div> -->



  <!-- Export Button -->
  <ExportButton data={employees} />



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
  :global(body) {
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  }
</style>
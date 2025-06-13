<script lang="ts">
  import * as XLSX from 'xlsx';

  export let data: Array<Record<string, any>> = [];

  let startDate = '';
  let endDate = '';
  let exportConfirmed = false;

  function handleExportClick() {
    if (!startDate || !endDate) {
      alert('Please select both a start and end date.');
      return;
    }

    const filtered = data.filter(emp => {
      const d = new Date(emp.last_day);
      return d >= new Date(startDate) && d <= new Date(endDate);
    });

    if (filtered.length === 0) {
      alert('No records found in this date range.');
      return;
    }

    const ws = XLSX.utils.json_to_sheet(filtered);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Sheet1');
    XLSX.writeFile(wb, 'resigned_employees.xlsx');

    exportConfirmed = true;
  }

  function clearDateRange() {
    startDate = '';
    endDate = '';
    exportConfirmed = false;
  }
</script>

<div class="flex items-center gap-2">
  <!-- Always-visible date inputs -->
  <label class="text-sm text-gray-600 font-[Open_Sans]">From:</label>
  <input type="date" bind:value={startDate} class="border px-3 py-1 rounded-full text-sm font-[Open_Sans] uppercase" />

  <label class="text-sm text-gray-600 font-[Open_Sans]">To:</label>
  <input type="date" bind:value={endDate} class="border px-3 py-1 rounded-full text-sm font-[Open_Sans] uppercase" />

  <button
    on:click={handleExportClick}
    class={`flex items-center gap-2 px-4.25 py-1.5 rounded-md text-sm font-medium transition ${
      exportConfirmed ? 'bg-blue-500 text-white' : 'bg-blue-500 text-white'
    }`}
  >
    <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5m-13.5-9L12 3m0 0 4.5 4.5M12 3v13.5" />
    </svg>
    Export
  </button>
</div>
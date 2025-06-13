<script lang="ts">
  export let data: Array<Record<string, any>> = [];

  let startDate = '';
  let endDate = '';
  let exportConfirmed = false;

  async function handleExportClick() {
    if (!startDate || !endDate) {
      alert('Please select both a start and end date.');
      return;
    }

    try {
      const isoStart = new Date(startDate).toISOString();
      const isoEnd = new Date(endDate).toISOString();

      const res = await fetch(`http://localhost:8000/resignees/report?start_date=${isoStart}&end_date=${isoEnd}`);
      if (!res.ok) throw new Error('Failed to fetch report from backend');

      const blob = await res.blob();
      const url = URL.createObjectURL(blob);

      const a = document.createElement('a');
      a.href = url;
      a.download = `resignee_report_${startDate}_to_${endDate}.xlsx`;
      a.click();
      URL.revokeObjectURL(url);

      exportConfirmed = true;
    } catch (err) {
      console.error('Error downloading backend report:', err);
      alert('No process dates were found within the specified date range');
    }
  }

  function clearDateRange() {
    startDate = '';
    endDate = '';
    exportConfirmed = false;
  }


</script>

<div class="flex items-center gap-2">
  <!-- Calendar -->
  <label class="text-sm text-gray-600 font-[Open_Sans]">From:</label>
  <input type="date" bind:value={startDate} class="border px-3 py-1 rounded-full text-sm font-[Open_Sans] uppercase" />
  
  <label class="text-sm text-gray-600 font-[Open_Sans]">To:</label>
  <input type="date" bind:value={endDate} class="border px-3 py-1 rounded-full text-sm font-[Open_Sans] uppercase" />


  <!-- Export Button -->
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
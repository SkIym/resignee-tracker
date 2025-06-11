<script lang="ts">
  import * as XLSX from 'xlsx';
  // Accept data to export (an array of objects)
  export let data: Array<Record<string, any>> = [];

  // Function to convert JSON to CSV and download the file
  function exportToExcel() {
    if (data.length === 0) {
      alert("No data to export!");
      return;
    }

    // Convert data to a worksheet
    const worksheet = XLSX.utils.json_to_sheet(data);
    // Create a workbook and append the worksheet
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, "Sheet1");

    // Export as an Excel file
    XLSX.writeFile(workbook, "resigned_employees.xlsx");
  }
</script>

<style>
  /* Basic styles for the export button */
  button {
    padding: 0.5rem 1.25rem;
    background-color: white;
    color: black;
    border: 1.25px solid #d1d5db;
    border-radius: 0.375rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-family: 'Inter', sans-serif;
    transition: background-color 0.2s, color 0.2s;
  }

  button:hover {
    background-color: #f3f4f6;            /* light gray on hover */
    color: black;
  }
  svg {
    width: 1.5rem;
    height: 1.5rem;
    stroke: black;
    stroke-width: 2;
  }


</style>

<button on:click={exportToExcel}>
  <!-- Download Icon -->
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5m-13.5-9L12 3m0 0 4.5 4.5M12 3v13.5" />
  </svg>
  Export 
</button>

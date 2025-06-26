<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { parseISO, format } from 'date-fns';
  export let employees: Array<Record<string, any>> = [];
  const dispatch = createEventDispatcher();

  let isOpen = false;
  let selectedField = '';
  let inputValue = '';
  let dateStart = '';
  let dateEnd = '';
  let activeFilters: { field: string, value: string }[] = [];

  const fields = [
    "Employee No.",
    "Date Hired",
    "Cost Center",
    "Name",
    "Position",
    "Rank",
    "Department",
    "Last Day",
    "Batch Deactivation",
    "3rd Party Systems",
    "Emails",
    "Windows",
    "HR Email",
    "Status",
    "Remarks"
  ];

  function toggleDropdown() {
    isOpen = !isOpen;
  }

  function selectField(field: string) {
    selectedField = field;
    inputValue = '';
    dateStart = '';
    dateEnd = '';
  }


  function addFilter() {
    if (["Date Hired", "Last Day", "Batch Deactivation", "3rd Party Systems", "Emails", "Windows", "HR Email"].includes(selectedField)) {
      if (dateStart && dateEnd) {
        const formattedStart = new Date(dateStart).toLocaleDateString('en-US', {
        month: '2-digit',
        day: '2-digit',
        year: 'numeric'
      });

        const formattedEnd = new Date(dateEnd).toLocaleDateString('en-US', {
        month: '2-digit',
        day: '2-digit',
        year: 'numeric'
      });
        
        
        const value = `${formattedStart} to ${formattedEnd}`;
        const exists = activeFilters.find(f => f.field === selectedField && f.value === value);
        if (!exists) {
          activeFilters = [...activeFilters, { field: selectedField, value }];
          applyFilters();
        }
        selectedField = '';
        dateStart = '';
        dateEnd = '';
      }
    } else if (selectedField && inputValue) {
      const exists = activeFilters.find(f => f.field === selectedField && f.value === inputValue);
      if (!exists) {
        activeFilters = [...activeFilters, { field: selectedField, value: inputValue }];
        applyFilters();
      }
      selectedField = '';
      inputValue = '';
    }
  }


   function removeFilter(index: number) {
    activeFilters = activeFilters.filter((_, i) => i !== index);
    applyFilters();
  }

  function closeDropdown() {
    isOpen = false;
    selectedField = '';
    inputValue = '';
  }

  function clearAllFilters() {
    activeFilters = [];
    applyFilters();
  }

  function applyFilters() {
    let filtered = employees;
    activeFilters.forEach(filter => {
    const key = mapFieldToKey(filter.field);
    filtered = filtered.filter(emp => {
    const fieldValue = emp[key]?.toString().toLowerCase();
    const filterValue = filter.value.toLowerCase();

      
    if (filter.field === "Employee No." || filter.field === "Cost Center") {
        const normalizedEmp = fieldValue.replace(/^0+/, '');       
        const normalizedInput = filterValue.replace(/^0+/, '');    
        return normalizedEmp === normalizedInput;
    }

    if (["Date Hired", "Last Day", "Batch Deactivation", "3rd Party Systems", "Emails", "Windows", "HR Email"].includes(filter.field)) {
        const [start, end] = filter.value.split(' to ');
        try {
          const date = parseISO(emp[key]);
          return date >= new Date(start) && date <= new Date(end);
        } catch {
          return false;
        }
      }

    if (filter.field === "Status") {
      const normalized = fieldValue ? 'processed' : 'unprocessed';
      return normalized === filterValue.toLowerCase();
    }

    return fieldValue?.toString().toLowerCase().includes(filterValue);
    });
  });

  dispatch('filter', { filtered });
}
function mapFieldToKey(field: string): string {
  const map: Record<string, string> = {
    "Employee No.": "employee_no",
    "Date Hired": "date_hired",
    "Cost Center": "cost_center",
    "Name": "name",
    "Position": "position_title",
    "Rank": "rank",
    "Department": "department",
    "Last Day": "last_day",
    "Batch Deactivation": "um",
    "3rd Party Systems": "third_party",
    "Emails": "email",
    "Windows": "windows",
    "HR Email": "date_hr_emailed",
    "Status": "processed_date_time",
    "Remarks": "remarks"
  };
  return map[field] || field;
}


</script>

<div class="dropdown">
  <button class="filter-button" on:click={toggleDropdown}>
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" d="M12 3c2.755 0 5.455.232 8.083.678.533.09.917.556.917 1.096v1.044a2.25 2.25 0 0 1-.659 1.591l-5.432 5.432a2.25 2.25 0 0 0-.659 1.591v2.927a2.25 2.25 0 0 1-1.244 2.013L9.75 21v-6.568a2.25 2.25 0 0 0-.659-1.591L3.659 7.409A2.25 2.25 0 0 1 3 5.818V4.774c0-.54.384-1.006.917-1.096A48.32 48.32 0 0 1 12 3Z" />
    </svg>
    Filter
  </button>

  {#if isOpen}
    <div class="dropdown-panel">
      <button class="close-button" on:click={closeDropdown}>✕</button>

      <div class="field-grid">
        {#each fields as field}
          <label class="field-option">
            <input type="radio" name="filter" value={field} on:change={() => selectField(field)} checked={selectedField === field} />
            {field}
          </label>
        {/each}
      </div>
      <hr class="divider" />

  {#if ["Date Hired", "Last Day", "Batch Deactivation", "3rd Party Systems", "Emails", "Windows", "HR Email"].includes(selectedField)}
    <div class="date-range">
        <input
          type="date"
          bind:value={dateStart}
          on:change={() => {
            if (dateStart && dateEnd) {
              addFilter();
              isOpen = false;
            }
          }}
        />
        <input
          type="date"
          bind:value={dateEnd}
          on:change={() => {
            if (dateStart && dateEnd) {
              addFilter();
              isOpen = false;
            }
          }}
        />
      </div>


  {:else if selectedField === "Status"} 
    <div class="field-grid mb-2" style="gap: 0.25rem 0.70rem;">
      <label class="field-option">
        <input
          type="radio"
          name="status-filter"
          value="processed"
          on:change={() => {
            inputValue = 'Processed';
            addFilter();
            
          }}
        />
        <span class="inline-block px-5 py-1.5 rounded-full text-sm font-[Open_Sans] font-550 bg-[#CFEED8] text-[#1E9F37]">
          Processed
        </span>
      </label>

      <label class="field-option">
        <input
          type="radio"
          name="status-filter"
          value="unprocessed"
          on:change={() => {
            inputValue = 'Unprocessed';
            addFilter();
            
          }}
        />
        <span class="inline-block px-3 py-1.5 rounded-full text-sm font-[Open_Sans] font-550 bg-[#FED9DA] text-[#D7313E]">
          Unprocessed
        </span>
      </label>
    </div>


    {:else if selectedField}
      <div class="filter-input">
        <input
          type="text"
          bind:value={inputValue}
          placeholder={`Enter ${selectedField}...`}
          class="w-full px-2 py-1 border rounded mb-0.25"
          on:keydown={(e) => {
            if (e.key === 'Enter') {
              addFilter();
              isOpen = false;
            }
          }}
        />
      </div>
    {/if}

      {#if activeFilters.length > 0}
        <div class="active-filters">
          {#each activeFilters as filter, index}
            <div class="filter-tag">
              {filter.field} = {filter.value}
              <button on:click={() => removeFilter(index)}>×</button>
            </div>
          {/each}
          <button class="clear-button" on:click={clearAllFilters}>Clear All</button>
        </div>
      {/if}
    </div>
  {/if}
</div>

<style>
  .dropdown {
    position: relative;
    display: inline-block;
  }

  .filter-button {
    padding: 0.25rem 1.25rem;
    background-color: white;
    color: black;
    border: 1.25px solid #d1d5db;
    border-radius: 0.5rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-family: 'Open Sans', sans-serif;
    font-weight: 500;
    transition: background-color 0.2s, color 0.2s;
  }

  .filter-button:hover {
    background-color: #f3f4f6;
  }

  .dropdown-panel {
    position: absolute;
    top: 110%;
    left: 0;
    background: white;
    border: 1px solid #ccc;
    border-radius: 0.75rem;
    padding: 1rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    z-index: 10;
    width: 300px;
  }

  .field-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.25rem 1rem;
    margin-bottom: 1rem;
  }

  .field-option {
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.875rem;
  }

  /* Filter Column Name Buttons */
  .field-option input[type="radio"] {
    appearance: none;
    width: 1rem;
    height: 1rem;
    border: 2px solid #d1d5db;    
    border-radius: 9999px;
    background-color: #f9fafb;     
    display: inline-block;
    position: relative;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .field-option input[type="radio"]:checked {
    background-color: #3b82f6;      
    border-color: #3b82f6;
  }

  .field-option input[type="radio"]:checked::after {
    content: '';
    position: absolute;
    top: 2px;
    left: 2px;
    width: 0.5rem;
    height: 0.5rem;
    background-color: white;
    border-radius: 9999px;
  }

  
  .filter-input {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    margin-bottom: 1rem;
  }

  .date-range input[type="date"] {
    padding: 0.5rem 0.80rem;
    font-size: 0.75rem;
    font-family: 'Open Sans', sans-serif;
    text-transform: uppercase;
    border: 1px solid #d1d5db;
    border-radius: 9999px;
    background-color: #f9fafb;
    color: #111827;

  }

  .active-filters {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 0.75rem;
  }

  .filter-tag {
    background-color: #3b82f6;
    color: white;
    padding: 0.35rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    font-weight: 500;
    letter-spacing: 0.2px;
  }

  .filter-tag button {
    background: transparent;
    border: none;
    color: white;
    cursor: pointer;
    font-size: 0.85rem;
    padding: 0;
    line-height: 1;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .close-button {
    position: absolute;
    top: 0.5rem;
    right: 0.5rem;
    background: none;
    border: none;
    font-size: 1.25rem;
    cursor: pointer;
    color: #ef4444;
  }

  .clear-button {
    background-color: #ef4444;
    color: white;
    padding: 0.35rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    font-weight: 500;
    letter-spacing: 0.2px;
  }

  svg {
    width: 1.5rem;
    height: 1.5rem;
    stroke: black;
    stroke-width: 1.5;
  }

  .divider {
  border: none;
  height: 1px;
  background-color: #d1d5db; 
  margin: 0.75rem 0;
}

</style>
<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  export let employees: Array<Record<string, any>> = [];
  const dispatch = createEventDispatcher();

  let isOpen = false;
  let selectedField = '';
  let inputValue = '';
  let activeFilters: { field: string, value: string }[] = [];
  
  const fields = [
    "Employee no.",
    "Date hired",
    "Cost center",
    "Name",
    "Position",
    "Rank",
    "Department",
    "Last day",
    "Status"
  ];

  function toggleDropdown() {
    isOpen = !isOpen;
  }

  function selectField(field: string) {
    selectedField = field;
    inputValue = '';
  }


  function addFilter() {
    if (selectedField && inputValue) {
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
    clearAllFilters();
  }

  function clearAllFilters() {
    activeFilters = [];
    applyFilters();
  }

  function applyFilters() {
  let filtered = employees;

  activeFilters.forEach(filter => {
    const key = mapFieldToKey(filter.field);
    filtered = filtered.filter(emp =>
      emp[key]?.toLowerCase().includes(filter.value.toLowerCase())
    );
  });

  dispatch('filter', { filtered });
}

function mapFieldToKey(field: string): string {
  const map: Record<string, string> = {
    "Employee no.": "employee_no",
    "Date hired": "date_hired",
    "Cost center": "cost_center",
    "Name": "name",
    "Position": "position_title",
    "Rank": "rank",
    "Department": "department",
    "Last day": "last_day",
    "Status": "status"
  };
  return map[field] || field;
}

</script>

<style>
  .dropdown {
    position: relative;
    display: inline-block;
  }

  .filter-button {
    padding: 0.5rem 1.5rem;
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
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1rem;
  }

  .filter-input input {
    flex: 1;
    padding: 0.5rem 0.75rem;
    border: 1px solid #d1d5db;
    border-radius: 0.375rem;
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

  svg {
    width: 1.5rem;
    height: 1.5rem;
    stroke: black;
    stroke-width: 1.5;
  }

  .divider {
  border: none;
  height: 1px;
  background-color: #d1d5db; /* Tailwind's gray-300 */
  margin: 0.75rem 0;
}

  
</style>



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

      {#if selectedField}
        <div class="filter-input">
          <input
          type="text"
          bind:value={inputValue}
          placeholder={`Enter ${selectedField}...`}
          class="w-full px-2 py-1 border rounded mb-3"
          on:keydown={(e) => {
            if (e.key === 'Enter') {
              addFilter();
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
        </div>
      {/if}
    </div>
  {/if}
</div>



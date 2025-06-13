<script>

    // On sort function from the parent Data page
    export let onSort;
    let years = ["UG1", "UG2", "UG3", "UG4", "-"]
    // State variables
    let isOpen = false;
    let sortCategory = "course"; // Default sort option
    let filterCategories = []; // Selected filter options
    $: allSelected = years.length === filterCategories.length

    function toggleAll() {
      filterCategories = allSelected ? [] : [...years]
		}

        // Clear all selections function
    function clearSortAndFilter() {
        sortCategory = "course"; // Reset to default
        filterCategories = []; // Clear all selections
        console.log("All selections cleared");
    }
    // Sort and filter function
    function sortAndFilter() {
      isOpen = false;
      
      

      
      onSort(sortCategory, filterCategories);
      
      
      console.log("Sorting by:", sortCategory);
      console.log("Filtering by:", filterCategories);
    }
  </script>
  
  <div class="relative z-100">
    

    <button class="px-4 py-2 border border-gray-300 rounded-lg flex items-center gap-2 bg-white" on:click={() => isOpen = !isOpen} >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
        </svg>
        Filters
    </button>
    
    {#if isOpen}
      <div class="dropdown-panel">
        <div class="panel-header">
          <h2>Sort & Filter</h2>
          <button on:click={() => isOpen = false} class="close-btn">×</button>
        </div>
        
        <!-- Sort Section -->
        <div class="section">
          <div class="section-header">
            <h3>Sort by</h3>
          </div>
          
          <div class="grid-options">
            <label class="radio-option">
              <input type="radio" bind:group={sortCategory} value="course">
              <span>Course</span>
            </label>
            
            <label class="radio-option">
              <input type="radio" bind:group={sortCategory} value="type">
              <span>Type</span>
            </label>
            
            <label class="radio-option">
              <input type="radio" bind:group={sortCategory} value="days">
              <span>Day</span>
            </label>

            

              <label class="radio-option">
                <input type="radio" bind:group={sortCategory} value="location">
                <span>Room</span>
              </label>

              


              <label class="radio-option">
                <input type="radio" bind:group={sortCategory} value="instructor">
                <span>Instructor</span>
              </label>


              <label class="radio-option">
                <input type="radio" bind:group={sortCategory} value="load">
                <span>Load</span>
              </label>

              
          </div>
        </div>
        
        <!-- Filter Section -->
        <div class="section">
          <div class="section-header">
            <h3>Year Level</h3>
            
          </div>
          
          <div class="grid-options">

            <label class="checkbox-option">
                <input type="checkbox" bind:group={filterCategories} on:click={toggleAll} checked={allSelected}>
                <span>All</span>
              </label>
              
            <label class="checkbox-option">
              <input type="checkbox" bind:group={filterCategories} value="UG1">
              <span>UG1</span>
            </label>
            
            <label class="checkbox-option">
              <input type="checkbox" bind:group={filterCategories} value="UG2">
              <span>UG2</span>
            </label>
            
            <label class="checkbox-option">
              <input type="checkbox" bind:group={filterCategories} value="UG3">
              <span>UG3</span>
            </label>
            
            <label class="checkbox-option">
              <input type="checkbox" bind:group={filterCategories} value="UG4">
              <span>UG4</span>
            </label>

            <label class="checkbox-option">
              <input type="checkbox" bind:group={filterCategories} value="-">
              <span>Misc.</span>
            </label>
          </div>
        </div>
        
        
        
        <!-- Clear and Results buttons -->
        <div class="actions">
          <button class="clear-btn" on:click={clearSortAndFilter} >Reset</button>
          <button on:click={sortAndFilter} class=" bg-green-500 hover:bg-green-600 results-btn">View results</button>
        </div>
      </div>
    {/if}
  </div>
  
  <style>
    .relative {
      position: relative;
    }
    
    .dropdown-panel {
      position: absolute;
      top: 100%;
      right: 0;
      width: 350px; /* Increased width */
      background: white;
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
      z-index: 50;
    }
    
    .panel-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 16px;
      border-bottom: 1px solid #eee;
    }
    
    .panel-header h2 {
      font-size: 18px;
      font-weight: 600;
      margin: 0;
    }
    
    .close-btn {
      font-size: 24px;
      background: none;
      border: none;
      cursor: pointer;
    }
    
    .section {
      border-bottom: 1px solid #eee;
    }
    
    .section-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 12px 16px;
      cursor: pointer;
    }
    
    .section-header h3 {
      font-size: 16px;
      font-weight: 500;
      margin: 0;
    }
    
    .grid-options {
      padding: 0 16px 16px;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
    }
    
    .radio-option, .checkbox-option {
      display: flex;
      align-items: center;
      gap: 8px;
      cursor: pointer;
    }
    
    .actions {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 16px;
    }
    
    .clear-btn {
      background: none;
      border: none;
      color: #777;
      cursor: pointer;
      font-size: 14px;
    }
    
    .results-btn {
      color: white;
      border: none;
      border-radius: 10px;
      padding: 10px 20px;
      font-weight: 500;
      cursor: pointer;
      width: 100%;
      max-width: 200px;
    }
  </style>
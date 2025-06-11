<script>
    export let employees = [];

    let sortField = '';
    let sortDirection = 'asc';

    function handleSort(field) {
        if (sortField == field) {
            sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
        } else {
            sortField = field;
            sortDirection = 'asc';
        }
    }

    function handleDelete(employee) {
        // delete
    }

    $: sortedEmployees = [...employees].sort((a, b) => {
        if (!sortField) return 0;
        
        let aVal = a[sortField];
        let bVal = b[sortField];
        
        // date sorting
        if (sortField === 'date_hired' || sortField === 'last_day') {
            aVal = new Date(aVal);
            bVal = new Date(bVal);
        }
        
        if (aVal < bVal) return sortDirection === 'asc' ? -1 : 1;
        if (aVal > bVal) return sortDirection === 'asc' ? 1 : -1;
        
        return 0;
    });

    function formatDate(dateString) {
        return new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
    });
  }
</script>

<div class="overflow-x-auto">

    <table class="min-w-full text-sm text-left text-gray-700 bg-white">
        <thead class="bg-gray-100 text-xs text-gray-500 uppercase">
            <tr>
                <!---------- Employee no. ---------->
                <th
                    class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors"
                    on:click={() => handleSort('employee_no')}
                >
                <div class="flex items-center gap-1">
                    Employee no.
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        {#if sortDirection === 'asc'}
                        <path fill-rule="evenodd" d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" />
                        {:else}
                        <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" />
                        {/if}
                    </svg>
                </div>
                </th>

                <!---------- Date hired ---------->
                <th 
                    class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors"
                    on:click={() => handleSort('date_hired')}
                >
                <div class="flex items-center gap-1">
                    Date hired
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        {#if sortDirection === 'asc'}
                        <path fill-rule="evenodd" d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" />
                        {:else}
                        <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" />
                        {/if}
                    </svg>
                </div>

                <!---------- Cost center ---------->
                </th>
                    <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">
                    Cost center
                </th>

                <!---------- Name ---------->
                <th 
                    class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors"
                    on:click={() => handleSort('name')}
                >
                <div class="flex items-center gap-1">
                    Name
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        {#if sortDirection === 'asc'}
                        <path fill-rule="evenodd" d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" />
                        {:else}
                        <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" />
                        {/if}
                    </svg>
                </div>
                </th>

                <!---------- Position title ---------->
                <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">
                    Position title
                </th>

                <!---------- Rank ---------->
                <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">
                    Rank
                </th>

                <!---------- Department ---------->
                <th 
                    class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors"
                    on:click={() => handleSort('department')}
                >
                <div class="flex items-center gap-1">
                    Department
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        {#if sortDirection === 'asc'}
                        <path fill-rule="evenodd" d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" />
                        {:else}
                        <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" />
                        {/if}
                    </svg>
                </div>
                </th>

                <!---------- Last day ---------->
                <th 
                    class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors"
                    on:click={() => handleSort('last_day')}
                >
                <div class="flex items-center gap-1">
                    Last day
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        {#if sortDirection === 'asc'}
                        <path fill-rule="evenodd" d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" />
                        {:else}
                        <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" />
                        {/if}
                    </svg>
                </div>
                </th>

                <!---------- Status ---------->
                <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">
                    Status
                </th>

                <!---------- Actions ---------->
                <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">
                    Actions
                </th>
            </tr>
        </thead>

        <tbody class="bg-white divide-y divide-gray-200">
            {#each sortedEmployees as employee, index (employee.employee_no)}
                <tr class="hover:bg-gray-50 transition-colors">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {employee.employee_no}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {formatDate(employee.date_hired)}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {employee.cost_center}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {employee.name}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {employee.position_title}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {employee.rank}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {employee.department}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {formatDate(employee.last_day)}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                    <span class="inline-flex px-2 py-1 text-xs font-semibold rounded-full {employee.status === 'processed' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}">
                    {employee.status === 'processed' ? 'Processed' : 'Unprocessed'}
                    </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <div class="relative">
                    <button 
                        class="text-gray-400 hover:text-gray-600 focus:outline-none"
                    >
                        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"/>
                        </svg>
                    </button>
                    </div>
                </td>
                </tr>
            {/each}
        </tbody>
    </table>
    
    {#if sortedEmployees.length === 0}
        <div class="text-center py-12">
        <!--
        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        -->
        <h3 class="mt-2 text-sm font-medium text-gray-900">No employees found</h3>
        </div>
    {/if}
</div>

<!-- component
<div class="p-6 overflow-scroll px-0">
  <table class="mt-4 w-full min-w-max table-auto text-left">
    <thead>
      <tr>
        <th class="cursor-pointer border-y border-blue-gray-100 bg-blue-gray-50/50 p-4 transition-colors hover:bg-blue-gray-50">
            <p class="antialiased font-sans text-sm text-blue-gray-900 flex items-center justify-between gap-2 font-normal leading-none opacity-70">Project <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" aria-hidden="true" class="h-4 w-4">
                <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 15L12 18.75 15.75 15m-7.5-6L12 5.25 15.75 9"></path>
                </svg>
          </p>
        </th>
        <th class="cursor-pointer border-y border-blue-gray-100 bg-blue-gray-50/50 p-4 transition-colors hover:bg-blue-gray-50">
          <p class="antialiased font-sans text-sm text-blue-gray-900 flex items-center justify-between gap-2 font-normal leading-none opacity-70">Teamlead <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" aria-hidden="true" class="h-4 w-4">
              <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 15L12 18.75 15.75 15m-7.5-6L12 5.25 15.75 9"></path>
            </svg>
          </p>
        </th>
        <th class="cursor-pointer border-y border-blue-gray-100 bg-blue-gray-50/50 p-4 transition-colors hover:bg-blue-gray-50">
          <p class="antialiased font-sans text-sm text-blue-gray-900 flex items-center justify-between gap-2 font-normal leading-none opacity-70">Function <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" aria-hidden="true" class="h-4 w-4">
              <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 15L12 18.75 15.75 15m-7.5-6L12 5.25 15.75 9"></path>
            </svg>
          </p>
        </th>
        <th class="cursor-pointer border-y border-blue-gray-100 bg-blue-gray-50/50 p-4 transition-colors hover:bg-blue-gray-50">
          <p class="antialiased font-sans text-sm text-blue-gray-900 flex items-center justify-between gap-2 font-normal leading-none opacity-70">Status <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" aria-hidden="true" class="h-4 w-4">
              <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 15L12 18.75 15.75 15m-7.5-6L12 5.25 15.75 9"></path>
            </svg>
          </p>
        </th>
        <th class="cursor-pointer border-y border-blue-gray-100 bg-blue-gray-50/50 p-4 transition-colors hover:bg-blue-gray-50">
          <p class="antialiased font-sans text-sm text-blue-gray-900 flex items-center justify-between gap-2 font-normal leading-none opacity-70">Deadline <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" aria-hidden="true" class="h-4 w-4">
              <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 15L12 18.75 15.75 15m-7.5-6L12 5.25 15.75 9"></path>
            </svg>
          </p>
        </th>
        <th class="cursor-pointer border-y border-blue-gray-100 bg-blue-gray-50/50 p-4 transition-colors hover:bg-blue-gray-50">
          <p class="antialiased font-sans text-sm text-blue-gray-900 flex items-center justify-between gap-2 font-normal leading-none opacity-70">Actions</p>
        </th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="p-4 border-b border-blue-gray-50">
          <div class="flex items-center gap-3">
            <div class="flex flex-col">
              <p class="block antialiased font-sans text-sm leading-normal text-blue-gray-900 font-normal">React Project</p>
              <p class="block antialiased font-sans text-sm leading-normal text-blue-gray-900 font-normal opacity-70">Start date: 10 Dec 2023</p>
            </div>
          </div>
        </td>
        <td class="p-4 border-b border-blue-gray-50">
          <div class="flex items-center gap-3">
            <img src="https://demos.creative-tim.com/test/corporate-ui-dashboard/assets/img/team-3.jpg" alt="John Michael" class="inline-block relative object-cover object-center !rounded-full w-9 h-9 rounded-md">
            <div class="flex flex-col">
              <p class="block antialiased font-sans text-sm leading-normal text-blue-gray-900 font-normal">John Michael</p>
              <p class="block antialiased font-sans text-sm leading-normal text-blue-gray-900 font-normal opacity-70">john@creative-tim.com</p>
            </div>
          </div>
        </td>
        <td class="p-4 border-b border-blue-gray-50">
          <div class="flex flex-col">
            <p class="block antialiased font-sans text-sm leading-normal text-blue-gray-900 font-normal">Manager</p>
            <p class="block antialiased font-sans text-sm leading-normal text-blue-gray-900 font-normal opacity-70">Organization</p>
          </div>
        </td>
        <td class="p-4 border-b border-blue-gray-50">
          <div class="w-max">
            <div class="relative grid items-center font-sans font-bold uppercase whitespace-nowrap select-none bg-green-500/20 text-green-600 py-1 px-2 text-xs rounded-md" style="opacity: 1;">
              <span class="">Completed</span>
            </div>
          </div>
        </td>
        <td class="p-4 border-b border-blue-gray-50">
          <p class="block antialiased font-sans text-sm leading-normal text-blue-gray-900 font-normal">23/04/18</p>
        </td>
        <td class="p-4 border-b border-blue-gray-50">
          <button class="relative align-middle select-none font-sans font-medium text-center uppercase transition-all disabled:opacity-50 disabled:shadow-none disabled:pointer-events-none w-10 max-w-[40px] h-10 max-h-[40px] rounded-lg text-xs text-blue-gray-500 hover:bg-blue-gray-500/10 active:bg-blue-gray-500/30" type="button">
            <span class="absolute top-1/2 left-1/2 transform -translate-y-1/2 -translate-x-1/2">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" class="h-4 w-4">
                <path d="M21.731 2.269a2.625 2.625 0 00-3.712 0l-1.157 1.157 3.712 3.712 1.157-1.157a2.625 2.625 0 000-3.712zM19.513 8.199l-3.712-3.712-12.15 12.15a5.25 5.25 0 00-1.32 2.214l-.8 2.685a.75.75 0 00.933.933l2.685-.8a5.25 5.25 0 002.214-1.32L19.513 8.2z"></path>
              </svg>
            </span>
          </button>
        </td>
      </tr>
      <tr>
        <td class="p-4 border-b border-blue-gray-50">
          <div class="flex items-center gap-3">
            <div class="flex flex-col">
              <p class="block antialiased font-sans text-sm leading-normal text-blue-gray-900 font-normal">Angular Project</p>
              <p class="block antialiased font-sans text-sm leading-normal text-blue-gray-900 font-normal opacity-70">Start date: 10 Dec 2023</p>
            </div>
          </div>
        </td>
        <td class="p-4 border-b border-blue-gray-50">
          <div class="flex items-center gap-3">
            <img src="https://demos.creative-tim.com/test/corporate-ui-dashboard/assets/img/team-2.jpg" alt="Alexa Liras" class="inline-block relative object-cover object-center !rounded-full w-9 h-9 rounded-md">
            <div class="flex flex-col">
              <p class="block antialiased font-sans text-sm leading-normal text-blue-gray-900 font-normal">Alexa Liras</p>
              <p class="block antialiased font-sans text-sm leading-normal text-blue-gray-900 font-normal opacity-70">alexa@creative-tim.com</p>
            </div>
          </div>
        </td>
        <td class="p-4 border-b border-blue-gray-50">
          <div class="flex flex-col">
            <p class="block antialiased font-sans text-sm leading-normal text-blue-gray-900 font-normal">Programator</p>
            <p class="block antialiased font-sans text-sm leading-normal text-blue-gray-900 font-normal opacity-70">Developer</p>
          </div>
        </td>
        <td class="p-4 border-b border-blue-gray-50">
          <div class="w-max">
            <div class="relative grid items-center font-sans font-bold uppercase whitespace-nowrap select-none bg-purple-500/20 text-purple-600 py-1 px-2 text-xs rounded-md" style="opacity: 1;">
              <span class="">active</span>
            </div>
          </div>
        </td>
        <td class="p-4 border-b border-blue-gray-50">
          <p class="block antialiased font-sans text-sm leading-normal text-blue-gray-900 font-normal">23/04/18</p>
        </td>
        <td class="p-4 border-b border-blue-gray-50">
          <button class="relative align-middle select-none font-sans font-medium text-center uppercase transition-all disabled:opacity-50 disabled:shadow-none disabled:pointer-events-none w-10 max-w-[40px] h-10 max-h-[40px] rounded-lg text-xs text-blue-gray-500 hover:bg-blue-gray-500/10 active:bg-blue-gray-500/30" type="button">
            <span class="absolute top-1/2 left-1/2 transform -translate-y-1/2 -translate-x-1/2">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" class="h-4 w-4">
                <path d="M21.731 2.269a2.625 2.625 0 00-3.712 0l-1.157 1.157 3.712 3.712 1.157-1.157a2.625 2.625 0 000-3.712zM19.513 8.199l-3.712-3.712-12.15 12.15a5.25 5.25 0 00-1.32 2.214l-.8 2.685a.75.75 0 00.933.933l2.685-.8a5.25 5.25 0 002.214-1.32L19.513 8.2z"></path>
              </svg>
            </span>
          </button>
        </td>
      </tr>
      <tr>
        <td class="p-4 border-b border-blue-gray-50">
          <div class="flex items-center gap-3">
            <div class="flex flex-col">
              <p class="block antialiased font-sans text-sm leading-normal text-blue-gray-900 font-normal">Tailwind Project</p>
              <p class="block antialiased font-sans text-sm leading-normal text-blue-gray-900 font-normal opacity-70">Start date: 10 Dec 2023</p>
            </div>
          </div>
        </td>
        <td class="p-4 border-b border-blue-gray-50">
          <div class="flex items-center gap-3">
            <img src="https://demos.creative-tim.com/test/corporate-ui-dashboard/assets/img/team-1.jpg" alt="Laurent Perrier" class="inline-block relative object-cover object-center !rounded-full w-9 h-9 rounded-md">
            <div class="flex flex-col">
              <p class="block antialiased font-sans text-sm leading-normal text-blue-gray-900 font-normal">Laurent Perrier</p>
              <p class="block antialiased font-sans text-sm leading-normal text-blue-gray-900 font-normal opacity-70">laurent@creative-tim.com</p>
            </div>
          </div>
        </td>
        <td class="p-4 border-b border-blue-gray-50">
          <div class="flex flex-col">
            <p class="block antialiased font-sans text-sm leading-normal text-blue-gray-900 font-normal">Executive</p>
            <p class="block antialiased font-sans text-sm leading-normal text-blue-gray-900 font-normal opacity-70">Projects</p>
          </div>
        </td>
        <td class="p-4 border-b border-blue-gray-50">
          <div class="w-max">
            <div class="relative grid items-center font-sans font-bold uppercase whitespace-nowrap select-none bg-yellow-500/20 text-yellow-600 py-1 px-2 text-xs rounded-md" style="opacity: 1;">
              <span class="">Scheduled	
</span>
            </div>
          </div>
        </td>
        <td class="p-4 border-b border-blue-gray-50">
          <p class="block antialiased font-sans text-sm leading-normal text-blue-gray-900 font-normal">19/09/17</p>
        </td>
        <td class="p-4 border-b border-blue-gray-50">
          <button class="relative align-middle select-none font-sans font-medium text-center uppercase transition-all disabled:opacity-50 disabled:shadow-none disabled:pointer-events-none w-10 max-w-[40px] h-10 max-h-[40px] rounded-lg text-xs text-blue-gray-500 hover:bg-blue-gray-500/10 active:bg-blue-gray-500/30" type="button">
            <span class="absolute top-1/2 left-1/2 transform -translate-y-1/2 -translate-x-1/2">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" class="h-4 w-4">
                <path d="M21.731 2.269a2.625 2.625 0 00-3.712 0l-1.157 1.157 3.712 3.712 1.157-1.157a2.625 2.625 0 000-3.712zM19.513 8.199l-3.712-3.712-12.15 12.15a5.25 5.25 0 00-1.32 2.214l-.8 2.685a.75.75 0 00.933.933l2.685-.8a5.25 5.25 0 002.214-1.32L19.513 8.2z"></path>
              </svg>
            </span>
          </button>
        </td>
      </tr>
      <tr>
        <td class="p-4 border-b border-blue-gray-50">
          <div class="flex items-center gap-3">
            <div class="flex flex-col">
              <p class="block antialiased font-sans text-sm leading-normal text-blue-gray-900 font-normal">Laravel Project</p>
              <p class="block antialiased font-sans text-sm leading-normal text-blue-gray-900 font-normal opacity-70">Start date: 10 Dec 2023</p>
            </div>
          </div>
        </td>
        <td class="p-4 border-b border-blue-gray-50">
          <div class="flex items-center gap-3">
            <img src="https://demos.creative-tim.com/test/corporate-ui-dashboard/assets/img/team-4.jpg" alt="Michael Levi" class="inline-block relative object-cover object-center !rounded-full w-9 h-9 rounded-md">
            <div class="flex flex-col">
              <p class="block antialiased font-sans text-sm leading-normal text-blue-gray-900 font-normal">Michael Levi</p>
              <p class="block antialiased font-sans text-sm leading-normal text-blue-gray-900 font-normal opacity-70">michael@creative-tim.com</p>
            </div>
          </div>
        </td>
        <td class="p-4 border-b border-blue-gray-50">
          <div class="flex flex-col">
            <p class="block antialiased font-sans text-sm leading-normal text-blue-gray-900 font-normal">Programator</p>
            <p class="block antialiased font-sans text-sm leading-normal text-blue-gray-900 font-normal opacity-70">Developer</p>
          </div>
        </td>
        <td class="p-4 border-b border-blue-gray-50">
          <div class="w-max">
            <div class="relative grid items-center font-sans font-bold uppercase whitespace-nowrap select-none bg-green-500/20 text-green-600 py-1 px-2 text-xs rounded-md" style="opacity: 1;">
              <span class="">Completed</span>
            </div>
          </div>
        </td>
        <td class="p-4 border-b border-blue-gray-50">
          <p class="block antialiased font-sans text-sm leading-normal text-blue-gray-900 font-normal">24/12/08</p>
        </td>
        <td class="p-4 border-b border-blue-gray-50">
          <button class="relative align-middle select-none font-sans font-medium text-center uppercase transition-all disabled:opacity-50 disabled:shadow-none disabled:pointer-events-none w-10 max-w-[40px] h-10 max-h-[40px] rounded-lg text-xs text-blue-gray-500 hover:bg-blue-gray-500/10 active:bg-blue-gray-500/30" type="button">
            <span class="absolute top-1/2 left-1/2 transform -translate-y-1/2 -translate-x-1/2">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" class="h-4 w-4">
                <path d="M21.731 2.269a2.625 2.625 0 00-3.712 0l-1.157 1.157 3.712 3.712 1.157-1.157a2.625 2.625 0 000-3.712zM19.513 8.199l-3.712-3.712-12.15 12.15a5.25 5.25 0 00-1.32 2.214l-.8 2.685a.75.75 0 00.933.933l2.685-.8a5.25 5.25 0 002.214-1.32L19.513 8.2z"></path>
              </svg>
            </span>
          </button>
        </td>
      </tr>
      <tr>
        <td class="p-4 border-b border-blue-gray-50">
          <div class="flex items-center gap-3">
            <div class="flex flex-col">
              <p class="block antialiased font-sans text-sm leading-normal text-blue-gray-900 font-normal">Astro Project</p>
              <p class="block antialiased font-sans text-sm leading-normal text-blue-gray-900 font-normal opacity-70">Start date: 10 Dec 2023</p>
            </div>
          </div>
        </td>
        <td class="p-4">
          <div class="flex items-center gap-3">
            <img src="https://demos.creative-tim.com/test/corporate-ui-dashboard/assets/img/team-5.jpg" alt="Richard Gran" class="inline-block relative object-cover object-center !rounded-full w-9 h-9 rounded-md">
            <div class="flex flex-col">
              <p class="block antialiased font-sans text-sm leading-normal text-blue-gray-900 font-normal">Richard Gran</p>
              <p class="block antialiased font-sans text-sm leading-normal text-blue-gray-900 font-normal opacity-70">richard@creative-tim.com</p>
            </div>
          </div>
        </td>
        <td class="p-4">
          <div class="flex flex-col">
            <p class="block antialiased font-sans text-sm leading-normal text-blue-gray-900 font-normal">Manager</p>
            <p class="block antialiased font-sans text-sm leading-normal text-blue-gray-900 font-normal opacity-70">Executive</p>
          </div>
        </td>
        <td class="p-4">
          <div class="w-max">
            <div class="relative grid items-center font-sans font-bold uppercase whitespace-nowrap select-none bg-red-500/20 text-red-700 py-1 px-2 text-xs rounded-md" style="opacity: 1;">
              <span class="">Pending</span>
            </div>
          </div>
        </td>
        <td class="p-4">
          <p class="block antialiased font-sans text-sm leading-normal text-blue-gray-900 font-normal">04/10/21</p>
        </td>
        <td class="p-4">
          <button class="relative align-middle select-none font-sans font-medium text-center uppercase transition-all disabled:opacity-50 disabled:shadow-none disabled:pointer-events-none w-10 max-w-[40px] h-10 max-h-[40px] rounded-lg text-xs text-blue-gray-500 hover:bg-blue-gray-500/10 active:bg-blue-gray-500/30" type="button">
            <span class="absolute top-1/2 left-1/2 transform -translate-y-1/2 -translate-x-1/2">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" class="h-4 w-4">
                <path d="M21.731 2.269a2.625 2.625 0 00-3.712 0l-1.157 1.157 3.712 3.712 1.157-1.157a2.625 2.625 0 000-3.712zM19.513 8.199l-3.712-3.712-12.15 12.15a5.25 5.25 0 00-1.32 2.214l-.8 2.685a.75.75 0 00.933.933l2.685-.8a5.25 5.25 0 002.214-1.32L19.513 8.2z"></path>
              </svg>
            </span>
          </button>
        </td>
      </tr>
    </tbody>
  </table>
</div>
<footer class="relative pt-8 pb-6 mt-16">
  <div class="container mx-auto px-4">
    <div class="flex flex-wrap items-center md:justify-between justify-center">
      <div class="w-full md:w-6/12 px-4 mx-auto text-center">
        <div class="text-sm text-gray-500  py-1">
          Made with <a href="https://www.creative-tim.com/product/soft-ui-dashboard-tailwind" class="text-gray-900 hover:text-gray-800" target="_blank">Soft UI</a> by <a href="https://www.creative-tim.com" class="text-gray-900 hover:text-gray-800" target="_blank"> Creative Tim</a>.
        </div>
      </div>
    </div>
  </div>
</footer>
-->
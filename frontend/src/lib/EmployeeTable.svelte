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
    <table class="w-full">
        <thead class="bg-gray-50 border-b border-gray-200">
            <tr>
                <!---------- Employee no. ---------->
                <th 
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors"
                    on:click={() => handleSort('employee_no')}
                >
                <div class="flex items-center gap-1">
                    Employee no.
                    {#if sortField === 'employee_no'}
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        {#if sortDirection === 'asc'}
                        <path fill-rule="evenodd" d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" />
                        {:else}
                        <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" />
                        {/if}
                    </svg>
                    {/if}
                </div>
                </th>

                <!---------- Date hired ---------->
                <th 
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors"
                    on:click={() => handleSort('date_hired')}
                >
                <div class="flex items-center gap-1">
                    Date hired
                    {#if sortField === 'date_hired'}
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        {#if sortDirection === 'asc'}
                        <path fill-rule="evenodd" d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" />
                        {:else}
                        <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" />
                        {/if}
                    </svg>
                    {/if}
                </div>

                <!---------- Cost center ---------->
                </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Cost center
                </th>

                <!---------- Name ---------->
                <th 
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors"
                    on:click={() => handleSort('name')}
                >
                <div class="flex items-center gap-1">
                    Name
                    {#if sortField === 'name'}
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        {#if sortDirection === 'asc'}
                        <path fill-rule="evenodd" d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" />
                        {:else}
                        <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" />
                        {/if}
                    </svg>
                    {/if}
                </div>
                </th>

                <!---------- Position title ---------->
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Position_title
                </th>

                <!---------- Rank ---------->
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Rank
                </th>

                <!---------- Department ---------->
                <th 
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors"
                    on:click={() => handleSort('department')}
                >
                <div class="flex items-center gap-1">
                    Department
                    {#if sortField === 'department'}
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        {#if sortDirection === 'asc'}
                        <path fill-rule="evenodd" d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" />
                        {:else}
                        <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" />
                        {/if}
                    </svg>
                    {/if}
                </div>
                </th>

                <!---------- Last day ---------->
                <th 
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors"
                    on:click={() => handleSort('last_day')}
                >
                <div class="flex items-center gap-1">
                    Last day
                    {#if sortField === 'last_day'}
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        {#if sortDirection === 'asc'}
                        <path fill-rule="evenodd" d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" />
                        {:else}
                        <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" />
                        {/if}
                    </svg>
                    {/if}
                </div>
                </th>

                <!---------- Status ---------->
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                </th>

                <!---------- Actions ---------->
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
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
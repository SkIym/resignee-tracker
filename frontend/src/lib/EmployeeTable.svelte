<script lang="ts">
  import { BASE_URL } from '../constants';

    export let employees: Employee[] = [];
    export let onstatustoggle: (event: { detail: { employee: Employee, action?: string } }) => void;

    import type { Employee } from '../types';

    let sortField: keyof Employee | '' = '';
    let sortDirection = 'asc';
    let editingEmployeeId: string | null = null;
    let editingValue: string = '';

    function handleSort(field: 'name' | 'employee_no' | 'department' | 'position_title' | 'date_hired' | 'last_day') {
        if (sortField == field) {
            sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
        } else {
            sortField = field;
            sortDirection = 'asc';
        }
    }

    $: sortedEmployees = [...employees].sort((a, b) => {
        if (!sortField) return 0;
        let aVal = a[sortField];
        let bVal = b[sortField];
        
        if (sortField === 'date_hired' || sortField === 'last_day') {
            const aDate = new Date(aVal || '1900-01-01');
            const bDate = new Date(bVal || '1900-01-01');
            
            if (aDate < bDate) return sortDirection === 'asc' ? -1 : 1;
            if (aDate > bDate) return sortDirection === 'asc' ? 1 : -1;
            return 0;
        }
        
        const aStr = String(aVal || '');
        const bStr = String(bVal || '');
        
        if (aStr < bStr) return sortDirection === 'asc' ? -1 : 1;
        if (aStr > bStr) return sortDirection === 'asc' ? 1 : -1;
        return 0;
    });

    function formatDate(dateString: string | null | undefined) {
        if (!dateString) return 'N/A';
        
        return new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
      });
    }

    function formatDateForInput(dateString: string | null | undefined) {
        if (!dateString) return '';
        
        const date = new Date(dateString);
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        
        return `${year}-${month}-${day}`;
    }

    function startEditing(employee: Employee) {
        editingEmployeeId = employee.employee_no;
        editingValue = formatDateForInput(employee.last_day);
        // console.log(editingValue);
    }
    async function saveEdit(employee: Employee) {
        try {
            const trimmed = editingValue.trim();
            const parsedDate = new Date(trimmed);

            if (!trimmed || isNaN(parsedDate.getTime())) {
                throw new Error("Invalid date format");
            }

            const res = await fetch(`${BASE_URL}/resignees/${employee.employee_no}/last_day/edit`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'text/plain',
                },
                body: trimmed,
                credentials: 'include',
            });

            if (!res.ok) {
                const text = await res.text();
                throw new Error(`Error ${res.status}: ${text}`);
            }

            const idx = employees.findIndex(emp => emp.employee_no === employee.employee_no);
            if (idx !== -1) {
                employees[idx].last_day = parsedDate.toISOString();
                employees = [...employees];
            }

        } catch (error) {
            console.error('Error updating last day:', error);
            const msg = error instanceof Error ? error.message : 'Unknown error';
            alert(`Failed to update last day: ${msg}`);
        } finally {
            editingEmployeeId = null;
            editingValue = '';
        }
    }




    function cancelEdit() {
        editingEmployeeId = null;
        editingValue = '';
    }

    function toggleStatus(employee: Employee) {
        const currentStatus = employee.processed_date_time ? 'processed' : 'unprocessed';
        // Call the callback function passed from parent
        if (onstatustoggle) {
            onstatustoggle({ detail: { employee } });
        }
    }

    // Handle escape key to cancel editing
    function handleKeydown(event: KeyboardEvent) {
        if (event.key === 'Escape') {
            cancelEdit();
        }
    } 
</script>

<svelte:window on:keydown={handleKeydown} />

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
                    <svg class="w-4 h-4 shrink-0" fill="currentColor" viewBox="0 0 20 20">
                        {#if sortField === 'employee_no' && sortDirection === 'asc'}
                        <path fill-rule="evenodd" d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" />
                        {:else if sortField === 'employee_no' && sortDirection === 'desc'}
                        <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" />
                        {:else}
                        <path fill-rule="evenodd" d="M10 3a1 1 0 01.707.293l3 3a1 1 0 01-1.414 1.414L10 5.414 7.707 7.707a1 1 0 01-1.414-1.414l3-3A1 1 0 0110 3zm-3.707 9.293a1 1 0 011.414 0L10 14.586l2.293-2.293a1 1 0 011.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" />
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
                    <svg class="w-4 h-4 shrink-0" fill="currentColor" viewBox="0 0 20 20">
                        {#if sortField === 'date_hired' && sortDirection === 'asc'}
                        <path fill-rule="evenodd" d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" />
                        {:else if sortField === 'date_hired' && sortDirection === 'desc'}
                        <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" />
                        {:else}
                        <path fill-rule="evenodd" d="M10 3a1 1 0 01.707.293l3 3a1 1 0 01-1.414 1.414L10 5.414 7.707 7.707a1 1 0 01-1.414-1.414l3-3A1 1 0 0110 3zm-3.707 9.293a1 1 0 011.414 0L10 14.586l2.293-2.293a1 1 0 011.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" />
                        {/if}
                    </svg>
                </div>
                </th>

                <!---------- Cost center ---------->
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
                    <svg class="w-4 h-4 shrink-0" fill="currentColor" viewBox="0 0 20 20">
                        {#if sortField === 'name' && sortDirection === 'asc'}
                        <path fill-rule="evenodd" d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" />
                        {:else if sortField === 'name' && sortDirection === 'desc'}
                        <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" />
                        {:else}
                        <path fill-rule="evenodd" d="M10 3a1 1 0 01.707.293l3 3a1 1 0 01-1.414 1.414L10 5.414 7.707 7.707a1 1 0 01-1.414-1.414l3-3A1 1 0 0110 3zm-3.707 9.293a1 1 0 011.414 0L10 14.586l2.293-2.293a1 1 0 011.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" />
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
                    <svg class="w-4 h-4 shrink-0" fill="currentColor" viewBox="0 0 20 20">
                        {#if sortField === 'department' && sortDirection === 'asc'}
                        <path fill-rule="evenodd" d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" />
                        {:else if sortField === 'department' && sortDirection === 'desc'}
                        <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" />
                        {:else}
                        <path fill-rule="evenodd" d="M10 3a1 1 0 01.707.293l3 3a1 1 0 01-1.414 1.414L10 5.414 7.707 7.707a1 1 0 01-1.414-1.414l3-3A1 1 0 0110 3zm-3.707 9.293a1 1 0 011.414 0L10 14.586l2.293-2.293a1 1 0 011.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" />
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
                    <svg class="w-4 h-4 shrink-0" fill="currentColor" viewBox="0 0 20 20">
                        {#if sortField === 'last_day' && sortDirection === 'asc'}
                        <path fill-rule="evenodd" d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" />
                        {:else if sortField === 'last_day' && sortDirection === 'desc'}
                        <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" />
                        {:else}
                        <path fill-rule="evenodd" d="M10 3a1 1 0 01.707.293l3 3a1 1 0 01-1.414 1.414L10 5.414 7.707 7.707a1 1 0 01-1.414-1.414l3-3A1 1 0 0110 3zm-3.707 9.293a1 1 0 011.414 0L10 14.586l2.293-2.293a1 1 0 011.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" />
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
                    Mark as Processed
                </th>
            </tr>
        </thead>

        <tbody class="bg-white divide-y divide-gray-200">
            {#each sortedEmployees as employee, index (employee.employee_no)}
                <tr class="hover:bg-gray-50 transition-colors">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {String(employee.employee_no || '')}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {formatDate(employee.date_hired)}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {String(employee.cost_center || '')}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {String(employee.name || '')}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {String(employee.position_title || '')}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {String(employee.rank || '')}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {String(employee.department || '')}
                </td>

                <!-- Editable Last Day Cell -->
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    <div class="flex items-center gap-2">
                        {#if editingEmployeeId === employee.employee_no}
                            <!-- Edit Mode: Date Input + Check Icon -->
                            <input
                                type="date"
                                bind:value={editingValue}
                                class="text-sm border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                on:blur={() => saveEdit(employee)}
                            />
                            <button
                                type="button"
                                on:click={() => saveEdit(employee)}
                                class="text-green-600 hover:text-green-800 transition-colors"
                                title="Save changes"
                            >
                                <!-- Check Icon -->
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                                </svg>
                            </button>
                        {:else}
                            <!-- Display Mode: Date + Pencil Icon -->
                            <span class="flex-1">
                                {formatDate(employee.last_day)}
                            </span>
                            <button
                                type="button"
                                on:click={() => startEditing(employee)}
                                class="text-gray-400 hover:text-gray-600 transition-colors"
                                title="Edit last day"
                            >
                                <!-- Pencil/Edit Icon -->
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                                </svg>
                            </button>
                        {/if}
                    </div>
                </td>

                <!-- Status Badge -->
                <td class="px-6 py-4 whitespace-nowrap">
                  <span
                    class="inline-flex px-2 py-1 text-xs font-medium rounded-full {employee.processed_date_time ? 'bg-[#CFEED8] text-[#1E9F37]' : 'bg-[#FED9DA] text-[#D7313E]'}"
                  >
                    {employee.processed_date_time ? 'Processed' : 'Unprocessed'}
                  </span>
                </td>

                <!-- Toggle Checkbox -->
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  <input
                    type="checkbox"
                    class="w-5 h-5 text-green-600 rounded border-gray-300 focus:ring-green-500"
                    checked={employee.processed_date_time !== null}
                    on:change={() => toggleStatus(employee)}
                  />
                </td>

                </tr>
            {/each}
        </tbody>
    </table>
    
    {#if sortedEmployees.length === 0}
        <div class="text-center py-12">
        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <h3 class="mt-2 text-sm font-medium text-gray-900">No employees found</h3>
        </div>
    {/if}
</div>
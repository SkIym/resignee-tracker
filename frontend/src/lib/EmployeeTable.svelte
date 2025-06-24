<script lang="ts">
    export let employees: Employee[] = [];

    import { onMount, onDestroy } from 'svelte';
    import type { Employee } from '../types';
    import toast, { Toaster } from 'svelte-5-french-toast';

    let sortField: keyof Employee | '' = '';
    let sortDirection = 'asc';
    let editingEmployeeId: {id: string; key: keyof Employee }| null = null;
    let editingValue: string = '';

    // Sticky scrollbar elements
    let tableContainer: HTMLDivElement;
    let stickyScrollbar: HTMLDivElement;
    let updateScrollbarWidth: () => void;
    let observer: MutationObserver | null = null;
    let scrollWrapper: HTMLDivElement;

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

    // Watch for employees changes to update scrollbar
    $: if (employees && tableContainer && stickyScrollbar) {
        setTimeout(async () => await setupScrollbarSync(), 50);
    }

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

    function startEditing(employee: Employee, key: keyof Employee) {
        editingEmployeeId = { id: employee.employee_no, key };
        editingValue = formatDateForInput(employee[key] as string | null | undefined);
    }

    async function saveEdit(employee: Employee) {
         if (!editingEmployeeId) return;
        const { key } = editingEmployeeId;
        try {
            const trimmed = editingValue.trim();
            const parsedDate = new Date(trimmed);

            if (!trimmed || isNaN(parsedDate.getTime())) {
                throw new Error("Invalid date format");
            }

            const res = await fetch(`https://localhost:8000/resignees/${employee.employee_no}/last_day/edit`, {
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
                toast.success('Changes saved for employee no. ' + employee.employee_no);
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

    async function saveRemarks(employee: Employee) {
        if (!editingEmployeeId) return;
        
        try {
            const trimmedRemarks = editingValue.trim();

            const res = await fetch(`https://localhost:8000/resignees/${employee.employee_no}/remarks`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ remarks: trimmedRemarks }),
                credentials: 'include',
            });

            if (!res.ok) {
                const text = await res.text();
                throw new Error(`Error ${res.status}: ${text}`);
            }

            // Update the local employee data
            const idx = employees.findIndex(emp => emp.employee_no === employee.employee_no);
            if (idx !== -1) {
                employees[idx].remarks = trimmedRemarks;
                employees = [...employees];
                toast.success('Remarks updated for employee no. ' + employee.employee_no);
            }

        } catch (error) {
            console.error('Error updating remarks:', error);
            const msg = error instanceof Error ? error.message : 'Unknown error';
            alert(`Failed to update remarks: ${msg}`);
        } finally {
            editingEmployeeId = null;
            editingValue = '';
        }
    }

    function startEditingRemarks(employee: Employee) {
        editingEmployeeId = { id: employee.employee_no, key: 'remarks' };
        editingValue = String(employee.remarks || '');
    }

    // Handle escape key to cancel editing
    function handleKeydown(event: KeyboardEvent) {
        if (event.key === 'Escape') {
            cancelEdit();
        }
    }

    async function setupScrollbarSync() {
        if (!scrollWrapper || !stickyScrollbar) return;

        const scrollDiv = stickyScrollbar.querySelector('div');

        const syncScroll = (source: HTMLElement, target: HTMLElement) => {
            let ticking = false;
            const handler = () => {
            if (!ticking) {
                window.requestAnimationFrame(() => {
                if (target.scrollLeft !== source.scrollLeft) {
                    target.scrollLeft = source.scrollLeft;
                }
                ticking = false;
                });
                ticking = true;
            }
            };
            return handler;
        };

        const wrapperHandler = syncScroll(scrollWrapper, stickyScrollbar);
        const stickyHandler = syncScroll(stickyScrollbar, scrollWrapper);

        scrollWrapper.addEventListener('scroll', wrapperHandler);
        stickyScrollbar.addEventListener('scroll', stickyHandler);

        // Set width of sticky scrollbar
        updateScrollbarWidth = () => {
            const table = scrollWrapper?.querySelector('table');
            if (table && scrollDiv) {
                // Get the actual scroll width and container width
                const tableWidth = table.scrollWidth;
                const containerWidth = scrollWrapper.clientWidth;

                // Only show scrollbar content if table is wider than container
                if (tableWidth > containerWidth) {
                    scrollDiv.style.width = tableWidth + 'px';
                } else {
                    // If table fits within container, set scrollbar content to container width
                    scrollDiv.style.width = containerWidth + 'px';
                }
            }
        };

        updateScrollbarWidth();

        // Observe content changes to update width
        if (observer) observer.disconnect();
        observer = new MutationObserver(updateScrollbarWidth);
        observer.observe(scrollWrapper, { childList: true, subtree: true });

        // Clean up on destroy
        onDestroy(() => {
            scrollWrapper.removeEventListener('scroll', wrapperHandler);
            stickyScrollbar.removeEventListener('scroll', stickyHandler);
            if (observer) observer.disconnect();
        });
    }

    onMount(() => {
        if (typeof window !== 'undefined') {
            window.addEventListener('resize', () => {
                if (updateScrollbarWidth) updateScrollbarWidth();
            });
        }
        
        return () => {
            if (typeof window !== 'undefined' && updateScrollbarWidth) {
                window.removeEventListener('resize', updateScrollbarWidth);
            }
        };
    });

    onDestroy(() => {
        if (observer) {
            observer.disconnect();
        }
    });
</script>

<Toaster />

<svelte:window on:keydown={handleKeydown} />

<div class="relative">
    <!-- Main scrollable table container -->
    <div class="overflow-hidden" bind:this={tableContainer}>
        <div
        class="overflow-x-auto overflow-y-visible hide-main-scrollbar"
            bind:this={scrollWrapper}
        >
            <table class="min-w-full text-sm text-left text-gray-700 bg-white">
                    <thead class="bg-gray-100 text-xs text-gray-500 uppercase">
                        <tr>
                            <!---------- Employee no. ---------->
                            <th
                                class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors sticky left-0 bg-gray-100"
                                on:click={() => handleSort('employee_no')}
                            >
                            <div class="flex items-center gap-1">
                                #
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
                                class="pl-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors"
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
                            <th class="pl-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">
                                Cost center
                            </th>

                            <!---------- Name ---------->
                            <th 
                                class="pl-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors"
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
                            <th class="pl-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">
                                Position title
                            </th>

                            <!---------- Rank ---------->
                            <th class="pl-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">
                                Rank
                            </th>

                            <!---------- Department ---------->
                            <th 
                                class="pl-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors"
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
                                class="pl-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors"
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

                            <!---------- Batch Deactivation ---------->
                            <th 
                                class="pl-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors"
                                on:click={() => handleSort('last_day')}
                            >
                            <div class="flex items-center gap-1">
                                Batch Deactivation
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

                            <!---------- 3rd Party Systems ---------->
                            <th 
                                class="pl-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors"
                                on:click={() => handleSort('last_day')}
                            >
                            <div class="flex items-center gap-1">
                                3rd Party Systems
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

                            <!---------- Emails ---------->
                            <th 
                                class="pl-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors"
                                on:click={() => handleSort('last_day')}
                            >
                            <div class="flex items-center gap-1">
                                Emails
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

                            <!---------- Windows ---------->
                            <th 
                                class="pl-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors"
                                on:click={() => handleSort('last_day')}
                            >
                            <div class="flex items-center gap-1">
                                Windows
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

                            <!---------- HR Email ---------->
                            <th 
                                class="pl-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors"
                                on:click={() => handleSort('last_day')}
                            >
                            <div class="flex items-center gap-1">
                                HR Email
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

                            <!---------- Remarks ---------->
                            <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">
                                Remarks
                            </th>
                            
                        </tr>
                    </thead>

                    <tbody class="bg-white divide-y divide-gray-200">
                        {#each sortedEmployees as employee, index (employee.employee_no)}
                            <tr class="hover:bg-gray-50 transition-colors">
                            <td class="px-6 py-2 whitespace-normal text-sm font-medium text-gray-900 sticky left-0 bg-white">
                                {String(employee.employee_no || '')}
                            </td>
                            <td class="pl-6 py-2 whitespace-nowrap text-sm text-gray-900">
                                {formatDate(employee.date_hired)}
                            </td>
                            <td class="pl-6 py-2 whitespace-normal text-sm text-gray-900">
                                {String(employee.cost_center || '')}
                            </td>
                            <td class="pl-6 py-2 whitespace-normal text-sm font-medium text-gray-900">
                                {String(employee.name || '')}
                            </td>
                            <td class="pl-6 py-2 whitespace-normal text-sm text-gray-900">
                                {String(employee.position_title || '')}
                            </td>
                            <td class="pl-6 py-2 whitespace-normal text-sm text-gray-900">
                                {String(employee.rank || '')}
                            </td>
                            <td class="pl-6 py-2 whitespace-normal text-sm text-gray-900">
                                {String(employee.department || '')}
                            </td>

                            <!-- Editable Last Day Cell -->
                            <td class="pl-6 py-2 whitespace-nowrap text-sm text-gray-900">
                                <div class="flex items-center gap-2">
                                    {#if editingEmployeeId?.id === employee.employee_no && editingEmployeeId?.key === 'last_day'}
                                        <!-- Edit Mode: Date Input + Check Icon -->
                                        <input
                                            type="date"
                                            bind:value={editingValue}
                                            class="text-sm border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                            on:keydown={(e) => {
                                                if (e.key === 'Enter') {
                                                    saveEdit(employee);
                                                }
                                            }}
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
                                            on:click={() => startEditing(employee, 'last_day')}
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

                            <!-- Editable Batch Deactivation Cell -->
                            <td class="pl-6 py-2 whitespace-nowrap text-sm text-gray-900">
                                <div class="flex items-center gap-2">
                                    {#if editingEmployeeId?.id === employee.employee_no && editingEmployeeId?.key === 'um'}
                                        <!-- Edit Mode: Date Input + Check Icon -->
                                        <input
                                            type="date"
                                            bind:value={editingValue}
                                            class="text-sm border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                            on:keydown={(e) => {
                                                if (e.key === 'Enter') {
                                                    saveEdit(employee);
                                                }
                                            }}
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
                                        <span class="inline-flex px-2 py-1 text-xs font-medium rounded-full {employee.um ? 'bg-[#CFEED8] text-[#1E9F37]}' : 'bg-[#FED9DA] text-[#D7313E]'}">
                                            {employee.um ? formatDate(employee.um) : 'N/A'}
                                        </span>
                                        <button
                                            type="button"
                                            on:click={() => startEditing(employee, 'um')}
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

                            <!-- Editable 3rd Party Systems Cell -->
                            <td class="pl-6 py-2 whitespace-nowrap text-sm text-gray-900">
                                <div class="flex items-center gap-2">
                                    {#if editingEmployeeId?.id === employee.employee_no && editingEmployeeId?.key === 'third_party'}
                                        <!-- Edit Mode: Date Input + Check Icon -->
                                        <input
                                            type="date"
                                            bind:value={editingValue}
                                            class="text-sm border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                            on:keydown={(e) => {
                                                if (e.key === 'Enter') {
                                                    saveEdit(employee);
                                                }
                                            }}
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
                                        <span class="inline-flex px-2 py-1 text-xs font-medium rounded-full {employee.um ? 'bg-[#CFEED8] text-[#1E9F37]}' : 'bg-[#FED9DA] text-[#D7313E]'}">
                                            {formatDate(employee.third_party)}
                                        </span>
                                        <button
                                            type="button"
                                            on:click={() => startEditing(employee, 'third_party')}
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

                            <!-- Editable Emails Cell -->
                            <td class="pl-6 py-2 whitespace-nowrap text-sm text-gray-900">
                                <div class="flex items-center gap-2">
                                    {#if editingEmployeeId?.id === employee.employee_no && editingEmployeeId?.key === 'email'}

                                        <!-- Edit Mode: Date Input + Check Icon -->
                                        <input
                                            type="date"
                                            bind:value={editingValue}
                                            class="text-sm border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                            on:keydown={(e) => {
                                                if (e.key === 'Enter') {
                                                    saveEdit(employee);
                                                }
                                            }}
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
                                        <span class="inline-flex px-2 py-1 text-xs font-medium rounded-full {employee.um ? 'bg-[#CFEED8] text-[#1E9F37]}' : 'bg-[#FED9DA] text-[#D7313E]'}">
                                            {formatDate(employee.email)}
                                        </span>
                                        <button
                                            type="button"
                                            on:click={() => startEditing(employee, 'email')}
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

                            <!-- Editable Windows Cell -->
                            <td class="pl-6 py-2 whitespace-nowrap text-sm text-gray-900">
                                <div class="flex items-center gap-2">
                                     {#if editingEmployeeId?.id === employee.employee_no && editingEmployeeId?.key === 'windows'}
                                        <!-- Edit Mode: Date Input + Check Icon -->
                                        <input
                                            type="date"
                                            bind:value={editingValue}
                                            class="text-sm border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                            on:keydown={(e) => {
                                                if (e.key === 'Enter') {
                                                    saveEdit(employee);
                                                }
                                            }}
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
                                        <span class="inline-flex px-2 py-1 text-xs font-medium rounded-full {employee.um ? 'bg-[#CFEED8] text-[#1E9F37]}' : 'bg-[#FED9DA] text-[#D7313E]'}">
                                            {formatDate(employee.windows)}
                                        </span>
                                        <button
                                            type="button"
                                            on:click={() => startEditing(employee, 'windows')}
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

                            <!-- Editable HR Email Cell -->
                            <td class="pl-6 py-2 whitespace-nowrap text-sm text-gray-900">
                                <div class="flex items-center gap-2">
                                    {#if editingEmployeeId?.id === employee.employee_no && editingEmployeeId?.key === 'hr_email_date'}
                                        <!-- Edit Mode: Date Input + Check Icon -->
                                        <input
                                            type="date"
                                            bind:value={editingValue}
                                            class="text-sm border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                            on:keydown={(e) => {
                                                if (e.key === 'Enter') {
                                                    saveEdit(employee);
                                                }
                                            }}
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
                                            {formatDate(employee.hr_email_date)}
                                        </span>

                                        <!--
                                        <span
                                            class="inline-flex px-2 py-1 text-xs font-medium rounded-full {employee.processed_date_time ? 'bg-[#CFEED8] text-[#1E9F37]' : 'bg-[#FED9DA] text-[#D7313E]'}"
                                        >
                                            {employee.processed_date_time ? 'Processed' : 'Unprocessed'}
                                        </span>
                                        -->

                                        <button
                                            type="button"
                                            on:click={() => startEditing(employee, 'hr_email_date')}
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

                            <!-- Remarks Field -->
                            <td class="px-6 py-2 whitespace-normal text-sm text-gray-900">
                                <div class="flex items-center gap-2">
                                    {#if editingEmployeeId?.id === employee.employee_no}
                                        <!-- Edit Mode: Text Field + Check Icon -->
                                        <textarea
                                            bind:value={editingValue}
                                            rows="3"
                                            class="text-sm border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 h-20 w-40"
                                            on:keydown={(e) => {
                                                if (e.key === 'Enter') {
                                                    saveRemarks(employee);
                                                }
                                            }}
                                        ></textarea>
                                        <button
                                            type="button"
                                            on:click={() => saveRemarks(employee)}
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
                                            {String(employee.remarks || 'N/A')}
                                        </span>

                                        <button
                                            type="button"
                                            on:click={() => startEditingRemarks(employee)}
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
        </div>
    
    <!-- Always Visible Sticky Scrollbar at Bottom -->
    <div class="sticky-scrollbar-container bg-gray-50 border-t border-gray-300 h-5 z-10" bind:this={stickyScrollbar}>
        <div class="h-5"></div>
    </div>
</div>

<style>
    /* Hide the main table scrollbar but keep sticky scrollbar visible */
    .hide-main-scrollbar::-webkit-scrollbar {
        display: none;
    }
    .hide-main-scrollbar {
        -ms-overflow-style: none;
        scrollbar-width: none;
    }

    /* Always visible sticky scrollbar */
    .sticky-scrollbar-container {
        position: sticky;
        bottom: 0;
        left: 0;
        right: 0;
        overflow-x: auto;
        overflow-y: hidden;
    }

    /* Show scrollbar for sticky container */
    .sticky-scrollbar-container::-webkit-scrollbar {
        height: 8px;
    }

    .sticky-scrollbar-container::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }

    .sticky-scrollbar-container::-webkit-scrollbar-thumb {
        background: #c1c1c1;
        border-radius: 4px;
    }

    .sticky-scrollbar-container::-webkit-scrollbar-thumb:hover {
        background: #a8a8a8;
    }
</style>
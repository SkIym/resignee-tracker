<script lang="ts">
  import { BASE_URL } from '../constants';

    export let employees: Employee[] = [];
    export let onstatustoggle: (event: { detail: { employee: Employee, action?: string } }) => void;
    export let onEmployeeUpdate: (() => void) | undefined = undefined;

    import { onMount, onDestroy } from 'svelte';
    import type { Employee } from '../types';
    import toast, { Toaster } from 'svelte-5-french-toast';

    let sortField: keyof Employee | '' = '';
    let sortDirection = 'asc';
    let editingEmployeeId: {id: string; key: keyof Employee }| null = null;
    let editingValue: string = '';

    // Sticky scrollbar elements
    let tableContainer: HTMLDivElement | null = null;
    let stickyScrollbar: HTMLDivElement | null = null;
    let updateScrollbarWidth: () => void;
    let observer: MutationObserver | null = null;
    let scrollWrapper: HTMLDivElement | null = null;

    function handleSort(field: 'name' | 'employee_no' | 'department' | 'position_title' | 'date_hired' | 'last_day' | 'um' | 'third_party' | 'email' | 'windows' | 'date_hr_emailed' ) {
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

        if (typeof aVal === 'boolean' || typeof bVal === 'boolean') {
            return 0;
        }
        
        if (sortField === 'date_hired' || sortField === 'last_day' || sortField === 'um' || sortField === 'third_party' || sortField === 'email' || sortField === 'windows') {
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

        if (typeof employee[key] === 'boolean') return

        // Handle special "1900-01-01" date by clearing the input
        if (isNoAccountDate(employee[key])) {
            editingValue = '';
        } else {
            editingValue = formatDateForInput(employee[key] as string | null | undefined);
        }
    }

    async function saveEdit(employee: Employee) {
        if (!editingEmployeeId) return;
        const { key } = editingEmployeeId;
        try {
            const trimmed = editingValue.trim();
            let body, succesxsessage, endpoint;

            // Handle special "NO_ACCOUNT" value with a special date
            if (trimmed === 'NO_ACCOUNT') {
                body = '1900-01-01';
                succesxsessage = 'Marked as "No existing account" for employee no. ' + employee.employee_no;
            } else {
                // Validate date format for regular date entries
                const parsedDate = new Date(trimmed);
                if (!trimmed || isNaN(parsedDate.getTime())) {
                    throw new Error("Invalid date format");
                }
                body = trimmed;
                succesxsessage = 'Changes saved for employee no. ' + employee.employee_no;
            }

            // Set endpoint based on the field being edited
            switch (key) {
                case 'last_day':
                    endpoint = `${BASE_URL}/resignees/${employee.employee_no}/last_day`;
                    break;
                case 'um':
                    endpoint = `${BASE_URL}/resignees/${employee.employee_no}/um`;
                    break;
                case 'third_party':
                    endpoint = `${BASE_URL}/resignees/${employee.employee_no}/third-party`;
                    break;
                case 'email':
                    endpoint = `${BASE_URL}/resignees/${employee.employee_no}/email`;
                    break;
                case 'windows':
                    endpoint = `${BASE_URL}/resignees/${employee.employee_no}/windows`;
                    break;
                case 'date_hr_emailed':
                    endpoint = `${BASE_URL}/resignees/${employee.employee_no}/date_hr_emailed`;
                    break;
                default:
                    throw new Error(`Unknown field: ${key}`);
            }

            const res = await fetch(endpoint, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'text/plain',
                },
                body: body,
                credentials: 'include',
            });

            if (!res.ok) {
                const text = await res.text();
                throw new Error(`Error ${res.status}: ${text}`);
            }

            const data = await res.json()
            const idx = employees.findIndex(emp => emp.employee_no === employee.employee_no);
            if (idx !== -1) {
                if (trimmed === 'NO_ACCOUNT') {
                    if (key in employees[idx]) {
                        (employees[idx] as any)[key] = '1900-01-01';
                        const late_key = key.concat("_late") as keyof Employee;
                        (employees[idx] as any)[late_key] = false
                    }
                } else {
                    if (key in employees[idx]) {
                        (employees[idx] as any)[key] = new Date(trimmed).toISOString();
                    }
                    if ((key == 'um') || (key == 'third_party') || (key == 'email') || (key == 'windows')) {
                        const late_key = key.concat("_late") as keyof Employee;
                        if (late_key in employees[idx]) {
                            (employees[idx] as any)[late_key] = data.late;
                        }
                    }
                }

                if (onEmployeeUpdate && (key === 'last_day' || key === 'date_hr_emailed')) {
                    onEmployeeUpdate()
                }
            }

        } catch (error) {
            console.error('Error updating field:', error);
            const msg = error instanceof Error ? error.message : 'Unknown error';
            toast.error(`Failed to update field: ${msg}`);
        } finally {
            editingEmployeeId = null;
            editingValue = '';
        }
    }

    function isNoAccountDate(dateString: string | null | undefined) {
        if (!dateString) return false;
        const date = new Date(dateString);
        return date.getFullYear() === 1900 && date.getMonth() === 0 && date.getDate() === 1;
    }

    function cancelEdit() {
        editingEmployeeId = null;
        editingValue = '';
    }

    async function saveRemarks(employee: Employee) {
        if (!editingEmployeeId) return;
        
        try {
            const trimmedRemarks = editingValue.trim();

            const res = await fetch(`${BASE_URL}/resignees/${employee.employee_no}/remarks`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'text/plain',
                },
                body: trimmedRemarks,
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

    function handleKeydown(event: KeyboardEvent) {
        if (event.key === 'Escape') {
            cancelEdit();
        }
    }

    function isEmployeeComplete(employee: Employee): boolean {
        const requiredFields = [employee.um, employee.third_party, employee.email, employee.windows];
        return requiredFields.every(field => field && field.trim() !== '');
    }

    function toggleStatus(employee: Employee) {
        const currentStatus = employee.processed_date_time ? 'processed' : 'unprocessed';
        const action = currentStatus === 'processed' ? 'unprocess' : 'process';
        
        if (onstatustoggle) {
            onstatustoggle({ detail: { employee, action } });
        }
         setTimeout(() => {
            if (action === 'process') {
                toast.success('Employee no. ' + employee.employee_no + ' marked as processed');
            } else {
                toast.success('Employee no. ' + employee.employee_no + ' marked as unprocessed');
            }
        }, 300);
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
<div class="outer-wrapper">
    <div class="table-wrapper rounded-md">
            <table class="min-w-full text-xs text-left text-gray-700 bg-white">
                    <thead class="bg-gray-100 text-xs text-gray-500 uppercase sticky top-0 z-20">
                        <tr>
                            <!---------- Employee no. ---------->
                            <th class="px-6 py-3 text-left text-[11px] font-bold text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors sticky left-0 top-0 bg-gray-100 z-30"
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
                                class="pl-6 py-3 text-left text-[11px] font-bold text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors"
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
                            <th class="pl-6 py-3 text-left text-[11px] font-bold text-gray-500 uppercase tracking-wider">
                                Cost center
                            </th>

                            <!---------- Name ---------->
                            <th 
                                class="pl-6 py-3 text-left text-[11px] font-bold text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors"
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
                            <th class="pl-6 py-3 text-left text-[11px] font-bold text-gray-500 uppercase tracking-wider">
                                Position title
                            </th>

                            <!---------- Rank ---------->
                            <th class="pl-6 py-3 text-left text-[11px] font-bold text-gray-500 uppercase tracking-wider">
                                Rank
                            </th>

                            <!---------- Department ---------->
                            <th 
                                class="pl-6 py-3 text-left text-[11px] font-bold text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors"
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
                                class="pl-6 py-3 text-left text-[11px] font-bold text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors"
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

                            <!---------- HR Email ---------->
                            <th 
                                class="pl-6 py-3 text-left text-[11px] font-bold text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors"
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

                            <!---------- Batch Deactivation ---------->
                            <th 
                                class="pl-6 py-3 text-left text-[11px] font-bold text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors"
                                on:click={() => handleSort('last_day')}
                            >
                            <div class="flex items-center gap-1">
                                Batch Deactivation
                                <svg class="w-4 h-4 shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                    {#if sortField === 'um' && sortDirection === 'asc'}
                                    <path fill-rule="evenodd" d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" />
                                    {:else if sortField === 'um' && sortDirection === 'desc'}
                                    <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" />
                                    {:else}
                                    <path fill-rule="evenodd" d="M10 3a1 1 0 01.707.293l3 3a1 1 0 01-1.414 1.414L10 5.414 7.707 7.707a1 1 0 01-1.414-1.414l3-3A1 1 0 0110 3zm-3.707 9.293a1 1 0 011.414 0L10 14.586l2.293-2.293a1 1 0 011.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" />
                                    {/if}
                                </svg>
                            </div>
                            </th>

                            <!---------- 3rd Party Systems ---------->
                            <th 
                                class="pl-6 py-3 text-left text-[11px] font-bold text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors"
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
                                class="pl-6 py-3 text-left text-[11px] font-bold text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors"
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
                                class="pl-6 py-3 text-left text-[11px] font-bold text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors"
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

                            <!---------- Status ---------->
                            <th class="pl-6 py-3 text-left text-[11px] font-bold text-gray-500 uppercase tracking-wider">
                                Status
                            </th>

                            <!---------- Remarks ---------->
                            <th class="px-6 py-3 text-left text-[11px] font-bold text-gray-500 uppercase tracking-wider w-80 max-w-80">
                                Remarks
                            </th>
                            
                        </tr>
                    </thead>

                    <tbody class="bg-white divide-y divide-gray-200">
                        {#each sortedEmployees as employee, index (employee.employee_no)}
                            <tr class="hover:bg-gray-50 transition-colors">
                            <td class="px-3 py-2 whitespace-normal text-xs font-medium text-gray-900 sticky left-0 bg-white">
                                {String(employee.employee_no || '')}
                            </td>
                            <td class="pl-3 py-2 whitespace-nowrap text-xs text-gray-900">
                                {formatDate(employee.date_hired)}
                            </td>
                            <td class="pl-3 py-2 whitespace-normal text-xs text-gray-900">
                                {String(employee.cost_center || '')}
                            </td>
                            <td class="pl-3 py-2 whitespace-normal text-xs font-medium text-gray-900">
                                {String(employee.name || '')}
                            </td>
                            <td class="pl-3 py-2 whitespace-normal text-xs text-gray-900">
                                {String(employee.position_title || '')}
                            </td>
                            <td class="pl-3 py-2 whitespace-normal text-xs text-gray-900">
                                {String(employee.rank || '')}
                            </td>
                            <td class="pl-3 py-2 whitespace-normal text-xs text-gray-900">
                                {String(employee.department || '')}
                            </td>

                            <!-- Editable Last Day Cell -->
                            <td class="pl-3 py-2 whitespace-nowrap text-xs text-gray-900">
                                <div class="flex items-center gap-2">
                                    {#if editingEmployeeId?.id === employee.employee_no && editingEmployeeId?.key === 'last_day'}
                                        <!-- Edit Mode: Date Input + Check Icon -->
                                        <input
                                            type="date"
                                            bind:value={editingValue}
                                            class="text-xs border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
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

                            <!-- Editable HR Email Cell -->
                            <td class="pl-3 py-2 whitespace-nowrap text-xs text-gray-900">
                                <div class="flex items-center gap-2">
                                    {#if editingEmployeeId?.id === employee.employee_no && editingEmployeeId?.key === 'date_hr_emailed'}
                                        <!-- Edit Mode: Date Input + Check Icon -->
                                        <input
                                            type="date"
                                            bind:value={editingValue}
                                            class="text-xs border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
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
                                            {formatDate(employee.date_hr_emailed)}
                                        </span>

                                        <button
                                            type="button"
                                            on:click={() => startEditing(employee, 'date_hr_emailed')}
                                            class="text-gray-400 hover:text-gray-600 transition-colors"
                                            title="Edit date for HR email"
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
                            <td class="pl-3 py-2 whitespace-nowrap text-xs text-gray-900">
                                <div class="flex items-center gap-2">
                                    {#if editingEmployeeId?.id === employee.employee_no && editingEmployeeId?.key === 'um'}
                                        <!-- Edit Mode: Date Input + No Account Button + Check Icon -->
                                        <div class="flex flex-col gap-2">
                                            <div class="flex items-center gap-2">
                                                <input
                                                    type="date"
                                                    bind:value={editingValue}
                                                    class="text-xs border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
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
                                            </div>
                                            <!-- No Existing Account Button -->
                                            <button
                                                type="button"
                                                on:click={() => {
                                                    editingValue = 'NO_ACCOUNT';
                                                    saveEdit(employee);
                                                }}
                                                class="text-xs border border-gray-300 hover:bg-gray-300 text-gray-700 w-21.5 rounded px-2 py-1 transition-colors"
                                                title="Mark as no existing account"
                                            >
                                                No account
                                            </button>
                                        </div>
                                    {:else}
                                        <!-- Display Mode: Date + Pencil Icon -->

                                        {#if employee.um_late}
                                            <span class="inline-flex w-5 h-5 text-xs font-medium rounded-full bg-red-600 text-white items-center justify-center"> L </span>
                                        {/if}

                                        <span class="inline-flex px-2 py-1 text-xs font-medium rounded-full {isNoAccountDate(employee.um) ? 'bg-[#FFF3CD] text-[#856404]' : employee.um ? 'bg-[#CFEED8] text-[#1E9F37]' : 'bg-[#FED9DA] text-[#D7313E]'}">
                                            {isNoAccountDate(employee.um) ? 'No account' : employee.um ? formatDate(employee.um) : 'N/A'}
                                        </span>
                                        <button
                                            type="button"
                                            on:click={() => startEditing(employee, 'um')}
                                            class="text-gray-400 hover:text-gray-600 transition-colors"
                                            title="Edit batch deactivation date"
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
                            <td class="pl-3 py-2 whitespace-nowrap text-xs text-gray-900">
                                <div class="flex items-center gap-2">
                                    {#if editingEmployeeId?.id === employee.employee_no && editingEmployeeId?.key === 'third_party'}
                                        <!-- Edit Mode: Date Input + No Account Button + Check Icon -->
                                        <div class="flex flex-col gap-2">
                                            <div class="flex items-center gap-2">
                                                <input
                                                    type="date"
                                                    bind:value={editingValue}
                                                    class="text-xs border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
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
                                            </div>
                                            <!-- No Existing Account Button -->
                                            <button
                                                type="button"
                                                on:click={() => {
                                                    editingValue = 'NO_ACCOUNT';
                                                    saveEdit(employee);
                                                }}
                                                class="text-xs border border-gray-300 hover:bg-gray-300 text-gray-700 w-21.5 rounded px-2 py-1 transition-colors"
                                                title="Mark as no existing account"
                                            >
                                                No account
                                            </button>
                                        </div>
                                    {:else}
                                        <!-- Display Mode: Date + Pencil Icon -->

                                        {#if employee.third_party_late}
                                            <span class="inline-flex w-5 h-5 text-xs font-medium rounded-full bg-red-600 text-white items-center justify-center"> L </span>
                                        {/if}

                                        <span class="inline-flex px-2 py-1 text-xs font-medium rounded-full {isNoAccountDate(employee.third_party) ? 'bg-[#FFF3CD] text-[#856404]' : employee.third_party ? 'bg-[#CFEED8] text-[#1E9F37]' : 'bg-[#FED9DA] text-[#D7313E]'}">
                                            {isNoAccountDate(employee.third_party) ? 'No account' : employee.third_party ? formatDate(employee.third_party) : 'N/A'}
                                        </span>
                                        <button
                                            type="button"
                                            on:click={() => startEditing(employee, 'third_party')}
                                            class="text-gray-400 hover:text-gray-600 transition-colors"
                                            title="Edit batch deactivation date"
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
                            <td class="pl-3 py-2 whitespace-nowrap text-xs text-gray-900">
                                <div class="flex items-center gap-2">
                                    {#if editingEmployeeId?.id === employee.employee_no && editingEmployeeId?.key === 'email'}
                                        <!-- Edit Mode: Date Input + No Account Button + Check Icon -->
                                        <div class="flex flex-col gap-2">
                                            <div class="flex items-center gap-2">
                                                <input
                                                    type="date"
                                                    bind:value={editingValue}
                                                    class="text-xs border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
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
                                            </div>
                                            <!-- No Existing Account Button -->
                                            <button
                                                type="button"
                                                on:click={() => {
                                                    editingValue = 'NO_ACCOUNT';
                                                    saveEdit(employee);
                                                }}
                                                class="text-xs border border-gray-300 hover:bg-gray-300 text-gray-700 w-21.5 rounded px-2 py-1 transition-colors"
                                                title="Mark as no existing account"
                                            >
                                                No account
                                            </button>
                                        </div>
                                    {:else}
                                        <!-- Display Mode: Date + Pencil Icon -->

                                        {#if employee.email_late}
                                            <span class="inline-flex w-5 h-5 text-xs font-medium rounded-full bg-red-600 text-white items-center justify-center"> L </span>
                                        {/if}

                                        <span class="inline-flex px-2 py-1 text-xs font-medium rounded-full {isNoAccountDate(employee.email) ? 'bg-[#FFF3CD] text-[#856404]' : employee.email ? 'bg-[#CFEED8] text-[#1E9F37]' : 'bg-[#FED9DA] text-[#D7313E]'}">
                                            {isNoAccountDate(employee.email) ? 'No account' : employee.email ? formatDate(employee.email) : 'N/A'}
                                        </span>
                                        <button
                                            type="button"
                                            on:click={() => startEditing(employee, 'email')}
                                            class="text-gray-400 hover:text-gray-600 transition-colors"
                                            title="Edit batch deactivation date"
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
                            <td class="pl-3 py-2 whitespace-nowrap text-xs text-gray-900">
                                <div class="flex items-center gap-2">
                                    {#if editingEmployeeId?.id === employee.employee_no && editingEmployeeId?.key === 'windows'}
                                        <!-- Edit Mode: Date Input + No Account Button + Check Icon -->
                                        <div class="flex flex-col gap-2">
                                            <div class="flex items-center gap-2">
                                                <input
                                                    type="date"
                                                    bind:value={editingValue}
                                                    class="text-xs border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
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
                                            </div>
                                            <!-- No Existing Account Button -->
                                            <button
                                                type="button"
                                                on:click={() => {
                                                    editingValue = 'NO_ACCOUNT';
                                                    saveEdit(employee);
                                                }}
                                                class="text-xs border border-gray-300 hover:bg-gray-300 text-gray-700 w-21.5 rounded px-2 py-1 transition-colors"
                                                title="Mark as no existing account"
                                            >
                                                No account
                                            </button>
                                        </div>
                                    {:else}
                                        <!-- Display Mode: Date + Pencil Icon -->

                                        {#if employee.windows_late}
                                            <span class="inline-flex w-5 h-5 text-xs font-medium rounded-full bg-red-600 text-white items-center justify-center"> L </span>
                                        {/if}

                                        <span class="inline-flex px-2 py-1 text-xs font-medium rounded-full {isNoAccountDate(employee.windows) ? 'bg-[#FFF3CD] text-[#856404]' : employee.windows ? 'bg-[#CFEED8] text-[#1E9F37]' : 'bg-[#FED9DA] text-[#D7313E]'}">
                                            {isNoAccountDate(employee.windows) ? 'No account' : employee.windows ? formatDate(employee.windows) : 'N/A'}
                                        </span>
                                        <button
                                            type="button"
                                            on:click={() => startEditing(employee, 'windows')}
                                            class="text-gray-400 hover:text-gray-600 transition-colors"
                                            title="Edit batch deactivation date"
                                        >
                                            <!-- Pencil/Edit Icon -->
                                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                                            </svg>
                                        </button>
                                    {/if}
                                </div>
                            </td>

                            <!-- Toggle Checkbox -->
                            <td class="pl-5 py-4 whitespace-nowrap text-xs text-gray-500 text-center align-middle z-10">
                                {#if isEmployeeComplete(employee)}
                                    <!-- Normal checkbox when all details are complete -->
                                    <input
                                        type="checkbox"
                                        class="w-5 h-5 text-green-600 rounded border-gray-300 focus:ring-green-500 cursor-pointer align-middle"
                                        checked={employee.processed_date_time !== null}
                                        on:change={() => toggleStatus(employee)}
                                    />
                                {:else}
                                    <!-- Disabled gray checkbox when details are incomplete -->
                                    <div 
                                        class="w-4 h-4 bg-gray-400 border-2 border-gray-400 rounded cursor-not-allowed align-middle inline-block"
                                        title="Incomplete details"
                                    >
                                    </div>
                                {/if}
                            </td>

                            <!-- Remarks Field -->
                            <td class="px-3 py-2 text-xs text-gray-900 w-80 max-w-80">
                                <div class="flex items-start gap-2">
                                    {#if editingEmployeeId?.id === employee.employee_no && editingEmployeeId?.key === 'remarks'}
                                        <!-- Edit Mode: Text Field + Check Icon -->
                                        <textarea
                                            bind:value={editingValue}
                                            rows="3"
                                            class="text-xs border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 h-20 w-28"
                                        ></textarea>
                                        <button
                                            type="button"
                                            on:click={() => saveRemarks(employee)}
                                            class="text-green-600 hover:text-green-800 transition-colors flex-shrink-0 mt-1"
                                            title="Save changes"
                                        >
                                            <!-- Check Icon -->
                                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                                            </svg>
                                        </button>
                                    {:else}
                                        <!-- Display Mode: Text + Pencil Icon -->
                                        <span class="flex-1 text-xs break-all hyphens-auto w-28 max-w-28">
                                            {String(employee.remarks || 'N/A')}
                                        </span>

                                        <button
                                            type="button"
                                            on:click={() => startEditingRemarks(employee)}
                                            class="text-gray-400 hover:text-gray-600 transition-colors flex-shrink-0 mt-1"
                                            title="Edit remarks"
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
                    <h3 class="mt-2 text-xs font-medium text-gray-900">No employees found</h3>
                    </div>
                {/if}
        </div>
    
    <!-- Always Visible Sticky Scrollbar at Bottom -->
    <div class="sticky-scrollbar-container bg-gray-50 border-t border-gray-300 h-5 z-10" bind:this={stickyScrollbar}>
        <div class="h-5"></div>
    </div>
</div>

<style>
    .table-wrapper {
        overflow-y: scroll;
        overflow-x: scroll;
        height: fit-content;
        max-height: 66.4vh;
        padding-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border-radius: 0.5rem;
    }

    table {
        border-collapse: separate;
        border-spacing: 0px;
        border-radius: 0.5rem;
    }
</style>
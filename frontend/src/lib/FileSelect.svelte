<script lang="ts">
	import { goto } from '$app/navigation';
	import { BASE_URL } from '../constants';

	let selectedPath = '';
	let isLoading = false;
	let errorMessage = '';
	let successMessage = '';

	const selectDatabase = async () => {
		try {
			const path = await (window as any).pywebview.api.select_file();
			if (!path) {
				errorMessage = 'No file selected.';
				return;
			}
			if (!path.endsWith('.db')) {
				errorMessage = 'Please select a valid .db file.';
				return;
			}
			selectedPath = path;
			errorMessage = '';
			successMessage = '';
		} catch (error) {
			errorMessage = 'File dialog failed. ' + error;
		}
	};

	const handleSubmit = async () => {
		if (!selectedPath) {
			errorMessage = 'Please select a .db file first.';
			return;
		}

		isLoading = true;
		errorMessage = '';
		successMessage = '';

		try {
			const response = await fetch(`${BASE_URL}/db-path`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ path: selectedPath }),
				credentials: 'include'
			});

			if (response.ok) {
				successMessage = 'Database path accepted!';
				setTimeout(() => goto('/login'), 1000);
			} else {
				const errorData = await response.text();
				errorMessage = `Failed (${response.status}). ${errorData}`;
			}
		} catch (error) {
			errorMessage = `Network error: ${error instanceof Error ? error.message : 'Unknown error'}`;
		} finally {
			isLoading = false;
		}
	};
</script>

<svelte:head>
	<title>Select Database File</title>
</svelte:head>

<div class="min-h-screen flex items-center justify-center bg-gray-100 px-4 py-8">
	<div class="w-full max-w-md">
		<div class="bg-white rounded-lg shadow-md p-6">
			<h1 class="text-2xl font-bold text-gray-900 mb-6 text-center">
				Select Database File
			</h1>
			
			<div class="space-y-4">

				<!-- File selection button -->
				<button
					on:click={selectDatabase}
					class="w-full py-2 px-4 bg-gray-500 hover:bg-gray-600 text-white rounded-md"
				>
					Select .db File
				</button>

				{#if selectedPath}
					<div class="p-3 bg-green-50 border border-green-200 rounded-lg">
						<p class="text-sm text-green-800">
							<strong>Selected path:</strong> {selectedPath}
						</p>
					</div>
				{/if}

				{#if errorMessage}
					<div class="p-3 bg-red-50 border border-red-200 rounded-lg">
						<p class="text-sm text-red-800">
							{errorMessage}
						</p>
					</div>
				{/if}

				{#if successMessage}
					<div class="p-3 bg-green-50 border border-green-200 rounded-lg">
						<p class="text-sm text-green-800">
							{successMessage}
						</p>
					</div>
				{/if}

				<button
					on:click={handleSubmit}
					disabled={!selectedPath || isLoading}
					class="w-full py-2 px-4 bg-blue-500 hover:bg-blue-600 text-white font-medium rounded-lg"
				>
					{isLoading ? 'Submitting...' : 'Submit Path'}
				</button>

			</div>
		</div>
	</div>
</div>

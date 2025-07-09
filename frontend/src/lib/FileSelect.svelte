<script lang="ts">
	import { goto } from '$app/navigation';

	let selectedFile: File | null = null;
	let isLoading = false;
	let errorMessage = '';
	let successMessage = '';

	const handleFileSelect = (event: Event) => {
		const target = event.target as HTMLInputElement;
		const file = target.files?.[0] || null;
		
		selectedFile = file;
		errorMessage = '';
		successMessage = '';
		
		if (file && !file.name.endsWith('.db')) {
			errorMessage = 'Please select a valid .db file.';
			selectedFile = null;
			target.value = '';
		}
	};

	const handleSubmit = async () => {
		if (!selectedFile) {
			errorMessage = 'Please select a .db file first.';
			return;
		}

		isLoading = true;
		errorMessage = '';
		successMessage = '';

		try {
			const formData = new FormData();
			formData.append("file", selectedFile);

			const response = await fetch('https://localhost:8000/db-route', {
				method: 'POST',
				body: formData,
				credentials: 'include'
			});

			if (response.ok) {
				successMessage = 'Database file uploaded successfully!';
				setTimeout(() => {
					goto('/login');
				}, 1000);
			} else {
				const errorData = await response.text();
				errorMessage = `Upload failed (${response.status}). ${errorData}`;
			}
		} catch (error) {
			if (error instanceof Error) {
				errorMessage = `Network error: ${error.message}. Please try again.`;
			} else {
				errorMessage = 'Network error: An unknown error occurred. Please try again.';
			}
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
				<div>
					<label for="file-input" class="block text-sm font-medium text-gray-700 mb-2">
						Choose Database File (.db)
					</label>
					<input
						id="file-input"
						type="file"
						accept=".db"
						on:change={handleFileSelect}
						disabled={isLoading}
						class="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg shadow-sm file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 transition-colors disabled:opacity-50"
					/>
				</div>

				{#if selectedFile}
					<div class="p-3 bg-green-50 border border-green-200 rounded-lg">
						<p class="text-sm text-green-800">
							<strong>Selected file:</strong> {selectedFile.name}
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
					disabled={!selectedFile || isLoading}
					class="w-full py-2 px-4 bg-blue-500 hover:bg-blue-600 disabled:bg-blue-300 text-white font-medium rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
				>
					{isLoading ? 'Uploading...' : 'Upload Database'}
				</button>
			</div>
		</div>
	</div>
</div> 
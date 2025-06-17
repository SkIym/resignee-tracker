<script>
	import { goto } from '$app/navigation';
    import { BASE_URL } from '../../constants';
	let username = '';
	let password = '';
	let confirmPassword = '';
	let isLoading = false;
	let errorMessage = '';

	const handleSubmit = async (e) => {
		e.preventDefault();
		isLoading = true;
		errorMessage = '';

		// Basic validation
		if (password !== confirmPassword) {
			errorMessage = 'Passwords do not match';
			isLoading = false;
			return;
		}

		try {
			const formData = new URLSearchParams();
			formData.append('username', username);
			formData.append('password', password);

			const response = await fetch(`${BASE_URL}/accounts`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/x-www-form-urlencoded',
				},
				body: formData,
				credentials: 'include'
			});

			if (response.ok) {
				// Redirect to login page after successful signup
				goto('/');
			} else {
				const errorData = await response.text();
				errorMessage = `Sign up failed (${response.status}). ${errorData || 'Please try again.'}`;
			}
		} catch (error) {
			errorMessage = `Network error: ${error.message}. Please try again.`;
		} finally {
			isLoading = false;
		}
	};

	const handleLogin = () => {
		goto('/');
	};
</script>

<svelte:head>
	<title>Sign Up</title>
</svelte:head>

<div class="min-h-screen flex items-center justify-center bg-gray-100 px-4 py-8">
	<div class="w-full max-w-sm">
		<form on:submit={handleSubmit} class="space-y-4">
			<div>
				<label for="username" class="block text-sm font-medium text-gray-700 mb-1">
					Username
				</label>
				<input
					id="username"
					name="username"
					type="text"
					bind:value={username}
					required
					disabled={isLoading}
					class="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 transition-colors disabled:opacity-50"
				/>
			</div>

			<div>
				<label for="password" class="block text-sm font-medium text-gray-700 mb-1">
					Password
				</label>
				<input
					id="password"
					name="password"
					type="password"
					bind:value={password}
					required
					disabled={isLoading}
					class="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 transition-colors disabled:opacity-50"
				/>
			</div>

			<div>
				<label for="confirmPassword" class="block text-sm font-medium text-gray-700 mb-1">
					Confirm Password
				</label>
				<input
					id="confirmPassword"
					name="confirmPassword"
					type="password"
					bind:value={confirmPassword}
					required
					disabled={isLoading}
					class="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 transition-colors disabled:opacity-50"
				/>
			</div>

			{#if errorMessage}
				<div class="text-red-600 text-sm text-center">
					{errorMessage}
				</div>
			{/if}

			<button
				type="submit"
				disabled={isLoading}
				class="mt-6 w-full py-2 px-4 bg-blue-500 hover:bg-blue-600 disabled:bg-blue-300 text-white font-medium rounded-lg shadow-sm"
			>
				{isLoading ? 'Signing up...' : 'Sign Up'}
			</button>
		</form>

		<div class="mt-5 text-center">
			<p class="text-left text-sm text-gray-600 mb-1">Already have an account?</p>
			<button
				on:click={handleLogin}
				type="button"
				disabled={isLoading}
				class="border-3 border-blue-500 w-full py-2 px-4 hover:bg-gray-300 disabled:opacity-50 text-blue-500 font-medium rounded-lg shadow-sm"
			>
				Login
			</button>
		</div>
	</div>
</div>
<script lang="ts">
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
    import { BASE_URL } from '../../constants';

	let username = '';
	let password = '';
	let isLoading = false;
	let errorMessage = '';

	onMount(async () => {
		try {
			const res = await fetch(`${BASE_URL}/check-auth`, {
				method: 'GET',
				credentials: 'include'
			});

			if (res.ok) {
				console.log("Already logged in. Redirecting to dashboard...");
				goto('/dashboard');
			}
		} catch (err) {
			console.warn("Auth check failed. Please Login.");
		}
	});


	const handleSubmit = async (e: any) => {
		e.preventDefault();
		isLoading = true;
		errorMessage = '';

		try {
			const formData = new URLSearchParams();
			formData.append('username', username);
			formData.append('password', password);

			const response = await fetch(`${BASE_URL}/login`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/x-www-form-urlencoded',
				},
				body: formData,
				credentials: 'include'
			});

			if (response.ok) {
				goto('/dashboard');
			} else {
				const errorData = await response.json();
				errorMessage = errorData.detail || `Login failed (${response.status})`;
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

	const handleSignUp = () => {
		goto('/signup');
	};
</script>

<svelte:head>
	<title>Login</title>
</svelte:head>

<div class="min-h-screen flex items-start justify-center bg-gray-100 px-4 pt-20">
	<div class="w-full max-w-sm">
		<div class="text-center">
			<!-- Replace `src="/logo.png"` with your actual logo path -->
			<img src="/assets/proj-1-logo.png"  alt="AUB Logo" class="mx-auto h-40 w-auto mb-4" />
			<h1 class="text-2xl font-bold text-gray-800"> AUB Resignee Tracker </h1>
		</div>

		<!-- Login form -->
		<form on:submit={handleSubmit} class="space-y-4 pt-4">
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
					class="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg placeholder-gray-400 transition-colors disabled:opacity-50 
						focus:outline-none focus:ring-1 focus:ring-red-500 focus:border-red-500"
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
					class="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg placeholder-gray-400 transition-colors disabled:opacity-50 
						focus:outline-none focus:ring-1 focus:ring-red-500 focus:border-red-500"
				/>
			</div>

			{#if errorMessage}
				<div class="text-black text-sm text-center">
					{errorMessage}
				</div>
			{/if}

			<button
				type="submit"
				disabled={isLoading}
				class="mt-6 w-full py-2 px-4 bg-red-500 hover:bg-red-600 disabled:bg-red-300 text-white font-medium rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition-colors"
			>
				{isLoading ? 'Logging in...' : 'Login'}
			</button>
		</form>
<!-- 
		<div class="mt-5 text-center">
			<p class="text-left text-sm text-gray-600 mb-1">Don't have an account yet?</p>
			<button
				on:click={handleSignUp}
				type="button"
				disabled={isLoading}
				class="border-3 border-red-500 w-full py-2 px-4 hover:bg-gray-300 disabled:opacity-50 text-red-500 font-medium rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-gray-400 focus:ring-offset-2 transition-colors"
			>
				Sign Up
			</button>
		</div> -->
	</div>
</div>
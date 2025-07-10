<<<<<<< HEAD
<script>
	import FileSelect from '$lib/FileSelect.svelte';
=======
<script lang="ts">
	import { goto } from '$app/navigation';
    import { BASE_URL } from '../constants';
	import { onMount } from 'svelte';

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
>>>>>>> exe-sqlite
</script>

<svelte:head>
	<title>Select Database File</title>
</svelte:head>

<FileSelect />
<script lang="ts">
  import { goto } from '$app/navigation'; // use 'import { push } from "svelte-spa-router"' if not using SvelteKit

  function handleLogout() {
    // Optional: clear auth/token/localStorage if you're using them
    localStorage.removeItem('user');
    sessionStorage.clear();

    // Redirect to login
    goto('/'); // or use `push('/')` for svelte-spa-router
  }
</script>

<button
  on:click={handleLogout}
  class="px-4.25 py-1.75 bg-red-500 text-white rounded-md hover:bg-red-600 transition"
>
  Logout
</button>


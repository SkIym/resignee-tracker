<script lang="ts">
  import { goto } from '$app/navigation'; 

  async function handleLogout() {   
    await fetch('http://localhost:8000/logout', {
        method: 'POST',
        credentials: 'include'
    });

  goto('/');
}

</script>

<button
  on:click={handleLogout}
  class="px-4.25 py-1.75 bg-red-500 text-white rounded-md hover:bg-red-600 transition"
>
  Logout
</button>


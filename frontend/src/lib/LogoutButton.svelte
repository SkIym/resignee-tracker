<script lang="ts">
  import { goto } from '$app/navigation'; 
  import { BASE_URL } from '../constants';

   async function handleLogout() {   
    try {
      const res = await fetch(`${BASE_URL}/logout`, {
        method: 'POST',
        credentials: 'include', 
      });

      if (!res.ok) {
        const text = await res.text();
        console.error('Logout failed:', text);
        return;
      }

      goto('/');
    } catch (err) {
      console.error('Logout error:', err);
    }
  }
</script>
  <button
    on:click={handleLogout}
    class="flex items-center gap-2 px-3 py-1.75 bg-red-500 text-white rounded-md hover:bg-red-600 transition"
  >
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
      <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0 0 13.5 3h-6a2.25 2.25 0 0 0-2.25 2.25v13.5A2.25 2.25 0 0 0 7.5 21h6a2.25 2.25 0 0 0 2.25-2.25V15m3 0 3-3m0 0-3-3m3 3H9" />
    </svg>
    Logout
  </button>

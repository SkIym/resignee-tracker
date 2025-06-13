<script>
  let username = '';
  let password = '';
  
  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Username:', username);
    console.log('Password:', password);
    // Add your login logic here
  };
</script>

<svelte:head>
  <title>Login</title>
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
            class="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 transition-colors"
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
            class="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 transition-colors"
          />
        </div>
        
        <button
          type="submit"
          class="mt-6 w-full py-2 px-4 bg-blue-500 hover:bg-blue-600 text-white font-medium rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
        >
          Login
        </button>
      </form>
  </div>
</div>
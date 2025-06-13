<script>
  import { supabase } from "$lib/supabaseClient";
  import { Toaster, toast } from 'svelte-sonner';

  let username = ''
  let password = ''
  let errorMessage = ''

  async function authenticateSupabase() {
  try {
    const { data, error } = await supabase.auth.signInWithPassword({
      email: username,
      password: password
    });

    if (error) throw error;

    toast.success("Login successful!");


    await supabase.auth.refreshSession();
    console.log("Session after login:", await supabase.auth.getSession());
    // Redirect after confirming session
    setTimeout(() => {
      window.location.href = "/dashboard";
    }, 200);

  } catch (error) {
    toast.error("Invalid credentials");
  }
}
</script>

<section class={"min-h-screen flex flex-col px-4"}>
  <div class="flex flex-col flex-1 max-w-[1400px] mx-auto w-full">
    <slot />
  </div>
</section>

  <Toaster />
    <header class="flex flex-col relative z-20">
        <div
          class="max-w-[1400px] mx-auto w-full flex items-center justify-between p-4 py-10"
        >
            <div class = "max-h-1 flex">
                <img class = "size-6" src = "https://dcs.upd.edu.ph/staticfiles/media/dcs_logo.png" alt="DCS LOGO">
                <a href="/">
                    <h1 class="font-bold text-left px-2">
                      
                      DCS <span 
                      class="text-green-400">Iskedyul</span>
                    </h1>
                </a>
            </div>
        </div>
      </header>
      <div class = "flex h-screen justify-center items-center flex-col space-y-2 flex-1 mx-60">
        <div class = "flex flex-col w-2/6">
            <label for="username" class="italic block mb-2 text-sm font-medium text-gray-900 text-left">Username</label>
            <input 
            bind:value={username}
            
            type="text" id="username" class="bg-gray-100 border border-gray-300 text-slate-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5" required />
            <label for="password" class="italic block mb-2 text-sm font-medium text-gray-900 text-left mt-3">Password</label>
            <input 
            bind:value={password}
            type="password" id="password" class="bg-gray-100 border border-gray-300 text-slate-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5" required />
            
              <button onclick={authenticateSupabase}
              type="submit" class="mt-4 text-white bg-green-700 hover:bg-green-900 focus:ring-4 focus:outline-none focus:ring-green-100 font-medium rounded-lg text-sm w-full px-5 py-2.5 text-center">Login</button>
            
        </div>
      </div>
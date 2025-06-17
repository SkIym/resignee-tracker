import { u as head, v as attr, t as escape_html, n as pop, p as push } from "../../../chunks/index.js";
import "../../../chunks/client.js";
function _page($$payload, $$props) {
  push();
  let username = "";
  let password = "";
  let confirmPassword = "";
  let isLoading = false;
  head($$payload, ($$payload2) => {
    $$payload2.title = `<title>Sign Up</title>`;
  });
  $$payload.out += `<div class="min-h-screen flex items-center justify-center bg-gray-100 px-4 py-8"><div class="w-full max-w-sm"><form class="space-y-4"><div><label for="username" class="block text-sm font-medium text-gray-700 mb-1">Username</label> <input id="username" name="username" type="text"${attr("value", username)} required${attr("disabled", isLoading, true)} class="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 transition-colors disabled:opacity-50"/></div> <div><label for="password" class="block text-sm font-medium text-gray-700 mb-1">Password</label> <input id="password" name="password" type="password"${attr("value", password)} required${attr("disabled", isLoading, true)} class="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 transition-colors disabled:opacity-50"/></div> <div><label for="confirmPassword" class="block text-sm font-medium text-gray-700 mb-1">Confirm Password</label> <input id="confirmPassword" name="confirmPassword" type="password"${attr("value", confirmPassword)} required${attr("disabled", isLoading, true)} class="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 transition-colors disabled:opacity-50"/></div> `;
  {
    $$payload.out += "<!--[!-->";
  }
  $$payload.out += `<!--]--> <button type="submit"${attr("disabled", isLoading, true)} class="mt-6 w-full py-2 px-4 bg-blue-500 hover:bg-blue-600 disabled:bg-blue-300 text-white font-medium rounded-lg shadow-sm">${escape_html("Sign Up")}</button></form> <div class="mt-5 text-center"><p class="text-left text-sm text-gray-600 mb-1">Already have an account?</p> <button type="button"${attr("disabled", isLoading, true)} class="border-3 border-blue-500 w-full py-2 px-4 hover:bg-gray-300 disabled:opacity-50 text-blue-500 font-medium rounded-lg shadow-sm">Login</button></div></div></div>`;
  pop();
}
export {
  _page as default
};

import { v as attr, n as pop, p as push, w as bind_props, x as fallback, y as attr_class, u as head, t as escape_html } from "../../../chunks/index.js";
import "../../../chunks/client.js";
import "clsx";
function SearchBar($$payload, $$props) {
  push();
  let searchTerm = "";
  $$payload.out += `<div class="relative flex-1 min-w-[200px] max-w-md"><div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"><svg class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-4.35-4.35M17 10a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg></div> <input${attr("value", searchTerm)} type="text" placeholder="Search" class="block w-full pl-10 pr-10 py-2.5 border border-gray-300 rounded-3xl"/> `;
  {
    $$payload.out += "<!--[!-->";
  }
  $$payload.out += `<!--]--></div>`;
  pop();
}
function FilterButton($$payload, $$props) {
  push();
  let employees = fallback($$props["employees"], () => [], true);
  $$payload.out += `<div class="dropdown svelte-1ndynix"><button class="filter-button svelte-1ndynix"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="svelte-1ndynix"><path stroke-linecap="round" stroke-linejoin="round" d="M12 3c2.755 0 5.455.232 8.083.678.533.09.917.556.917 1.096v1.044a2.25 2.25 0 0 1-.659 1.591l-5.432 5.432a2.25 2.25 0 0 0-.659 1.591v2.927a2.25 2.25 0 0 1-1.244 2.013L9.75 21v-6.568a2.25 2.25 0 0 0-.659-1.591L3.659 7.409A2.25 2.25 0 0 1 3 5.818V4.774c0-.54.384-1.006.917-1.096A48.32 48.32 0 0 1 12 3Z"></path></svg> Filter</button> `;
  {
    $$payload.out += "<!--[!-->";
  }
  $$payload.out += `<!--]--></div>`;
  bind_props($$props, { employees });
  pop();
}
function ExportCalendarButton($$payload, $$props) {
  push();
  let startDate = "";
  let endDate = "";
  $$payload.out += `<div class="flex items-center gap-2"><label for="start-date" class="text-sm text-gray-600 font-[Open_Sans]">From:</label> <input id="start-date" type="date"${attr("value", startDate)} class="border border-gray-300 px-3 py-1 rounded-full text-sm font-[Open_Sans] uppercase"/> <label for="end-date" class="text-sm text-gray-600 font-[Open_Sans]">To:</label> <input id="end-date" type="date"${attr("value", endDate)} class="border border-gray-300 px-3 py-1 rounded-full text-sm font-[Open_Sans] uppercase"/> <button${attr_class(`flex items-center gap-2 px-4.25 py-1.75 rounded-md text-sm font-[Open_Sans] hover:bg-blue-600 transition ${"bg-blue-500 text-white"}`)}><svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5m-13.5-9L12 3m0 0 4.5 4.5M12 3v13.5"></path></svg> Export</button></div>`;
  pop();
}
function LogoutButton($$payload, $$props) {
  push();
  $$payload.out += `<button class="flex items-center gap-2 px-3 py-1.75 bg-red-500 text-white rounded-md hover:bg-red-600 transition"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0 0 13.5 3h-6a2.25 2.25 0 0 0-2.25 2.25v13.5A2.25 2.25 0 0 0 7.5 21h6a2.25 2.25 0 0 0 2.25-2.25V15m3 0 3-3m0 0-3-3m3 3H9"></path></svg> Logout</button>`;
  pop();
}
function _page($$payload, $$props) {
  push();
  let employees = [];
  let statusFilter = "all";
  let message = "";
  {
    employees.filter((emp) => {
      emp.processed_date_time ? "processed" : "unprocessed";
      const matchesStatus = statusFilter === "all";
      return matchesStatus;
    });
  }
  head($$payload, ($$payload2) => {
    $$payload2.title = `<title>AUB Resignee Tracker</title>`;
  });
  $$payload.out += `<main class="min-h-screen bg-gray-50 p-6"><div class="max-w-7xl mx-auto"><div class="flex flex-wrap items-center justify-between gap-4 mb-6"><div class="flex items-center gap-4 flex-1">`;
  SearchBar($$payload);
  $$payload.out += `<!----></div> <div class="flex gap-2">`;
  FilterButton($$payload, { employees });
  $$payload.out += `<!----> `;
  ExportCalendarButton($$payload);
  $$payload.out += `<!----></div></div> <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">`;
  {
    $$payload.out += "<!--[-->";
    $$payload.out += `<div class="flex items-center justify-center py-12"><div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div> <span class="ml-3 text-gray-600">Loading employees...</span></div>`;
  }
  $$payload.out += `<!--]--></div> `;
  {
    $$payload.out += "<!--[!-->";
  }
  $$payload.out += `<!--]--></div> <form><div class="mt-4 max-w-7xl mx-auto mb-6"><textarea rows="5" class="block w-full p-4 text-gray-900 border border-gray-300 rounded-lg bg-white text-base resize-y" placeholder="Paste resignee details here...">`;
  const $$body = escape_html(message);
  if ($$body) {
    $$payload.out += `${$$body}`;
  }
  $$payload.out += `</textarea> <div class="mt-4 flex justify-between items-center"><button type="submit" class="px-4.25 py-1.5 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition">Submit</button> `;
  LogoutButton($$payload);
  $$payload.out += `<!----></div> `;
  {
    $$payload.out += "<!--[!-->";
  }
  $$payload.out += `<!--]--></div></form></main>`;
  pop();
}
export {
  _page as default
};

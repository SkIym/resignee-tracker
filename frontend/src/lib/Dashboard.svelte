<script>
  let count = $state(0)
  const increment = () => {
    count += 1
  }
</script>

<div>
  <!-- Search and Controls -->
		<div class="flex flex-wrap gap-3 mb-4">
			<div class="flex-1 min-w-[200px] relative">
				<input 
					type="text" 
					placeholder="Search" 
					class="w-full px-4 py-2 border border-gray-300 rounded-lg pl-10"
				>
				<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400 absolute left-3 top-2.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
				</svg>
			</div>
    </div>
</div>

<table>
    <thead class="new-thead z-10">
        <tr>
            <th class="course">Course</th>
            <th class="type">Type</th>
            <th class="section">Section</th>
            <th class="days">Day</th>
            <th class="time">Start Time</th>
            <th class="time">End Time</th>
            <th class="room">Room</th>
            <th class="size">Size</th>
            <th class="instructor">Instructor</th>
            <th class="load">Load</th>
			<th class="status">Status</th>
			<th>+/- Slots</th>
            <th>Delete</th>
			<th>Edit</th>
        </tr>
    </thead>
</table>

<style>
	:global(body) {
		/* background-color: #f9fafb; */
	}
	/* .to_focus{
		--tw-ring-color: rgba(16, 185, 129, var(--tw-ring-opacity));
		border-color: var(--color-green-500);
	} */
	.cont {
		display: inline;
		gap: 10px;
		background-color: red;
	}
	.title1 {
		text-align: left;
		font-size: 2rem;
		font-weight: 800;
	}
	.title2{
		text-align: left;
		font-size: 1.25rem;
		font-weight: 600;
	}
	.backdrop {
    width: 100%;
		height: 100%;
		position: fixed;
		background: rgba(0, 0, 0, 0.8);
		overflow-y: auto;
		z-index: 100;
	}
	.modal {
		/* text-align: center; */
		padding: 5rem;
		border-radius: 10px;
		max-width: 60rem;
		margin: 10% auto;
		background: white;
		/* justify-items: center; */
		justify-content: space-between;
		z-index: 150;
	}

	.delete-modal {
		/* text-align: center; */
		padding: 2rem;
		border-radius: 10px;
		max-width: 40rem;
		margin: 5% auto;
		background: white;
		/* justify-items: center; */
		justify-content: space-between;
		z-index: 150;
	}
	.form_total {
		display: flex;
		flex-wrap: wrap;
		justify-items: center;
		justify-content: space-between;
	}
	.center_col {
		display: flex;
		flex-direction: row;
		place-items: center;
		justify-content: space-between;
	}

  .form-row {
		padding-top: 10px;
		width: 100%;
	}
	.new-row {
		display: flex;
		flex-direction: row;
		gap: 50px;
		/* background-color: aqua; */
		flex-wrap:wrap;
	}

	input[type='checkbox'] {
		-webkit-appearance:none;
		width:15px;
		height:15px;
		background:white;
		border-radius:5px;
		border:2px solid #555;
	}
	input[type='checkbox']:checked {
		background:green;
	}
	.form-col {
		text-align: left;
		display: flex;
		flex-direction: column;
		padding-top: 10px;
    width: 100%;
		/* margin-left: 2.5rem; */
		margin-right: 2.5rem;
	}
	.submit-btn {
		margin-top: 1.5rem;
		background-color: green;
		color: white;
		padding-top: 0.625rem;
		padding-bottom: 0.625rem;
		padding-left: 1.5rem;
		padding-right: 1.5rem;
		border-radius: 0.625rem;
	}
</style>
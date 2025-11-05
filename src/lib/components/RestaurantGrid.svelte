<script lang="ts">
	import type { Table, BookingSlot } from '$lib/types';
	import { isTableAvailable } from '$lib/dataGenerator';
	import TableComponent from './TableComponent.svelte';

	interface Props {
		tables: Table[];
		bookings: BookingSlot[];
		systemType: 'coloured' | 'text';
		selectedTime: string | null;
		onTableSelect: (tableId: number) => void;
	}

	let { tables, bookings, systemType, selectedTime, onTableSelect }: Props = $props();

	// Layout: 3 rows x 4 columns as shown in the images
	const gridLayout = [
		[1, 6, 7, 8],
		[2, 3, 9, 10],
		[4, 5, 11, 12]
	];
</script>

<div class="restaurant-grid">
	{#each gridLayout as row}
		<div class="table-row">
			{#each row as tableId}
				{@const table = tables.find(t => t.id === tableId)}
				{#if table}
					<div class="table-cell">
						<TableComponent
							{table}
							available={selectedTime ? isTableAvailable(table.id, selectedTime, bookings) : false}
							{systemType}
							{selectedTime}
							onSelect={onTableSelect}
						/>
					</div>
				{/if}
			{/each}
		</div>
	{/each}
</div>

<style>
	.restaurant-grid {
		display: flex;
		flex-direction: column;
		gap: 50px;
		padding: 40px;
		background-color: #f3f4f6;
		border-radius: 12px;
		max-width: 700px;
		margin: 0 auto;
	}

	.table-row {
		display: flex;
		justify-content: space-around;
		gap: 50px;
	}

	.table-cell {
		display: flex;
		align-items: center;
		justify-content: center;
	}
</style>

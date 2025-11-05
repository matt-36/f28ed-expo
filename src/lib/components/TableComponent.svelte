<script lang="ts">
	import type { Table } from '$lib/types';

	interface Props {
		table: Table;
		available: boolean;
		systemType: 'coloured' | 'text';
		selectedTime: string | null;
		onSelect: (tableId: number) => void;
	}

	let { table, available, systemType, selectedTime, onSelect }: Props = $props();

	function handleClick() {
		if (selectedTime && available) {
			onSelect(table.id);
		}
	}

	let buttonClass = $derived(() => {
		if (!selectedTime) return 'table-btn disabled';
		if (systemType === 'coloured') {
			return `table-btn ${table.shape} ${available ? 'available' : 'booked'}`;
		}
		return `table-btn ${table.shape} text-mode ${available ? 'available' : 'booked'}`;
	});

	// Generate chair positions based on table capacity (not shape)
	const chairs = $derived(() => {
		if (table.capacity === 4) {
			// 4 chairs (top, right, bottom, left)
			return [
				{ position: 'top' },
				{ position: 'right' },
				{ position: 'bottom' },
				{ position: 'left' }
			];
		} else {
			// 6 chairs (2 on each long side, 1 on each short side)
			return [
				{ position: 'top' },
				{ position: 'right-top' },
				{ position: 'right-bottom' },
				{ position: 'bottom' },
				{ position: 'left-top' },
				{ position: 'left-bottom' }
			];
		}
	});
</script>

<div class="table-container">
	{#each chairs() as chair}
		<div class="chair {chair.position}" class:visible={selectedTime !== null}></div>
	{/each}
	
	<button
		class={buttonClass()}
		onclick={handleClick}
		disabled={!selectedTime || !available}
	>
		{#if selectedTime}
			{#if systemType === 'text'}
				<span class="status-text">{available ? 'Available' : 'Booked'}</span>
			{/if}
		{/if}
	</button>
</div>

<style>
	.table-container {
		position: relative;
		width: 120px;
		height: 120px;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.chair {
		position: absolute;
		width: 18px;
		height: 18px;
		background-color: #9ca3af;
		border-radius: 3px;
		opacity: 0;
		transition: opacity 0.3s ease;
	}

	.chair.visible {
		opacity: 1;
	}

	/* Circle table chairs (4 chairs at cardinal directions) */
	.chair.top {
		top: -4px;
		left: 50%;
		transform: translateX(-50%);
	}

	.chair.right {
		top: 50%;
		right: -4px;
		transform: translateY(-50%);
	}

	.chair.bottom {
		bottom: -4px;
		left: 50%;
		transform: translateX(-50%);
	}

	.chair.left {
		top: 50%;
		left: -4px;
		transform: translateY(-50%);
	}

	/* Rectangle table chairs (6 chairs) */
	.chair.right-top {
		top: 28%;
		right: -4px;
	}

	.chair.right-bottom {
		top: 72%;
		right: -4px;
		transform: translateY(-50%);
	}

	.chair.left-top {
		top: 28%;
		left: -4px;
	}

	.chair.left-bottom {
		top: 72%;
		left: -4px;
		transform: translateY(-50%);
	}

	.table-btn {
		position: relative;
		border: none;
		cursor: pointer;
		transition: none; /* Remove all transitions */
		font-size: 1rem;
		font-weight: 600;
		color: white;
		display: flex;
		align-items: center;
		justify-content: center;
		text-align: center;
		padding: 0;
		z-index: 1;
	}

	.table-btn.circle {
		width: 90px;
		height: 90px;
		border-radius: 50%;
	}

	.table-btn.square {
		width: 90px;
		height: 90px;
		border-radius: 6px;
	}

	.table-btn.disabled {
		background-color: #999;
		cursor: not-allowed;
		opacity: 0.5;
	}

	/* coloured system */
	.table-btn.available:not(.text-mode) {
		background-color: #4ade80; /* green */
	}

	.table-btn.booked:not(.text-mode) {
		background-color: #ef4444; /* red */
		cursor: not-allowed;
	}

	/* Text system - exact same color for all tables */
	.table-btn.text-mode {
		background-color: #6b7280; /* neutral gray */
	}

	.table-btn.text-mode.booked {
		background-color: #6b7280; /* exact same gray */
		cursor: not-allowed;
	}

	.table-btn.text-mode.available {
		background-color: #6b7280; /* exact same gray */
	}

	/* Override disabled opacity for text mode */
	.table-btn.text-mode:disabled {
		opacity: 1; /* Keep full opacity in text mode */
	}

	.status-text {
		font-size: 0.8rem;
		line-height: 1.2;
		padding: 6px;
	}

	.table-btn:disabled {
		cursor: not-allowed;
		opacity: 0.6;
	}
</style>

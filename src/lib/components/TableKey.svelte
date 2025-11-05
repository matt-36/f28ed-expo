<script lang="ts">
</script>

<div class="table-key">
	<h4>Table Guide:</h4>
	<div class="key-item">
		<div class="key-icon">
			<div class="mini-chair chair-top"></div>
			<div class="mini-chair chair-right"></div>
			<div class="mini-chair chair-bottom"></div>
			<div class="mini-chair chair-left"></div>
		</div>
		<span>4 chairs = 4 people</span>
	</div>
	<div class="key-item">
		<div class="key-icon">
			<div class="mini-chair chair-top"></div>
			<div class="mini-chair chair-right-top"></div>
			<div class="mini-chair chair-right-bottom"></div>
			<div class="mini-chair chair-bottom"></div>
			<div class="mini-chair chair-left-top"></div>
			<div class="mini-chair chair-left-bottom"></div>
		</div>
		<span>6 chairs = 6 people</span>
	</div>
</div>

<style>
	.table-key {
		background-color: #f9fafb;
		border: 2px solid #d1d5db;
		border-radius: 8px;
		padding: 1rem;
		margin-right: 2rem;
	}

	h4 {
		margin: 0 0 0.75rem 0;
		font-size: 1rem;
		color: #1f2937;
		font-weight: 600;
	}

	.key-item {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		margin-bottom: 0.75rem;
	}

	.key-item:last-child {
		margin-bottom: 0;
	}

	.key-item span {
		font-size: 0.875rem;
		color: #4b5563;
	}

	.key-icon {
		position: relative;
		width: 50px;
		height: 50px;
		background-color: #6b7280;
		flex-shrink: 0;
		border-radius: 4px;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.mini-chair {
		position: absolute;
		width: 6px;
		height: 6px;
		background-color: #9ca3af;
		border-radius: 1px;
	}

	/* 4 chairs layout */
	.chair-top {
		top: -3px;
		left: 50%;
		transform: translateX(-50%);
	}

	.chair-right {
		top: 50%;
		right: -3px;
		transform: translateY(-50%);
	}

	.chair-bottom {
		bottom: -3px;
		left: 50%;
		transform: translateX(-50%);
	}

	.chair-left {
		top: 50%;
		left: -3px;
		transform: translateY(-50%);
	}

	/* 6 chairs layout */
	.chair-right-top {
		top: 28%;
		right: -3px;
	}

	.chair-right-bottom {
		top: 72%;
		right: -3px;
		transform: translateY(-50%);
	}

	.chair-left-top {
		top: 28%;
		left: -3px;
	}

	.chair-left-bottom {
		top: 72%;
		left: -3px;
		transform: translateY(-50%);
	}
</style>

<script lang="ts">
    import { t } from '../i18n.js';  // Import the translation store

    export let show = false;
    export let message = "";
    export let onConfirm: () => void;
    export let onCancel: () => void;

    function handleConfirm(): void {
        onConfirm();
    }

    function handleCancel(): void {
        onCancel();
    }
</script>

{#if show}
    <div class="modal-overlay">
        <div class="modal">
            <p>{message}</p>
            <div class="modal-buttons">
                <button on:click={handleConfirm}>{$t.modal?.confirm || 'Confirm'}</button>
                <button on:click={handleCancel}>{$t.modal?.cancel || 'Cancel'}</button>
            </div>
        </div>
    </div>
{/if}

<style>
    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .modal {
        background: white;
        padding: 2rem;
        border-radius: 8px;
        text-align: center;
    }

    .modal-buttons {
        margin-top: 1rem;
        display: flex;
        justify-content: space-around;
    }

    .modal-buttons button {
        padding: 0.5rem 1rem;
        border: none;
        cursor: pointer;
    }
</style>

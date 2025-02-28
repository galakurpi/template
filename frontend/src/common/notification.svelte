<script lang="ts">
    import { onMount } from "svelte";

    export let title: string;
    export let content: string | { isHTML: boolean; html: string };
    export let type: { primary: string; secondary: string };

    let notification: HTMLDivElement;

    let timer;
    let hidden: boolean = false;
    let shake: boolean = false;

    function close() {
        clearTimeout(timer);
        hidden = true;
        setTimeout(() => {
            notification.remove();
        }, 500);
    }

    function startTimer() {
        timer = setTimeout(() => {
            close();
        }, 8000);
    }

    onMount(() => {
        console.log("mounted");
        shake = true;
        startTimer();
    });
</script>

<div
    class="notification {hidden ? 'hidden' : ''} {shake ? 'shaking' : ''}"
    style="background-color: {type.primary}; border: 1px solid {type.secondary}; border-left: 4px solid {type.secondary};"
    bind:this={notification}
>
    <div class="decoration" style="background-color: {type.secondary};" />
    <div class="text-holder">
        <div class="title">{title}</div>
        {#if typeof content === 'object' && content.isHTML}
            <div class="content">
                {@html content.html}
            </div>
        {:else}
            <div class="content">
                {content}
            </div>
        {/if}
    </div>
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <div class="close-button" on:click={close}>
        <img src="/static/icons/close.svg" alt="close" />
    </div>
    <!-- svelte-ignore a11y-missing-content -->
    <a target="_blank" rel="noreferrer" href="https://icons8.com/icon/8112/close" />
</div>

<style>
    .notification {
        display: grid;
        grid-template-columns: 1fr 15fr 2fr;
        justify-content: space-between;
        align-items: center;
        flex-direction: row;
        color: #282828;
        width: 50%;
        padding-inline: 1.3rem;
        padding-block: 0.6rem;
        background-color: #fff;
        border-radius: 5px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        z-index: 1000;
    }

    .decoration {
        width: 1.2rem;
        height: 1.2rem;
        border-radius: 50%;
    }

    .title {
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 0.1rem;
    }

    img {
        width: 1.7rem;
        height: 1.7rem;
    }

    .close-button {
        cursor: pointer;
        text-align: end;
    }

    .hidden {
        animation: fadeOut 0.5s ease-in-out forwards;
    }

    .shaking {
        animation: shake 0.5s ease-in-out;
    }

    @keyframes fadeOut {
        from {
            opacity: 1;
        }
        to {
            opacity: 0;
        }
    }

    @keyframes shake {
        0% {
            transform: translate(1px, 1px) rotate(0deg);
        }
        10% {
            transform: translate(-1px, -2px) rotate(-1deg);
        }
        20% {
            transform: translate(-3px, 0px) rotate(1deg);
        }
        30% {
            transform: translate(3px, 2px) rotate(0deg);
        }
        40% {
            transform: translate(1px, -1px) rotate(1deg);
        }
        50% {
            transform: translate(-1px, 2px) rotate(-1deg);
        }
        60% {
            transform: translate(-3px, 1px) rotate(0deg);
        }
        70% {
            transform: translate(3px, 1px) rotate(-1deg);
        }
        80% {
            transform: translate(-1px, -1px) rotate(1deg);
        }
        90% {
            transform: translate(1px, 2px) rotate(0deg);
        }
        100% {
            transform: translate(1px, -2px) rotate(-1deg);
        }
    }

    @media only screen and (max-width: 768px) {
        .notification {
            width: 80%;
        }

        .decoration {
            visibility: hidden;
        }
    }
</style>

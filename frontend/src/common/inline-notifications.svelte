<script lang="ts">
    import Notification from "./notification.svelte";

    const types = {
        success: {
            primary: "#a5eea7",
            secondary: "#2d8e2d",
        },
        error: {
            primary: "#ff8880",
            secondary: "#ff0000",
        },
        warning: {
            primary: "#FFE480",
            secondary: "#FFC000",
        },
        info: {
            primary: "#80C9FF",
            secondary: "#0070C0",
        },
    };

    export function addMessage(title: string, content: string | { isHTML: boolean; html: string }, type: string) {
        const notification = new Notification({
            target: document.querySelector(".message-holder"),
            props: {
                title,
                content,
                type: types[type],
            },
        });
    }
</script>

<div class="message-holder" />

<style>
    div {
        position: fixed;
        display: flex;
        flex-direction: column;
        gap: 1rem;
        top: 6rem;
        width: 100%;
        align-items: center;
        justify-content: center;
    }
</style>

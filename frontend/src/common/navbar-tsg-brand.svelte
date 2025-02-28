<script lang="ts">
  import { createEventDispatcher, onMount } from "svelte";

  const dispatch = createEventDispatcher();
  let currentPath = "";

  function handleMenuClick() {
    dispatch("toggle-menu");
  }

  async function handleLogout() {
    const response = await fetch('/api/logout/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
      }
    });
    if (response.ok) {
      window.location.href = '/api/login/';
    } else {
      console.error('Logout failed');
    }
  }

  function handleDashboardClick() {
    if (currentPath !== "/dashboard") {
      window.location.href = "/dashboard";
    } else {
      window.location.href = "/prototype";
    }
  }

  function handleLogoClick() {
    window.location.href = "/prototype";
  }

  onMount(() => {
    currentPath = window.location.pathname;
  });
</script>

<nav>
  <div class="left-buttons">
    {#if currentPath !== "/login"}
      <button on:click={handleDashboardClick} class="dashboard-button">
        {currentPath !== "/dashboard" ? "Dashboard" : "Upload"}
      </button>
    {/if}
  </div>
  <div class="logo-holder" on:click={handleLogoClick}>
    <img src="/static/icons/TSG-Horizontal-logo-for-web-01.svg" alt="TSG-Logo" />
  </div>
  <div class="settings-holder">
    <button on:click={handleLogout} class="logout-button">LOG OUT</button>
  </div>
</nav>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Proxima+Nova:wght@400&display=swap');

  nav {
    background-color: rgb(255, 255, 255);
    height: 6rem;
    display: flex;
    align-items: center;
    justify-content: space-between; /* Distribute space between the left, center, and right items */
    padding-inline: 2rem;
    color: #2f2f2f;
    font-family: 'Proxima Nova', sans-serif;
    text-transform: uppercase;
    border-bottom: 1px solid #e1e1e1;
  }

  .left-buttons {
    display: flex;
    justify-content: flex-start; /* Align to the far left */
    align-items: center;
    flex: 1;
  }

  .logo-holder {
    display: flex;
    justify-content: center; /* Center the logo */
    align-items: center;
    flex: 1;
    cursor: pointer;
  }

  .logo-holder img {
    height: 2.5rem;
    width: auto;
  }

  .settings-holder {
    display: flex;
    justify-content: flex-end; /* Align to the far right */
    align-items: center;
    flex: 1;
  }

  .dashboard-button {
    background-color: transparent;
    color: #2f2f2f;
    padding: 0.5rem 1rem;
    cursor: pointer;
    font-size: 1rem;
    border: none;
    text-transform: uppercase;
    position: relative;
    font-weight: 600;
  }

  .dashboard-button::after {
    content: "";
    display: block;
    width: 0;
    height: 3px;
    background-color: #1f71b8;
    position: absolute;
    bottom: -3px;
    left: 0;
  }

  .dashboard-button:hover::after {
    width: 100%;
  }

  .logout-button {
    background-color: transparent;
    color: #ed2426;
    padding: 0.5rem 1rem;
    cursor: pointer;
    font-size: 1rem;
    border: none;
    text-transform: uppercase;
    position: relative;
    font-weight: 600;
  }

  .logout-button::after {
    content: "";
    display: block;
    width: 0;
    height: 3px;
    background-color: #ed2426;
    position: absolute;
    bottom: -3px;
    left: 0;
  }

  .logout-button:hover::after {
    width: 100%;
  }
</style>
